Median of 41 repetitions, milliseconds per call. Node v22.23.2.

### Full decode (`process` path)

| File | C++ median | C++ min | Node median | Node min | Node / C++ (median) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `flt32_30s.wav` | 3.458 | 3.188 | 14.250 | 13.282 | 4.12× |
| `pcm08_30s.wav` | 1.052 | 1.024 | 3.557 | 2.867 | 3.38× |
| `pcm16_05s.wav` | 0.199 | 0.191 | 1.563 | 1.361 | 7.84× |
| `pcm16_180s.wav` | 22.025 | 20.463 | 62.034 | 54.602 | 2.82× |
| `pcm16_30s.wav` | 1.397 | 1.311 | 9.342 | 8.954 | 6.69× |
| `pcm16_600s.wav` | 84.064 | 81.069 | 205.832 | 197.263 | 2.45× |
| `pcm24_30s.wav` | 2.962 | 2.762 | 7.657 | 6.783 | 2.58× |
| `pcm32_30s.wav` | 2.327 | 2.221 | 12.509 | 11.630 | 5.38× |
| `real_sound_186s.wav` | 22.733 | 21.298 | 63.767 | 56.272 | 2.80× |

### Header only (`readMetadata` path)

| File | C++ median | C++ min | Node median | Node min | Node / C++ (median) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `flt32_30s.wav` | 0.002 | 0.002 | 0.016 | 0.015 | 8.17× |
| `pcm08_30s.wav` | 0.118 | 0.106 | 0.013 | 0.013 | 0.11× |
| `pcm16_05s.wav` | 0.002 | 0.002 | 0.013 | 0.013 | 6.86× |
| `pcm16_180s.wav` | 0.002 | 0.002 | 0.013 | 0.013 | 7.02× |
| `pcm16_30s.wav` | 0.002 | 0.002 | 0.013 | 0.013 | 6.89× |
| `pcm16_600s.wav` | 0.002 | 0.002 | 0.013 | 0.013 | 7.06× |
| `pcm24_30s.wav` | 1.159 | 1.052 | 0.013 | 0.012 | 0.01× |
| `pcm32_30s.wav` | 1.513 | 1.317 | 0.013 | 0.012 | 0.01× |
| `real_sound_186s.wav` | 0.002 | 0.002 | 0.011 | 0.011 | 5.99× |

### Throughput, full decode

| File | Samples | C++ (Msample/s) | Node (Msample/s) |
| --- | ---: | ---: | ---: |
| `flt32_30s.wav` | 2,646,000 | 765.1 | 185.7 |
| `pcm08_30s.wav` | 2,646,000 | 2515.9 | 743.9 |
| `pcm16_05s.wav` | 441,000 | 2212.7 | 282.2 |
| `pcm16_180s.wav` | 15,876,000 | 720.8 | 255.9 |
| `pcm16_30s.wav` | 2,646,000 | 1894.3 | 283.2 |
| `pcm16_600s.wav` | 52,920,000 | 629.5 | 257.1 |
| `pcm24_30s.wav` | 2,646,000 | 893.2 | 345.6 |
| `pcm32_30s.wav` | 2,646,000 | 1137.0 | 211.5 |
| `real_sound_186s.wav` | 16,433,152 | 722.9 | 257.7 |

### Run-to-run spread, full decode

Gap between the slowest and fastest replicate median, over 3 replicates. This is the error bar on the figures above — differences smaller than this are noise.

| File | C++ | Node |
| --- | ---: | ---: |
| `flt32_30s.wav` | 20.6% | 0.5% |
| `pcm08_30s.wav` | 6.7% | 8.3% |
| `pcm16_05s.wav` | 0.5% | 3.9% |
| `pcm16_180s.wav` | 6.5% | 0.3% |
| `pcm16_30s.wav` | 4.8% | 0.6% |
| `pcm16_600s.wav` | 2.9% | 3.0% |
| `pcm24_30s.wav` | 6.6% | 1.5% |
| `pcm32_30s.wav` | 9.1% | 0.3% |
| `real_sound_186s.wav` | 5.1% | 0.9% |

Whole-run peak RSS: C++ 336 MB, Node 431 MB.
