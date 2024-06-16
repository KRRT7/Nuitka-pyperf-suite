experimental benchmark suite for nuitka using an adapted and naive form of the CPython Benchmark Suite
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><code style="font-family:inherit"><span class="r1">              </span><span class="r2">bm_asyncio_tcp</span><span class="r1">               </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 2.10    │ 2.15   │ <span class="r4">-2.29%</span>     │
│ 3.8     │ 1.59    │ 1.56   │ <span class="r5">+1.91%</span>     │
│ 3.9     │ 1.47    │ 1.43   │ <span class="r5">+2.27%</span>     │
│ 3.10    │ 1.64    │ 1.54   │ <span class="r5">+6.24%</span>     │
│ 3.11    │ 1.64    │ 1.61   │ <span class="r5">+2.28%</span>     │
│ 3.12    │ 1.53    │ 1.39   │ <span class="r5">+9.12%</span>     │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">           </span><span class="r2">bm_asyncio_websockets</span><span class="r1">           </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 1.57    │ 1.46   │ <span class="r5">+6.67%</span>     │
│ 3.8     │ 1.44    │ 1.36   │ <span class="r5">+5.76%</span>     │
│ 3.9     │ 1.44    │ 1.37   │ <span class="r5">+5.11%</span>     │
│ 3.10    │ 1.52    │ 1.45   │ <span class="r5">+4.86%</span>     │
│ 3.11    │ 1.43    │ 1.34   │ <span class="r5">+6.24%</span>     │
│ 3.12    │ 1.46    │ 1.36   │ <span class="r5">+6.87%</span>     │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">            </span><span class="r2">bm_async_generators</span><span class="r1">            </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 0.66    │ 0.57   │ <span class="r5">+13.44%</span>    │
│ 3.8     │ 0.65    │ 0.53   │ <span class="r5">+18.36%</span>    │
│ 3.9     │ 0.64    │ 0.53   │ <span class="r5">+17.13%</span>    │
│ 3.10    │ 0.66    │ 0.52   │ <span class="r5">+21.66%</span>    │
│ 3.11    │ 0.59    │ 0.54   │ <span class="r5">+8.01%</span>     │
│ 3.12    │ 0.74    │ 0.66   │ <span class="r5">+11.32%</span>    │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">             </span><span class="r2">bm_comprehensions</span><span class="r1">             </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 1.92    │ 1.58   │ <span class="r5">+17.72%</span>    │
│ 3.8     │ 1.73    │ 1.21   │ <span class="r5">+29.84%</span>    │
│ 3.9     │ 1.65    │ 1.23   │ <span class="r5">+25.41%</span>    │
│ 3.10    │ 1.77    │ 1.27   │ <span class="r5">+28.55%</span>    │
│ 3.11    │ 1.67    │ 1.23   │ <span class="r5">+26.47%</span>    │
│ 3.12    │ 1.22    │ 1.34   │ <span class="r4">-10.02%</span>    │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">            </span><span class="r2">bm_concurrent_imap</span><span class="r1">             </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 0.94    │ 0.84   │ <span class="r5">+11.04%</span>    │
│ 3.8     │ 1.19    │ 1.13   │ <span class="r5">+4.75%</span>     │
│ 3.9     │ 1.17    │ 1.17   │ <span class="r4">-0.11%</span>     │
│ 3.10    │ 1.18    │ 1.13   │ <span class="r5">+4.35%</span>     │
│ 3.11    │ 1.06    │ 1.07   │ <span class="r4">-0.52%</span>     │
│ 3.12    │ 1.01    │ 1.62   │ <span class="r4">-61.28%</span>    │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">               </span><span class="r2">bm_coroutines</span><span class="r1">               </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 1.10    │ 1.05   │ <span class="r5">+4.34%</span>     │
│ 3.8     │ 1.08    │ 1.04   │ <span class="r5">+3.79%</span>     │
│ 3.9     │ 1.03    │ 1.01   │ <span class="r5">+2.16%</span>     │
│ 3.10    │ 0.80    │ 1.00   │ <span class="r4">-24.49%</span>    │
│ 3.11    │ 0.77    │ 1.04   │ <span class="r4">-34.34%</span>    │
│ 3.12    │ 0.67    │ 1.30   │ <span class="r4">-93.30%</span>    │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">              </span><span class="r2">bm_crypto_pyaes</span><span class="r1">              </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 1.60    │ 1.34   │ <span class="r5">+16.36%</span>    │
│ 3.8     │ 1.46    │ 1.23   │ <span class="r5">+15.63%</span>    │
│ 3.9     │ 1.35    │ 1.19   │ <span class="r5">+12.33%</span>    │
│ 3.10    │ 1.42    │ 1.20   │ <span class="r5">+15.20%</span>    │
│ 3.11    │ 1.03    │ 0.94   │ <span class="r5">+8.87%</span>     │
│ 3.12    │ 1.09    │ 1.08   │ <span class="r5">+1.65%</span>     │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">             </span><span class="r2">bm_meteor_contest</span><span class="r1">             </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 0.83    │ 0.73   │ <span class="r5">+12.01%</span>    │
│ 3.8     │ 0.74    │ 0.65   │ <span class="r5">+11.72%</span>    │
│ 3.9     │ 0.75    │ 0.65   │ <span class="r5">+12.85%</span>    │
│ 3.10    │ 0.77    │ 0.66   │ <span class="r5">+14.02%</span>    │
│ 3.11    │ 0.76    │ 0.67   │ <span class="r5">+12.79%</span>    │
│ 3.12    │ 0.77    │ 0.71   │ <span class="r5">+7.56%</span>     │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">                 </span><span class="r2">bm_nbody</span><span class="r1">                  </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 0.95    │ 0.80   │ <span class="r5">+16.46%</span>    │
│ 3.8     │ 0.77    │ 0.75   │ <span class="r5">+2.78%</span>     │
│ 3.9     │ 0.78    │ 0.75   │ <span class="r5">+3.98%</span>     │
│ 3.10    │ 0.82    │ 0.77   │ <span class="r5">+6.22%</span>     │
│ 3.11    │ 0.80    │ 0.84   │ <span class="r4">-4.48%</span>     │
│ 3.12    │ 0.76    │ 0.94   │ <span class="r4">-23.61%</span>    │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">              </span><span class="r2">bm_regex_effbot</span><span class="r1">              </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 1.39    │ 1.38   │ <span class="r5">+1.17%</span>     │
│ 3.8     │ 1.27    │ 1.25   │ <span class="r5">+1.57%</span>     │
│ 3.9     │ 1.18    │ 1.16   │ <span class="r5">+1.67%</span>     │
│ 3.10    │ 1.25    │ 1.23   │ <span class="r5">+1.44%</span>     │
│ 3.11    │ 1.13    │ 1.08   │ <span class="r5">+4.17%</span>     │
│ 3.12    │ 1.13    │ 1.12   │ <span class="r5">+0.98%</span>     │
└─────────┴─────────┴────────┴────────────┘
<span class="r1">                </span><span class="r2">bm_sqlglot</span><span class="r1">                 </span>
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃<span class="r3"> Version </span>┃<span class="r3"> Cpython </span>┃<span class="r3"> Nuitka </span>┃<span class="r3"> Difference </span>┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 3.7     │ 2.28    │ 1.79   │ <span class="r5">+21.51%</span>    │
│ 3.8     │ 1.67    │ 1.31   │ <span class="r5">+21.49%</span>    │
│ 3.9     │ 1.65    │ 1.34   │ <span class="r5">+18.35%</span>    │
│ 3.10    │ 1.76    │ 1.40   │ <span class="r5">+20.33%</span>    │
│ 3.11    │ 1.63    │ 1.41   │ <span class="r5">+13.68%</span>    │
│ 3.12    │ 1.55    │ 1.61   │ <span class="r4">-3.81%</span>     │
└─────────┴─────────┴────────┴────────────┘
</code></pre>
</body>
</html>
