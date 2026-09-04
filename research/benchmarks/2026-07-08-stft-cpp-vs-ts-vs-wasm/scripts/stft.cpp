// Dissonance STFT benchmark - native C++ reference (stands in for JUCE/C++ DSP path)
// Same algorithm as the WASM and TS versions: Hann window, 2048-pt radix-2 FFT,
// hop 512, forward + inverse per frame, 5-minute stereo 44.1 kHz signal.
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <chrono>
#include <vector>
#include <algorithm>

static const int SR = 44100;
static const int SECONDS = 300;
static const int CHANNELS = 2;
static const int N = SR * SECONDS;
static const int FRAME = 2048;
static const int HOP = 512;

static void fft(double* re, double* im, int n, bool inverse) {
    // bit-reversal permutation
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) { std::swap(re[i], re[j]); std::swap(im[i], im[j]); }
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2.0 * M_PI / len * (inverse ? 1.0 : -1.0);
        double wr = std::cos(ang), wi = std::sin(ang);
        for (int i = 0; i < n; i += len) {
            double cr = 1.0, ci = 0.0;
            for (int j = 0; j < len / 2; j++) {
                int a = i + j, b = i + j + len / 2;
                double vr = re[b] * cr - im[b] * ci;
                double vi = re[b] * ci + im[b] * cr;
                re[b] = re[a] - vr; im[b] = im[a] - vi;
                re[a] += vr;        im[a] += vi;
                double ncr = cr * wr - ci * wi;
                ci = cr * wi + ci * wr; cr = ncr;
            }
        }
    }
    if (inverse) {
        double inv = 1.0 / n;
        for (int i = 0; i < n; i++) { re[i] *= inv; im[i] *= inv; }
    }
}

int main() {
    // deterministic pseudo-random "audio" (LCG), float32 like a decoded WAV
    std::vector<float> signal((size_t)N * CHANNELS);
    uint32_t x = 1234567u;
    for (size_t i = 0; i < signal.size(); i++) {
        x = x * 1664525u + 1013904223u;
        signal[i] = (float)(((x >> 8) / 16777216.0) * 2.0 - 1.0);
    }
    std::vector<double> win(FRAME);
    for (int i = 0; i < FRAME; i++)
        win[i] = 0.5 * (1.0 - std::cos(2.0 * M_PI * i / (FRAME - 1)));

    std::vector<double> re(FRAME), im(FRAME);
    int frames = (N - FRAME) / HOP + 1;
    const int ITER = 5;
    printf("impl=cpp frames_per_channel=%d channels=%d fft=%d hop=%d\n", frames, CHANNELS, FRAME, HOP);
    for (int it = 0; it < ITER; it++) {
        double checksum = 0.0;
        auto t0 = std::chrono::steady_clock::now();
        for (int ch = 0; ch < CHANNELS; ch++) {
            const float* s = signal.data() + (size_t)ch * N;
            for (int f = 0; f < frames; f++) {
                const float* p = s + (size_t)f * HOP;
                for (int i = 0; i < FRAME; i++) { re[i] = p[i] * win[i]; im[i] = 0.0; }
                fft(re.data(), im.data(), FRAME, false);
                fft(re.data(), im.data(), FRAME, true);
                checksum += re[0] + re[FRAME / 2];
            }
        }
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        printf("iter=%d ms=%.1f checksum=%.6f\n", it, ms, checksum);
    }
    return 0;
}
