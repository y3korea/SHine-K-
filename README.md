# SHine-K (Safety and Health in Enterprise) — Reproducibility Package

Code, benchmarks, and per-run provenance for:

> **Design and Working Prototype of SHine-K: An Edge-AI, Video-Free Web Platform for
> Centralized Worker Safety-and-Health Monitoring in SME Manufacturing**
> (IEEE Access — under submission, 2026)

**Interactive demonstration site** (simulation control-twin + in-browser live edge demo running the
same deployed fall-detection state machine evaluated here):
**https://y3korea.github.io/shine-k/** · source: [y3korea/shine-k](https://github.com/y3korea/shine-k)

## Reproduce the fall-detection evaluation (URFD + GMDCSA-24)

| Notebook | What it does | One-click |
|---|---|---|
| `SHine-K_full70_sweep_colab.ipynb` | **Everything in the Evaluation section, one click** — full 70-sequence URFD run + threshold sweep (7 tilt × 5 window) + component ablation + **GMDCSA-24 cross-dataset evaluation** (auto-downloads v2.0 from Zenodo, CC BY 4.0; deployed thresholds, no re-tuning; per-clip predictions saved) | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_full70_sweep_colab.ipynb) |
| `SHine-K_urfd_minimal_colab.ipynb` | **Minimal 3-cell reproduction** — full 70-sequence URFD run, no Drive mount needed, results zip auto-downloads. Verified: `fall-01` triggers at frame 150, identical to the manuscript run | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_urfd_minimal_colab.ipynb) |
| `SHine-K_full70_colab.ipynb` | **Full URFD run — 30 fall + 40 ADL sequences**, deployed thresholds (sens = 1.0), no re-tuning | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_full70_colab.ipynb) |
| `SHine-K_reproducibility_colab.ipynb` | Early-draft figures, recovery-guide GIFs, post-processing micro-benchmark, and the 8+8-sequence URFD subset run reported in the manuscript. **For the submitted manuscript figures use `gen_figures_colab.ipynb`** (Figs. 1–8); this notebook predates the final figure numbering | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/SHine-K_reproducibility_colab.ipynb) |
| `gen_figures_colab.ipynb` | **Regenerates every figure in the manuscript (Figs. 1–8)** — diagrams (deterministic matplotlib, version-pinned), result plots re-drawn from the archived run data in this repo, and the two prototype screenshots re-captured headlessly (Playwright) from the public demo console | [Open in Colab](https://colab.research.google.com/github/y3korea/SHine-K-/blob/main/gen_figures_colab.ipynb) |

Run everything with **Runtime → Run all**. Each run writes a timestamped `output/run_<id>/` folder
containing `eval_metrics.json`, `eval_per_sequence.csv`, `eval_confusion_matrix.png`, and a
`run_manifest.json` with environment versions and SHA-256 content hashes. (Runs
execute in Colab outside a git checkout, so `git_commit` in the manifest is
`null`; provenance is anchored by the environment record and per-file SHA-256
hashes, and the notebooks themselves are versioned in this repository.)

## Contents

- `SHine-K_full70_sweep_colab.ipynb` — full-70 URFD + keypoint-cache threshold sweep / ablation + GMDCSA-24 cross-dataset run (one click; ships with the executed outputs of the manuscript run)
- `SHine-K_urfd_minimal_colab.ipynb` — minimal 3-cell full-70 reproduction (deps → evaluate → zip)
- `SHine-K_full70_colab.ipynb` — full 70-sequence URFD evaluation (env-var config only; evaluation cell identical to the original notebook)
- `SHine-K_reproducibility_colab.ipynb` — figures · GIFs · latency micro-benchmark · URFD subset evaluation
- `gen_figures.py` — early-draft publication figures (superseded by `gen_figures_ieee.py` / `gen_figures_colab.ipynb`, which match the submitted manuscript's Figs. 1–8)
- `gen_figures_colab.ipynb` — Colab reproduction of **all 8 manuscript figures**: diagrams (Figs. 1–3, deterministic; pixel-identical under the pinned matplotlib), result plots (Figs. 6–8, same code + archived run data), and demo-console screenshots (Figs. 4–5, headless capture; equivalent-capture standard since the console is live)
- `gen_gifs.py` — recovery-exercise animation guides
- `latency_benchmark.js` — post-processing micro-benchmark (simplified REBA + fire pixel-scan; neural inference excluded)
- `output/run_20260627_222419/` — subset run cited in the manuscript (metrics, per-sequence CSV, confusion matrix, logs, manifest)
- `output/run_20260722_195713_full70/` — full-benchmark run cited in the manuscript
- `output/run_20260723_131035/` — threshold sweep + ablation run cited in the manuscript (`sweep_results.csv`, `ablation_results.csv`, sensitivity/operating-point figures)
- `output/run_20260723_135028/` — independent re-run (reproduces the URFD metrics, sweep grid, and ablation byte-for-byte) **plus the GMDCSA-24 cross-dataset evaluation** (`eval_ds2_metrics.json`, per-clip `eval_ds2_per_clip.csv`, executed notebook)

### Manuscript figures (IEEE Access, print-size)

`gen_figures_ieee.py` regenerates the manuscript's diagram figures (Figs. 1-3)
at their final printed width (7.16 in, IEEE Access full text width) so
in-figure text is >= 6.5 pt in print. The prototype screenshots (Figs. 4-5)
are captured from the public demo console in English light-capture mode:

```bash
python3 -m http.server 8765 --directory shine-k-site
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --force-device-scale-factor=2 --window-size=1200,1000   --virtual-time-budget=20000 --screenshot=fig_twin.png   "http://localhost:8765/console.html?demo&light&en#twin"
"$CHROME" --headless=new --force-device-scale-factor=2 --window-size=1200,1000   --virtual-time-budget=9500 --screenshot=fig_live.png   "http://localhost:8765/console.html?autoreplay&light&en#live"
```

## Results (measured)

| Run | Sequences | Precision | Recall | F1 | Accuracy | Median latency |
|---|---|---|---|---|---|---|
| `run_20260722_195713_full70` — **full benchmark** | 30 fall + 40 ADL (URFD) | 0.61 | 0.77 (23/30) | 0.68 | 0.69 | 57 frames ≈ 1.9 s |
| `run_20260627_222419` — standing-fall subset | 8 fall + 8 ADL (URFD) | 0.73 | 1.00 (8/8) | 0.84 | 0.81 | 99.5 frames ≈ 3.3 s |
| `run_20260723_135028` — **GMDCSA-24 cross-dataset, no re-tuning** | 79 fall + 81 ADL | 0.66 | 1.00 (79/79) | 0.80 | 0.75 | — (not recorded) |

**Threshold sweep + ablation** (`run_20260723_131035`, reproduced byte-for-byte by
`run_20260723_135028`): across the 7 × 5 grid F1 spans 0.586–0.686 and the deployed setting
(52°, 700 ms) is within one point of the grid maximum; 700 ms is the F1 optimum along the
window axis; removing the confirmation window recovers **all** missed falls (recall 1.00) but
nearly doubles false alarms (15 → 28).

Failure modes on the full URFD run are structured (per-frame diagnostics): missed falls crossed the
posture thresholds only transiently without sustaining the 700 ms confirmation window; false alarms
split into sustained deep-bending vs deliberate lying-down classes. On GMDCSA-24 — whose ADL set
deliberately contains fall-like activities (lying down to sleep, push-ups) — every fall is detected and
the false alarms land exactly on those deliberate horizontal postures (per-clip CSV in the run folder).
All run folders under `output/` carry full per-sequence/per-clip CSVs and manifests.

## Data

The [UR Fall Detection dataset (URFD)](https://fenix.ur.edu.pl/~mkepski/ds/uf.html) is publicly
available; the notebooks download the cam0 RGB sequences directly.
The [GMDCSA-24 dataset](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos)
(Alam et al., *Data in Brief* 57:110892, 2024) is available under CC BY 4.0; the sweep notebook
auto-downloads the pinned version 2.0 archive (79 fall + 81 ADL clips) from
[Zenodo DOI 10.5281/zenodo.12921216](https://zenodo.org/records/12921216). No new human-subject
data were collected for this evaluation.

## Honest-staging note

Measured results are: the URFD and GMDCSA-24 fall-detection evaluations, the threshold
sweep / component ablation, the in-browser edge benchmark (`bench.html` on the
[demo site](https://y3korea.github.io/shine-k/bench.html)), and the post-processing
micro-benchmark. Emergency 119/e-Gen linkage, radar/thermal sensing, the agent harness, and all
business metrics are design targets, as stated in the manuscript (Table 2).

## Funding

This research was supported by the ANCHOR program through the Gyeongbuk ANCHOR Center, funded by
the Ministry of Education (MOE) and Gyeongsangbuk-do, Republic of Korea (2026-ANCHOR-15-102).

## License

MIT — see [LICENSE](LICENSE).
