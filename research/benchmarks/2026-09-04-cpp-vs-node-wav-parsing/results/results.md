Median of 41 repetitions, milliseconds per call. Node v22.22.2.

### Full decode (`process` path)

| File | C++ median | C++ min | Node median | Node min | Node / C++ (median) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `flt32_30s.wav` | 3.083 | 2.761 | 36.940 | 35.620 | 12× |
| `pcm08_30s.wav` | 2.370 | 2.279 | 6.999 | 6.378 | 2.95× |
| `pcm16_05s.wav` | 0.394 | 0.364 | 2.433 | 2.302 | 6.17× |
| `pcm16_180s.wav` | 45.493 | 44.094 | 109.064 | 86.596 | 2.40× |
| `pcm16_30s.wav` | 2.651 | 2.414 | 15.082 | 14.431 | 5.69× |
| `pcm16_600s.wav` | 191.943 | 187.411 | 435.316 | 352.453 | 2.27× |
| `pcm24_30s.wav` | 5.082 | 4.585 | 11.175 | 10.683 | 2.20× |
| `pcm32_30s.wav` | 3.310 | 2.736 | 18.657 | 18.112 | 5.64× |
| `real_sound_186s.wav` | 47.256 | 44.969 | 166.355 | 146.188 | 3.52× |

### Header only (`readMetadata` path)

| File | C++ median | C++ min | Node median | Node min | Node / C++ (median) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `flt32_30s.wav` | 0.002 | 0.002 | 0.013 | 0.012 | 5.23× |
| `pcm08_30s.wav` | 0.254 | 0.240 | 0.012 | 0.012 | 0.05× |
| `pcm16_05s.wav` | 0.002 | 0.002 | 0.012 | 0.011 | 5.15× |
| `pcm16_180s.wav` | 0.003 | 0.002 | 0.013 | 0.012 | 5.06× |
| `pcm16_30s.wav` | 0.003 | 0.002 | 0.012 | 0.011 | 4.72× |
| `pcm16_600s.wav` | 0.003 | 0.002 | 0.012 | 0.011 | 4.94× |
| `pcm24_30s.wav` | 0.814 | 0.764 | 0.011 | 0.011 | 0.01× |
| `pcm32_30s.wav` | 1.160 | 1.058 | 0.012 | 0.011 | 0.01× |
| `real_sound_186s.wav` | 0.003 | 0.002 | 0.011 | 0.010 | 4.42× |

### Throughput, full decode

| File | Samples | C++ (Msample/s) | Node (Msample/s) |
| --- | ---: | ---: | ---: |
| `flt32_30s.wav` | 2,646,000 | 858.1 | 71.6 |
| `pcm08_30s.wav` | 2,646,000 | 1116.5 | 378.0 |
| `pcm16_05s.wav` | 441,000 | 1118.4 | 181.3 |
| `pcm16_180s.wav` | 15,876,000 | 349.0 | 145.6 |
| `pcm16_30s.wav` | 2,646,000 | 998.2 | 175.4 |
| `pcm16_600s.wav` | 52,920,000 | 275.7 | 121.6 |
| `pcm24_30s.wav` | 2,646,000 | 520.6 | 236.8 |
| `pcm32_30s.wav` | 2,646,000 | 799.4 | 141.8 |
| `real_sound_186s.wav` | 16,433,152 | 347.7 | 98.8 |

### Run-to-run spread, full decode

Gap between the slowest and fastest replicate median, over 3 replicates. This is the error bar on the figures above — differences smaller than this are noise.

| File | C++ | Node |
| --- | ---: | ---: |
| `flt32_30s.wav` | 12.5% | 5.3% |
| `pcm08_30s.wav` | 1.0% | 10.4% |
| `pcm16_05s.wav` | 0.5% | 7.1% |
| `pcm16_180s.wav` | 2.1% | 1.7% |
| `pcm16_30s.wav` | 6.6% | 9.4% |
| `pcm16_600s.wav` | 2.2% | 1.9% |
| `pcm24_30s.wav` | 6.1% | 2.3% |
| `pcm32_30s.wav` | 26.7% | 2.1% |
| `real_sound_186s.wav` | 4.2% | 5.9% |

Whole-run peak RSS: C++ 337 MB, Node 389 MB.
