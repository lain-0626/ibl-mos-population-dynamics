# Visual contrast scales the magnitude and temporal emergence of stimulus-side-associated population dynamics in mouse MOs

## Overview

How does visual evidence strength shape population-level neural dynamics in secondary motor cortex (MOs)?

Using publicly available electrophysiology data from the International Brain Laboratory (IBL), this project examines whether visual contrast modulates stimulus-side-associated population activity in MOs. Across subjects, stronger visual contrast was associated with larger population excursions, greater separation between left- and right-associated population states, and an earlier emergence of contrast-dependent separation.

The analysis progresses from session and unit quality control, through single-session population dynamics, to cross-subject statistical inference.

## Analysis framework

![Analysis framework](final_project/figures/figure1/Figure1_overview.png)

## Dataset and cohort selection

This project uses publicly available electrophysiology and behavioral data from the International Brain Laboratory (IBL) Brain-Wide Map dataset, distributed through DANDI dandiset **000409**.

The analysis began with **459 recording sessions from 139 subjects**. Sessions containing recordings from secondary motor cortex (MOs) were identified using the anatomical region labels provided in the dataset, yielding **55 MOs sessions from 36 subjects**.

To ensure sufficient neural and behavioral sampling for population-level analyses, sessions were required to contain:

- at least **20 high-quality MOs units** (`ibl_quality_score == 1.0`);
- at least **10 valid trials per stimulus-side × contrast condition**;
- valid behavioral timing information;
- reaction times between **0.08 and 2.0 s**.

Visible-stimulus trials were grouped by **stimulus side** (`gabor_stimulus_side`) rather than behavioral choice. The main analysis included four non-zero visual contrast levels:

**6.25%, 12.5%, 25%, and 100%.**

After quality-control and sampling criteria were applied, the final cross-session dataset contained **22 MOs sessions from 18 subjects**.

Importantly, repeated sessions from the same animal were averaged within subject before cross-subject statistical inference, so the primary inferential unit was the **subject**, not the recording session.
The session-screening workflow is documented in:

- [`01_session_inventory.ipynb`](notebooks/01_session_inventory.ipynb)
- [`02_global_session_region_inventory.ipynb`](notebooks/02_global_session_region_inventory.ipynb)
- [`03_select_candidate_sessions.ipynb`](notebooks/03_select_candidate_sessions.ipynb)

## Representative population dynamics in MOs

To establish the population-level analysis framework, a representative MOs session was examined at progressively higher levels of organization, from individual spikes to high-dimensional population dynamics.

![Representative MOs population dynamics](final_project/figures/figure2/Figure2_overview.png)

**A. Single-unit activity.**  
Stimulus-aligned raster plots and peri-stimulus time histograms (PSTHs) illustrate trial-by-trial and average firing responses of individual MOs neurons.

**B. Population activity.**  
Neurons were combined into a population activity matrix to visualize the temporal structure of stimulus-associated responses across the recorded MOs population.

**C. Population trajectories.**  
Population states from all stimulus-side × contrast conditions were projected into a shared principal-component space. A single PCA basis was used for all conditions within the session, allowing their trajectories to be visualized in the same low-dimensional coordinate system.

**D. Full-dimensional stimulus-side separation.**  
Formal left–right population separation was quantified in the full neuron-dimensional space using the root-mean-square (RMS) distance between the left- and right-associated population states at each time point. PCA was therefore used for visualization rather than as the primary quantitative measure of separation.

Together, these analyses show that MOs activity can be represented as a time-evolving population state whose stimulus-side-associated separation varies with visual contrast.
The representative single-session analyses are documented in:

- [`05a_single_session_population_dynamics_VISp.ipynb`](notebooks/05a_single_session_population_dynamics_VISp.ipynb)
- [`05b_single_session_population_dynamics_MOs.ipynb`](notebooks/05b_single_session_population_dynamics_MOs.ipynb)

## Cross-subject magnitude effects

The single-session observations were next tested across the full MOs cohort. Repeated recording sessions from the same animal were first averaged within subject, yielding **18 subjects** for cross-subject inference.

![Cross-subject magnitude effects](final_project/figures/figure3/Figure3_cross_subject_magnitude.png)

### Population excursion increases with visual contrast

Population excursion quantified how far the evoked population state moved away from its pre-stimulus baseline state. Across subjects, stronger visual contrast produced progressively larger population excursions.

This contrast dependence was significant across the four contrast conditions  
(**Friedman test:** χ² = 46.2, *p* = 5.1 × 10⁻¹⁰; **Kendall's W = 0.86**).

A subject-wise regression against log₂ contrast showed a positive excursion slope in **18/18 subjects**, indicating that the effect was highly consistent across animals.

### Stimulus-side separation increases with visual contrast

The distance between left- and right-associated population states was quantified independently using full-dimensional RMS separation. Stronger visual contrast produced greater left–right population separation across subjects.

The contrast effect was again significant  
(**Friedman test:** χ² = 38.47, *p* = 2.3 × 10⁻⁸; **Kendall's W = 0.71**).

The stimulus-side separation slope was positive in **17/18 subjects**, showing that the increase with contrast was not driven by a small subset of recordings.

Together, these results demonstrate that increasing visual evidence strength is associated with both a larger MOs population response and a greater separation between stimulus-side-associated population states.
The cross-session analysis and subject-level statistics are documented in:

- [`06_cross-session_batch_analysis_MOs.ipynb`](notebooks/06_cross-session_batch_analysis_MOs.ipynb)

## Temporal emergence of contrast-dependent separation

The final analysis asked whether visual contrast affected not only the magnitude of stimulus-side population separation, but also its temporal emergence.

![Temporal emergence of contrast-dependent separation](final_project/figures/figure4/Figure4_temporal_emergence.png)

### Reliable separation is detected more frequently at higher contrast

For each session and contrast condition, stimulus-side separation onset was defined using a permutation-based threshold that controlled the family-wise error rate across the 0–0.8 s post-stimulus window.

The fraction of sessions meeting this predefined onset criterion increased systematically with contrast:

- **6.25%:** 2/22 sessions
- **12.5%:** 7/22 sessions
- **25%:** 13/22 sessions
- **100%:** 16/22 sessions

The cumulative onset curves provide a descriptive view of when sessions first reached this criterion. Importantly, sessions without a detected onset were not assigned an artificial latency; they simply did not contribute to the cumulative detected fraction.

### Contrast-dependent separation emerges rapidly after stimulus onset

Because criterion-based onset detection can fail in individual sessions, the primary timing inference used the complete, unsmoothed stimulus-side separation timecourse from all subjects.

At each time point, separation was regressed against log₂ visual contrast within each subject, producing a time-resolved contrast slope. A one-sided cluster-based sign-flip permutation test was then used to determine when this slope was reliably positive across subjects.

A significant positive contrast effect emerged by approximately **80 ms after stimulus onset** and persisted until approximately **560 ms**  
(**cluster-based permutation test:** *p* = 0.0002).

Thus, stronger visual evidence was associated not only with greater stimulus-side population separation, but also with an earlier emergence of the contrast-dependent population effect.
The temporal analysis is documented in:

- [`06_cross-session_batch_analysis_MOs.ipynb`](notebooks/06_cross-session_batch_analysis_MOs.ipynb)

## Interpretation and limitations

These results show that visual contrast systematically modulates stimulus-side-associated population dynamics in MOs. Stronger visual evidence was associated with larger population excursions, greater left–right population separation, and an earlier emergence of the contrast-dependent separation effect.

Several limitations are important for interpreting these findings.

First, **stimulus side, behavioral choice, and movement are correlated in this task**. Because MOs is strongly involved in action- and decision-related processes, the present analysis cannot determine whether the observed left–right population separation reflects sensory information, decision variables, movement preparation, motor execution, or a combination of these signals. The results should therefore be interpreted as **stimulus-side-associated population dynamics**, rather than as evidence for pure sensory encoding in MOs.

Second, this project was designed as a focused population-level analysis rather than a complete mechanistic dissection of MOs coding. Analyses such as choice-conditioned decoding, error-trial comparisons, movement-matched analyses, or explicit sensory-versus-motor encoding models would be required to separate these correlated variables more directly.

Third, PCA was used only to visualize population trajectories. The formal measure of stimulus-side separation was computed in the full neuron-dimensional space. Consequently, the low-dimensional trajectories should not be interpreted as a complete representation of the underlying neural population activity.

Fourth, recordings from different sessions were not simultaneous and neurons were not matched across sessions. Cross-session inference was therefore performed on session-level population metrics, with repeated sessions averaged within subject before statistical testing, rather than by concatenating neurons across recordings.

Finally, the onset analysis identifies when population separation meets a predefined statistical detection criterion. Failure to detect an onset within the analyzed window does not imply the absence of biological separation, and cluster boundaries should not be interpreted as exact physiological onset times.

Within these constraints, the analysis provides evidence for a robust and reproducible relationship between visual evidence strength and the magnitude and temporal structure of stimulus-side-associated MOs population dynamics.

## Methods summary

### Trial and unit selection

High-quality units were defined as units with `ibl_quality_score == 1.0`.

Trials were required to contain valid stimulus, movement, choice-registration, and feedback timing information. Reaction time was defined as wheel-movement onset minus stimulus onset, and trials with reaction times outside **0.08–2.0 s** were excluded.

The main stimulus-side analysis included four non-zero contrast levels: **6.25%, 12.5%, 25%, and 100%**.

### Spike alignment and population activity

Spike times were aligned to visual stimulus onset and binned at **20 ms** resolution over a window from **−0.5 to 1.0 s** relative to stimulus onset.

Population responses were organized as neuron-dimensional activity vectors evolving over time. For magnitude analyses, activity was baseline-centered using a pre-stimulus interval from **−0.35 to −0.15 s** and normalized on a per-unit basis.

### Population trajectory analysis

Principal component analysis (PCA) was used to visualize population trajectories. All stimulus-side × contrast conditions within a session were projected into a **shared PCA basis**.

PCA was used only for visualization. Formal left-right population separation was quantified in the full neuron-dimensional space using root-mean-square (RMS) distance:

```math
D_{\mathrm{RMS}}(t)
=
\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
\left[L_i(t)-R_i(t)\right]^2
}
```

where $N$ is the number of neurons, and $L_i(t)$ and $R_i(t)$ denote the normalized population activity of neuron $i$ for left- and right-stimulus trials at time $t$.

Population excursion quantified the distance of the evoked population state from its pre-stimulus baseline state.
### Cross-subject statistics

Repeated sessions from the same animal were averaged within subject before inferential statistics.

Contrast effects across the four repeated conditions were tested using the **Friedman test**, with **Kendall's W** reported as an effect-size measure.

For each subject, contrast dependence was additionally summarized by regressing each population metric against `log2(contrast)`. The resulting slope represents the change in the metric associated with each doubling of visual contrast.

### Temporal analysis

Session-level separation onset was defined using a permutation-derived threshold controlling the family-wise error rate over the **0–0.8 s** post-stimulus interval. Onset required at least **three consecutive 20-ms bins** above threshold.

For the primary cross-subject timing analysis, unsmoothed separation timecourses were used. At each time point, stimulus-side separation was regressed against `log2(contrast)` within each subject. The resulting subject-level contrast-slope timecourses were tested using a **one-sided cluster-based sign-flip permutation test** with **5,000 permutations**.

This analysis identified a significant positive contrast-dependent cluster from approximately **80 to 560 ms** after stimulus onset.

## Reproducibility

The analysis workflow is organized as a sequence of Jupyter notebooks, progressing from dataset inventory and session screening to representative single-session analyses and cross-subject inference.

The main analysis notebooks are:

- `01_session_inventory.ipynb`
- `01b_single_session_metadata_prototype.ipynb`
- `02_global_session_region_inventory.ipynb`
- `03_select_candidate_sessions.ipynb`
- `04_extract_prototype_session.ipynb`
- `04b_extract_prototype_session.ipynb`
- `04b_pre_session_search_MOs.ipynb`
- `05a_single_session_population_dynamics_VISp.ipynb`
- `05b_single_session_population_dynamics_MOs.ipynb`
- `06_cross-session_batch_analysis_MOs.ipynb`

Final multi-panel figures are assembled from notebook-generated results using scripts in `final_project/scripts/`.

Raw NWB files are not included in this repository and should be obtained directly from DANDI.

## Repository structure

```text
ibl-population-dynamics/
├── notebooks/          # Analysis notebooks
├── results/            # Intermediate tables and notebook-generated figures
├── final_project/
│   ├── figures/        # Final Figures 1–4
│   └── scripts/        # Scripts for assembling final figures
├── README.md
└── LICENSE
```

## Data availability

This project uses publicly available data from the International Brain Laboratory (IBL) Brain-Wide Map dataset.

- **DANDI Dandiset:** 000409
- **Version:** 0.260309.1324
- **DOI:** 10.48324/dandi.000409/0.260309.1324

The original electrophysiology and behavioral data are hosted by DANDI and are not redistributed in this repository.

## License and attribution

Analysis code in this repository is released under the MIT License.

The underlying IBL/DANDI dataset is distributed under its own data license and should be cited independently when reused.