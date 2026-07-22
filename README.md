# SHine-K — Reproducibility Package

Code, benchmarks, and per-run provenance for:

> **Design and Working Prototype of SHine-K: An Edge-AI, Video-Free Web Platform for
> Centralized Worker Safety-and-Health Monitoring in SME Manufacturing**
> (Sensors, MDPI — submitted 2026)

**Interactive demonstration site** (simulation control-twin + in-browser live edge demo running the
same deployed fall-detection state machine evaluated here):
**https://y3korea.github.io/shine-k/** · source: [y3korea/shine-k](https://github.com/y3korea/shine-k)

## Reproduce the fall-detection evaluation (URFD)

| Notebook | What it does | One-click |
|---|---|---|
| `SHine-K_urfd_minimal_colab.ipynb` | **Minimal 3-cell reproduction** — full 70-sequence URFD run, no Drive mount needed, results zip auto-downloads. Verified: `fall-01` triggers at frame 150, identical to the manuscript run | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_urfd_minimal_colab.ipynb) |
| `SHine-K_full70_colab.ipynb` | **Full URFD run — 30 fall + 40 ADL sequences**, deployed thresholds (sens = 1.0), no re-tuning | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_full70_colab.ipynb) |
| `SHine-K_reproducibility_colab.ipynb` | Paper figures (Fig. 1–4, 300 dpi), recovery-guide GIFs, post-processing micro-benchmark, and the 8+8-sequence URFD subset run reported in the manuscript | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_reproducibility_colab.ipynb) |

Run everything with **Runtime → Run all**. Each run writes a timestamped `output/run_<id>/` folder
containing `eval_metrics.json`, `eval_per_sequence.csv`, `eval_confusion_matrix.png`, and a
`run_manifest.json` with environment versions and SHA-256 content hashes.

## Contents

- `SHine-K_urfd_minimal_colab.ipynb` — minimal 3-cell full-70 reproduction (deps → evaluate → zip)
- `SHine-K_full70_colab.ipynb` — full 70-sequence URFD evaluation (env-var config only; evaluation cell identical to the original notebook)
- `SHine-K_reproducibility_colab.ipynb` — figures · GIFs · latency micro-benchmark · URFD subset evaluation
- `gen_figures.py` — publication figures (Fig. 1–4, 300 dpi, monochrome academic style)
- `gen_gifs.py` — recovery-exercise animation guides
- `latency_benchmark.js` — post-processing micro-benchmark (simplified REBA + fire pixel-scan; neural inference excluded)
- `output/run_20260627_222419/` — the exact run cited in the manuscript (metrics, per-sequence CSV, confusion matrix, logs, manifest)

## Results (measured)

| Run | Sequences | Precision | Recall | F1 | Accuracy | Median latency |
|---|---|---|---|---|---|---|
| `run_20260722_195713_full70` — **full benchmark** | 30 fall + 40 ADL | 0.61 | 0.77 (23/30) | 0.68 | 0.69 | 57 frames ≈ 1.9 s |
| `run_20260627_222419` — standing-fall subset | 8 fall + 8 ADL | 0.73 | 1.00 (8/8) | 0.84 | 0.81 | 99.5 frames ≈ 3.3 s |

Failure modes on the full run are structured (per-frame diagnostics): missed falls crossed the posture
thresholds only transiently without sustaining the 700 ms confirmation window; false alarms split into
sustained deep-bending vs deliberate lying-down classes. Both run folders under `output/` carry the full
per-sequence CSVs and manifests.

## Data

The [UR Fall Detection dataset (URFD)](https://fenix.ur.edu.pl/~mkepski/ds/uf.html) is publicly
available; the notebooks download the cam0 RGB sequences directly. No new human-subject data were
collected for this evaluation.

## Honest-staging note

Only the URFD evaluation and the post-processing micro-benchmark are **measured** results.
Emergency 119/e-Gen linkage, radar/thermal sensing, the 12-agent harness, and all business metrics
are design targets, as stated in the manuscript (Table 2).

## Funding

This research was supported by the ANCHOR program through the Gyeongbuk ANCHOR Center, funded by
the Ministry of Education (MOE) and Gyeongsangbuk-do, Republic of Korea (2026-ANCHOR-15-102).

## License

MIT — see [LICENSE](LICENSE).
