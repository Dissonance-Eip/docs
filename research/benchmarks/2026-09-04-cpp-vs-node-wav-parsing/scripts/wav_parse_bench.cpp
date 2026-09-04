/**
 * @file wav_parse_bench.cpp
 * @brief Times the production `Parser` (core/src/utils/WavParser.cpp) against a
 *        corpus of WAV files and prints one JSON object to stdout.
 *
 * Two operations are timed per file, matching the two things the addon actually
 * does:
 *   header  - Parser::fromFile(file, readAudioData = false)  -> readMetadata()
 *   decode  - Parser::fromFile(file, readAudioData = true)   -> process()
 *
 * Build (from the core repo root):
 *   g++ -O2 -std=c++17 -Iinclude \
 *       <this file> src/utils/WavParser.cpp -o wav_parse_bench
 *
 * Usage:
 *   ./wav_parse_bench <reps> <file> [file...]
 */

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <string>
#include <vector>

#include "utils/WavParser.hpp"

#if defined(__unix__) || defined(__APPLE__)
#include <sys/resource.h>
#endif

namespace {

struct Stats {
    double min_ms{0};
    double median_ms{0};
    double mean_ms{0};
};

Stats summarise(std::vector<double> samples) {
    std::sort(samples.begin(), samples.end());
    Stats s;
    s.min_ms = samples.front();
    s.median_ms = samples[samples.size() / 2];
    double total = 0.0;
    for (double v : samples)
        total += v;
    s.mean_ms = total / static_cast<double>(samples.size());
    return s;
}

Stats timeParse(const std::string &path, int reps, bool readAudioData, size_t &samplesOut) {
    std::vector<double> runs;
    runs.reserve(static_cast<size_t>(reps));

    for (int i = 0; i < reps; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        std::ifstream file(path, std::ios::binary);
        Parser parser = Parser::fromFile(file, readAudioData);
        auto t1 = std::chrono::steady_clock::now();
        runs.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());
        samplesOut = parser.getAudioData().size();
    }
    return summarise(std::move(runs));
}

long peakRssKb() {
#if defined(__unix__) || defined(__APPLE__)
    struct rusage usage {};
    getrusage(RUSAGE_SELF, &usage);
#if defined(__APPLE__)
    return usage.ru_maxrss / 1024; // macOS reports bytes
#else
    return usage.ru_maxrss; // Linux reports kilobytes
#endif
#else
    return -1;
#endif
}

} // namespace

int main(int argc, char **argv) {
    if (argc < 3) {
        std::fprintf(stderr, "usage: %s <reps> <file> [file...]\n", argv[0]);
        return 2;
    }

    const int reps = std::atoi(argv[1]);
    std::printf("{\n  \"runner\": \"cpp\",\n  \"reps\": %d,\n  \"files\": [\n", reps);

    for (int i = 2; i < argc; ++i) {
        const std::string path = argv[i];

        // Warm the page cache so we measure parsing, not the first disk read.
        {
            std::ifstream warm(path, std::ios::binary);
            Parser::fromFile(warm, true);
        }

        size_t sampleCount = 0;
        size_t ignored = 0;
        const Stats header = timeParse(path, reps, false, ignored);
        const Stats decode = timeParse(path, reps, true, sampleCount);

        std::printf("    {\"file\": \"%s\", \"samples\": %zu,\n"
                    "     \"header\": {\"min\": %.4f, \"median\": %.4f, \"mean\": %.4f},\n"
                    "     \"decode\": {\"min\": %.4f, \"median\": %.4f, \"mean\": %.4f}}%s\n",
                    path.c_str(), sampleCount, header.min_ms, header.median_ms, header.mean_ms,
                    decode.min_ms, decode.median_ms, decode.mean_ms, (i + 1 < argc) ? "," : "");
        std::fflush(stdout);
    }

    std::printf("  ],\n  \"peakRssKb\": %ld\n}\n", peakRssKb());
    return 0;
}
