/**
 * @file probe_parser.cpp
 * @brief Report what core's `Parser` does with each file it is handed.
 *
 * Used to reproduce the limitations in
 * design/core/2026-09-04-cpp-wav-parser-audit.md. For every file it prints
 * either the parsed header plus a count of non-finite and out-of-range samples,
 * or the exception the parser threw.
 *
 * Build (from the core repo root):
 *   g++ -O2 -std=c++17 -Iinclude \
 *       <this file> src/utils/WavParser.cpp -o probe_parser
 *
 * Usage:
 *   ./probe_parser edge-cases/*.wav
 *
 * A file declaring a huge chunk size will try to allocate it — run that one
 * under a memory limit:
 *   ( ulimit -v 2000000; ./probe_parser edge-cases/hugechunk.wav )
 */

#include <cmath>
#include <cstdio>
#include <fstream>

#include "utils/WavParser.hpp"

int main(int argc, char **argv) {
    if (argc < 2) {
        std::fprintf(stderr, "usage: %s <file> [file...]\n", argv[0]);
        return 2;
    }

    for (int i = 1; i < argc; ++i) {
        std::ifstream file(argv[i], std::ios::binary);
        if (!file) {
            std::printf("%-18s OPEN FAILED\n", argv[i]);
            continue;
        }

        try {
            const Parser p = Parser::fromFile(file, true);
            const auto &samples = p.getAudioData();

            int nan = 0, inf = 0, out_of_range = 0;
            for (float s : samples) {
                if (std::isnan(s))
                    ++nan;
                else if (std::isinf(s))
                    ++inf;
                else if (s < -1.0f || s > 1.0f)
                    ++out_of_range;
            }

            std::printf("%-18s OK    fmt=%u ch=%u bps=%u samples=%zu "
                        "otherChunks=%zu nan=%d inf=%d oob=%d\n",
                        argv[i], p.getAudioFormat(), p.getNumChannels(),
                        p.getBitsPerSample(), samples.size(), p.getOtherChunks().size(),
                        nan, inf, out_of_range);
        } catch (const std::exception &e) {
            std::printf("%-18s THROW %s\n", argv[i], e.what());
        } catch (...) {
            std::printf("%-18s THROW (non-std exception)\n", argv[i]);
        }
    }
    return 0;
}
