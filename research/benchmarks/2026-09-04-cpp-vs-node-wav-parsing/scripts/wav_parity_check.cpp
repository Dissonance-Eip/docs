/**
 * @file wav_parity_check.cpp
 * @brief Prints a fingerprint of what core's `Parser` decoded from a WAV file.
 *
 * The Node harness prints the same fingerprint. If the two differ, the
 * benchmark is comparing two different algorithms and its numbers are void.
 *
 * Build (from the core repo root):
 *   g++ -O2 -std=c++17 -Iinclude \
 *       <this file> src/utils/WavParser.cpp -o wav_parity_check
 *
 * Usage: ./wav_parity_check <file>
 */

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <string>

#include "utils/WavParser.hpp"

int main(int argc, char **argv) {
    if (argc != 2) {
        std::fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 2;
    }

    std::ifstream file(argv[1], std::ios::binary);
    const Parser p = Parser::fromFile(file, true);
    const auto &samples = p.getAudioData();

    // FNV-1a over the raw float bits: catches any per-sample difference.
    uint64_t hash = 14695981039346656037ULL;
    for (float s : samples) {
        uint32_t bits;
        std::memcpy(&bits, &s, sizeof(bits));
        for (int b = 0; b < 4; ++b) {
            hash ^= static_cast<uint8_t>(bits >> (b * 8));
            hash *= 1099511628211ULL;
        }
    }

    std::printf("{\"audioFormat\":%u,\"numChannels\":%u,\"sampleRate\":%u,\"byteRate\":%u,"
                "\"blockAlign\":%u,\"bitsPerSample\":%u,\"dataSize\":%u,\"samples\":%zu,"
                "\"otherChunks\":%zu,\"hash\":\"%016llx\"}\n",
                p.getAudioFormat(), p.getNumChannels(), p.getSampleRate(), p.getByteRate(),
                p.getBlockAlign(), p.getBitsPerSample(), p.getSubchunk2Size(), samples.size(),
                p.getOtherChunks().size(), static_cast<unsigned long long>(hash));
    return 0;
}
