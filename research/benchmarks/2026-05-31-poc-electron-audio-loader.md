---
title: POC 1 — Electron audio loader
status: final
owner: Noé Kurata
created: 2026-05-31
updated: 2026-09-04
milestone: B
tags: [poc, electron, core, addon]
---

# POC 1 — Electron audio loader

## 1. Goal of this POC

- Document how the Dissonance Electron app discovers and loads the native `dissonance_core` audio engine.
- Explain how this loader is wired into the Electron main process lifecycle (startup, IPC, cleanup).
- Describe the main technologies involved so future contributors can debug or extend the loader without reading every source file.

This POC is about the loader and integration glue, not the DSP internals. The audio processing itself lives in the separate [`core`](https://github.com/Dissonance-Eip/core) repository as a C++ Node addon.

---

## 2. High level overview

At a high level, the Electron loader is responsible for:

- Discovering an appropriate `dissonance_core` `.node` binary for the current platform and architecture.
- Supporting overrides for local development, while keeping CI and packaged builds simple.
- Loading the addon once at startup in the Electron main process and exposing it through a small IPC surface.
- Ensuring processed audio is written to safe temporary locations instead of next to the user's input files.
- Cleaning up temporary processed files when the app quits.

The renderer never imports the addon directly. All interaction with `dissonance_core` happens over IPC channels prefixed `core:`.

---

## 3. Technologies in play

### 3.1 Electron multi process model

The UI is built as a classic Electron app with:

- **Main process** - creates the window, registers IPC handlers, owns addon loading and all disk IO.
- **Preload script** - exposes a safe API on `window.dissonance` that forwards to IPC.
- **Renderer** - pure browser environment that talks only to the preload bridge and never imports Node modules directly.

The loader and IPC handlers live entirely on the main side and are registered once per `BrowserWindow`.

### 3.2 Node.js native addon (`.node`)

The audio engine is compiled as a Node native addon that exports functions such as:

- `process(inputPath, options)` - run the audio pipeline on a WAV file and write a processed output.
- `readMetadata(inputPath)` - read header information and LIST/INFO tags without decoding the whole audio stream.
- `writeTags(inputPath, tags)` - update the LIST/INFO chunk in place.

The loader's job is to locate a `.node` file that implements this API and load it with `require(...)`.

### 3.3 Node and Electron APIs

The loader and IPC layer are implemented with:

- `require`, `require.resolve` - to load the addon or discover helper modules such as `bindings`.
- `fs` and `fs.promises` - to check candidate paths, copy exported files, and remove temporary files.
- `path` - to build platform independent paths to `Build/Release` or `build/Release`.
- `ipcMain.handle` and `webContents.send` - to expose `core:*` request handlers and send status events back to the renderer.
- `dialog.showSaveDialog` - to ask the user where to write exported processed files.

### 3.4 Environment and CI integration

The loader also integrates with the surrounding tooling:

- `DISSONANCE_CORE_ADDON_PATH` - environment variable that forces the loader to use a specific `.node` file for local builds.
- GitHub Actions workflow `sync-core-addon.yml` in the UI repo - downloads prebuilt addon binaries from core releases into `Build/Release/` so the loader finds them without manual copying.

---

## 4. Electron lifecycle and loader placement

### 4.1 Main entry point

The Electron main entry point is `main.js`:

```js
// main.js
const { MainApplication } = require('./main/MainApplication');

new MainApplication({ uiRoot: __dirname }).run();
```

`MainApplication` is responsible for:

- Creating the main `BrowserWindow`.
- Loading `index.html` from `uiRoot`.
- Registering IPC handlers.
- Managing quit and close so that pending tag writes flush before the process exits.
- Triggering final cleanup of temporary files on `will-quit`.

### 4.2 Composition root for IPC

IPC registration is centralized in `ipcHandlers/fileHandlers.js`:

```js
// ipcHandlers/fileHandlers.js
const { UiLogForwarder } = require('./UiLogForwarder');
const { FileDialogHandlers } = require('./FileDialogHandlers');
const { registerThemeHandlers } = require('./themeHandlers');
const { registerCoreHandlers } = require('./core/coreSetup');

function registerFileHandlers(mainWindow) {
  new UiLogForwarder().register();
  new FileDialogHandlers().register();
  registerThemeHandlers(mainWindow);
  registerCoreHandlers(mainWindow);
}

module.exports = { registerFileHandlers };
```

`MainApplication` calls `registerFileHandlers(win)` once, immediately after creating the window and before the user interacts with the UI. This means the core loader is part of a small, explicit composition root instead of ad hoc `require` calls distributed across the codebase.

### 4.3 Core setup singleton

Core related wiring lives in `ipcHandlers/core/coreSetup.js`:

```js
// ipcHandlers/core/coreSetup.js
const { CoreAddonLoader } = require('./CoreAddonLoader');
const { TempFileManager } = require('./TempFileManager');
const { CoreIpcHandlers } = require('./CoreIpcHandlers');

const tempFileManager = new TempFileManager();
const coreAddon = new CoreAddonLoader().load();
const coreIpcHandlers = new CoreIpcHandlers({ coreAddon, tempFileManager });

function registerCoreHandlers(mainWindow) {
  coreIpcHandlers.register(mainWindow);
}

async function cleanupAllTempFiles() {
  await tempFileManager.cleanupAll();
}

module.exports = { registerCoreHandlers, cleanupAllTempFiles };
```

The important design choices are:

- The addon is loaded once at module load time.
- A single `TempFileManager` instance is shared across all core IPC handlers.
- Callers interact only through `registerCoreHandlers(mainWindow)` and `cleanupAllTempFiles()`.

`MainApplication` calls `cleanupAllTempFiles()` from its `will-quit` handler to remove any remaining processed temp files.

---

## 5. CoreAddonLoader - how the addon is discovered

### 5.1 Candidate paths

`CoreAddonLoader` is the one place that knows where `.node` files may live. It constructs a list of candidates:

1. Explicit override via `DISSONANCE_CORE_ADDON_PATH` if the environment variable is set.
2. Platform specific binary under `Build/Release/`  
   `dissonance_core-${platform}-${arch}.node`
3. Generic binary under `Build/Release/`  
   `dissonance_core.node`
4. Generic binary under `build/Release/`  
   `dissonance_core.node`
5. Platform specific binary under `build/Release/`  
   `dissonance_core-${platform}-${arch}.node`

Conceptually:

```js
function getAddonCandidates() {
  const candidates = [];

  const override = process.env.DISSONANCE_CORE_ADDON_PATH || null;
  if (override) candidates.push(override);

  const platform = process.platform;
  const arch = process.arch;

  candidates.push(path.join(__dirname, '..', '..', 'Build', 'Release', `dissonance_core-${platform}-${arch}.node`));
  candidates.push(path.join(__dirname, '..', '..', 'Build', 'Release', 'dissonance_core.node'));
  candidates.push(path.join(__dirname, '..', '..', 'build', 'Release', 'dissonance_core.node'));
  candidates.push(path.join(__dirname, '..', '..', 'build', 'Release', `dissonance_core-${platform}-${arch}.node`));

  return [...new Set(candidates.filter(Boolean))];
}
```

### 5.2 Loading strategy and fallbacks

The loader then:

- Splits candidates into those that exist on disk and those that do not.
- Tries to `require(addonPath)` for each candidate in priority order.
- Logs the list of attempted paths and the one that succeeded, when any.

If all candidate paths fail, it falls back to:

1. `require('dissonance-core')` - a potential npm package form of the addon.
2. `require('bindings')('dissonance_core')` - using the generic `bindings` helper if it is available.

The loader never throws. Instead it returns either a loaded module or `null`. Call sites check `coreAddon` and return structured IPC errors if the addon is missing, rather than crashing the entire Electron process.

### 5.3 Why this design

This layout:

- Centralizes all path and fallback logic in one module.
- Makes CI and local development agree on a small number of directories (`Build/Release` and `build/Release`).
- Allows developers to override the addon location during experiments without touching the code.
- Keeps error handling and logging in one place, which simplifies debugging when the addon fails to load.

---

## 6. CoreIpcHandlers - exposing the addon safely

`CoreIpcHandlers` is the main side class that wraps `dissonance_core` behind IPC handlers and status events. It is created by `coreSetup` with a specific `coreAddon` instance and a shared `TempFileManager`.

### 6.1 Channels

The following request channels are registered with `ipcMain.handle`:

- `core:process` - run the audio pipeline and produce a processed temp file.
- `core:readMetadata` - read header and LIST/INFO metadata.
- `core:writeTags` - update LIST/INFO metadata for a given file.
- `core:export` - copy a processed temp file to a user chosen path.
- `core:cleanupProcessed` - delete a single processed temp file.

Additionally, status updates are pushed back to the renderer on the `core:status` channel. Typical statuses are:

- `processing` - processing has started.
- `processed` - processing finished, with a `processedPath` attached.
- `exported` - export finished, with an `exportedPath`.
- `error` - something failed, with an `error` message.

### 6.2 Example - `core:process`

High level flow:

1. Validate there is a main window, a file path, and a loaded addon with a `process` function.
2. Ask the `TempFileManager` to clean up previous temp files for that renderer.
3. Ask the `TempFileManager` to create a new temp output path for this input file.
4. Merge renderer supplied options (for example perturbation strength) with the forced `outputPath`.
5. Send a `core:status` message with `status: 'processing'`.
6. Await `coreAddon.process(filePath, addonOptions)`.
7. Register the resulting processed path with `TempFileManager`.
8. Send a `core:status` message with `status: 'processed'` and return `{ ok: true, processedPath }`.
9. On error, send a `core:status` message with `status: 'error'` and return `{ ok: false, error: '...' }`.

Important design points:

- The renderer cannot choose the output location, it only provides `filePath` and user facing options. The main process always controls where processed files are stored.
- Temp files are tracked per renderer via a sender id so that a renderer can not leak processed files across sessions.
- Status updates are decoupled from the return value of the handler, which keeps the IPC contract small and predictable.

### 6.3 Metadata and tag editing

Two additional handlers support metadata features:

- `core:readMetadata` - wraps the addon function that parses header and LIST/INFO tags. The renderer's `WavMetadataService` converts this into a display friendly shape that feeds the Analyze view.
- `core:writeTags` - wraps the addon function that applies tag updates. The renderer's `TagWriteQueue` calls this whenever queued edits need to be flushed, for example on pause, file switch, or app quit.

This keeps binary safe operations on the main side, while metadata presentation and queuing logic stay in the renderer.

---

## 7. TempFileManager - keeping processed audio safe

`TempFileManager` owns the lifecycle of processed files created by `core:process`:

- Creates a dedicated root under the system temp directory, for example something like `os.tmpdir()/dissonance/`.
- Generates per input temp paths, usually combining the original filename with a unique suffix.
- Tracks which temp files belong to which renderer via sender id.
- Provides methods:
  - `ensureRootDir()` - create the root folder if it does not exist.
  - `makeTempProcessedPath(inputPath)` - compute the processed file path for a given input file.
  - `registerForSender(senderId, processedPath)` - remember that this sender owns this temp file.
  - `cleanupTempFile(processedPath)` - delete a specific processed file.
  - `cleanupForSender(senderId)` - delete all processed files created for this renderer.
  - `cleanupAll()` - delete every tracked file at app shutdown.

Using a centralized manager avoids:

- Overwriting input files with processed output.
- Leaving large processed files in random locations on disk.
- Duplicated cleanup logic scattered across handlers.

---

## 8. How the renderer uses the loader

On the renderer side:

- The preload script exposes a small API on `window.dissonance` that wraps IPC invocations for:
  - `processFile`
  - `readMetadata`
  - `writeTags`
  - `exportFile`
  - `cleanupProcessed`
- `renderer/infrastructure/DissonanceApi` turns these into methods that return predictable objects `{ ok, ... }` instead of raw IPC responses.
- Services and controllers use this API:
  - `WavMetadataService` reads metadata and converts it into `basicInfo` and tag fields for display.
  - `TagWriteQueue` queues and flushes tag writes, calling `writeTags` through the API.
  - `AppController` coordinates higher level flows such as processing, compare view updates, and quit flush.

This clear separation means:

- The main process owns all OS integration, addon loading, file IO, and temp management.
- The renderer owns UI, view state, and user flows.
- The preload bridge is a small, typed boundary between both.

---

## 9. Relationship to earlier Electron research

The earlier document `research/benchmarks/2025-11-21-electron-comparative-study.md` explains why the project chose an Electron plus TypeScript architecture instead of a JUCE or pure C++ UI stack. That study covers trade offs around performance, customization, design system support, and long term maintainability.

This POC builds on that decision by:

- Documenting exactly how the current Electron UI loads the core audio engine.
- Showing where addon binaries live and how they are discovered and loaded.
- Describing the IPC surface that exposes core functions to the renderer.
- Explaining how temp files and export behavior are handled to avoid data loss or disk bloat.

The intention is that future changes to the core addon layout or API can be implemented by updating the loader modules described here, without surprising behavior elsewhere in the app.