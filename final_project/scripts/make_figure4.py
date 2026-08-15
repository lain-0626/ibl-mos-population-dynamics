"""
make_figure4.py

Generate Figure 4:
Temporal emergence of contrast-dependent MOs population separation.

Panels
------
A. Fraction of sessions with permutation-defined separation onset
B. Cumulative fraction of sessions reaching separation-onset criterion
C. Subject-level time-resolved contrast slope with cluster permutation

Important
---------
Panels A-B are descriptive session-level analyses (n = 22 sessions).

Panel C is the primary subject-level timing inference
(n = 18 subjects) and is imported directly from the
analysis-notebook output.

No neural analysis or statistical inference is recomputed here.
"""

# ============================================================
# 1. Imports
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 2. Paths
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent


TABLE_DIR = Path(
    r"D:\Ephys_analysis\ibl-population-dynamics"
    r"\results\cross_session_MOs\tables"
)


SUMMARY_FIGURE_DIR = Path(
    r"D:\Ephys_analysis\ibl-population-dynamics"
    r"\results\cross_session_MOs\summary_figures"
)


OUTPUT_DIR = (
    PROJECT_DIR
    / "figures"
    / "figure4"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ONSET_SUMMARY_PATH = (
    TABLE_DIR
    / "cross_session_onset_summary.csv"
)


TIMING_PANEL_PATH = (
    SUMMARY_FIGURE_DIR
    / "05_time_resolved_contrast_slope_cluster_permutation.png"
)


# ============================================================
# 3. Frozen analysis parameters
# ============================================================

ANALYSIS_CONTRASTS = [
    6.25,
    12.5,
    25.0,
    100.0,
]

ONSET_END_S = 0.8

BIN_SIZE_S = 0.020

N_SESSIONS = 22

N_SUBJECTS = 18


# ============================================================
# 4. Plot style
# ============================================================

plt.rcParams["font.family"] = [
    "Arial",
    "DejaVu Sans",
]

plt.rcParams["font.size"] = 9

plt.rcParams["axes.linewidth"] = 0.8

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


TEXT_COLOR = "#222222"
MUTED_TEXT = "#666666"
LIGHT_GRAY = "#C7CBD1"


# Same contrast palette used in the other figures
contrast_colors = plt.cm.viridis(
    np.linspace(
        0.18,
        0.88,
        len(ANALYSIS_CONTRASTS),
    )
)


CONTRAST_COLOR_MAP = dict(
    zip(
        ANALYSIS_CONTRASTS,
        contrast_colors,
    )
)


# ============================================================
# 5. Load onset summary
# ============================================================

onset_df = pd.read_csv(
    ONSET_SUMMARY_PATH
)


# Make sure important columns have the expected type
onset_df["contrast"] = pd.to_numeric(
    onset_df["contrast"],
    errors="coerce",
)


onset_df["onset_latency_s"] = pd.to_numeric(
    onset_df["onset_latency_s"],
    errors="coerce",
)


# Robust conversion in case CSV stores True/False as text
if onset_df["onset_detected"].dtype == object:

    onset_df["onset_detected"] = (
        onset_df["onset_detected"]
        .astype(str)
        .str.lower()
        .map(
            {
                "true": True,
                "false": False,
            }
        )
    )


# ============================================================
# 6. QC
# ============================================================

print(
    "Sessions:",
    onset_df[
        "session"
    ].nunique()
)

print(
    "Subjects:",
    onset_df[
        "subject"
    ].nunique()
)

print(
    "Rows:",
    len(
        onset_df
    )
)


assert (
    onset_df[
        "session"
    ].nunique()
    ==
    N_SESSIONS
)


assert set(
    onset_df[
        "contrast"
    ].unique()
) == set(
    ANALYSIS_CONTRASTS
)


if not TIMING_PANEL_PATH.exists():

    raise FileNotFoundError(
        f"Cannot find timing panel:\n"
        f"{TIMING_PANEL_PATH}"
    )


# ============================================================
# 7. Helper functions
# ============================================================

def add_panel_label(
    ax,
    label,
    x=-0.10,
    y=1.06,
):

    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        ha="left",
        va="top",
        color=TEXT_COLOR,
    )


def clean_axis(
    ax,
):

    ax.spines[
        "top"
    ].set_visible(
        False
    )

    ax.spines[
        "right"
    ].set_visible(
        False
    )

    ax.tick_params(
        direction="out",
        length=3,
        width=0.8,
    )


# ============================================================
# 8. Panel A data:
#    detection fraction by contrast
# ============================================================

detection_summary_df = (
    onset_df
    .groupby(
        "contrast",
        as_index=False,
    )
    .agg(
        n_sessions=(
            "session",
            "nunique",
        ),

        n_detected=(
            "onset_detected",
            "sum",
        ),
    )
)


detection_summary_df[
    "detection_fraction"
] = (
    detection_summary_df[
        "n_detected"
    ]
    /
    detection_summary_df[
        "n_sessions"
    ]
)


detection_summary_df = (
    detection_summary_df
    .set_index(
        "contrast"
    )
    .reindex(
        ANALYSIS_CONTRASTS
    )
    .reset_index()
)


print(
    "\nDetection summary:"
)

print(
    detection_summary_df
)


# ============================================================
# 9. Panel B data:
#    cumulative onset curves
# ============================================================

ONSET_TIME_GRID_S = np.arange(
    0.0,
    ONSET_END_S
    +
    BIN_SIZE_S / 2,
    BIN_SIZE_S,
)


cumulative_rows = []


for contrast in ANALYSIS_CONTRASTS:

    contrast_df = (
        onset_df.loc[
            np.isclose(
                onset_df[
                    "contrast"
                ],
                contrast,
            )
        ]
        .copy()
    )


    onset_times = (
        contrast_df[
            "onset_latency_s"
        ]
        .to_numpy(
            dtype=float
        )
    )


    n_sessions = (
        contrast_df[
            "session"
        ]
        .nunique()
    )


    for time_s in ONSET_TIME_GRID_S:

        # NaN <= time_s evaluates False.
        #
        # Therefore sessions without a detected onset
        # never enter the cumulative count.
        n_reached = int(
            np.sum(
                onset_times
                <=
                time_s
            )
        )


        cumulative_rows.append(
            {
                "contrast":
                    contrast,

                "time_s":
                    time_s,

                "n_sessions":
                    n_sessions,

                "n_reached":
                    n_reached,

                "fraction_reached":
                    n_reached
                    /
                    n_sessions,
            }
        )


cumulative_onset_df = pd.DataFrame(
    cumulative_rows
)


# ============================================================
# 10. Build Figure 4
# ============================================================

fig = plt.figure(
    figsize=(
        10,
        8.2,
    ),
    facecolor="white",
)


grid = fig.add_gridspec(
    nrows=2,
    ncols=2,
    height_ratios=[
        1.0,
        1.35,
    ],
    left=0.09,
    right=0.97,
    bottom=0.07,
    top=0.96,
    wspace=0.30,
    hspace=0.32,
)


ax_a = fig.add_subplot(
    grid[
        0,
        0,
    ]
)


ax_b = fig.add_subplot(
    grid[
        0,
        1,
    ]
)


ax_c = fig.add_subplot(
    grid[
        1,
        :,
    ]
)


# ============================================================
# 11. Panel A:
#     onset detection fraction
# ============================================================

x_values = (
    detection_summary_df[
        "contrast"
    ]
    .to_numpy(
        dtype=float
    )
)


y_values = (
    detection_summary_df[
        "detection_fraction"
    ]
    .to_numpy(
        dtype=float
    )
)


# Connecting line
ax_a.plot(
    x_values,
    y_values,
    linewidth=1.8,
    color=TEXT_COLOR,
    zorder=2,
)


# Contrast-colored points
for _, row in (
    detection_summary_df.iterrows()
):

    contrast = float(
        row[
            "contrast"
        ]
    )


    fraction = float(
        row[
            "detection_fraction"
        ]
    )


    n_detected = int(
        row[
            "n_detected"
        ]
    )


    n_sessions = int(
        row[
            "n_sessions"
        ]
    )


    ax_a.scatter(
        contrast,
        fraction,
        s=55,
        color=CONTRAST_COLOR_MAP[
            contrast
        ],
        zorder=3,
    )


    ax_a.text(
        contrast,
        fraction + 0.055,
        f"{n_detected}/{n_sessions}",
        ha="center",
        va="bottom",
        fontsize=8,
        color=TEXT_COLOR,
    )


ax_a.set_xscale(
    "log",
    base=2,
)


ax_a.set_xticks(
    ANALYSIS_CONTRASTS
)


ax_a.set_xticklabels(
    [
        f"{contrast:g}"
        for contrast
        in ANALYSIS_CONTRASTS
    ]
)


ax_a.set_ylim(
    0,
    1.0,
)


ax_a.set_xlabel(
    "Visual contrast (%)"
)


ax_a.set_ylabel(
    "Fraction of sessions\n"
    "with detected onset"
)


ax_a.set_title(
    "Reliable separation is more frequently detected",
    fontsize=10,
    fontweight="bold",
)


ax_a.text(
    0.03,
    0.04,
    "n = 22 sessions",
    transform=ax_a.transAxes,
    fontsize=8,
    color=MUTED_TEXT,
    ha="left",
    va="bottom",
)


clean_axis(
    ax_a
)


add_panel_label(
    ax_a,
    "A",
)


# ============================================================
# 12. Panel B:
#     cumulative onset curves
# ============================================================

for contrast in ANALYSIS_CONTRASTS:

    plot_df = (
        cumulative_onset_df.loc[
            np.isclose(
                cumulative_onset_df[
                    "contrast"
                ],
                contrast,
            )
        ]
        .sort_values(
            "time_s"
        )
    )


    ax_b.step(
        plot_df[
            "time_s"
        ],
        plot_df[
            "fraction_reached"
        ],
        where="post",
        linewidth=2.0,
        color=CONTRAST_COLOR_MAP[
            contrast
        ],
        label=f"{contrast:g}%",
    )


ax_b.set_xlim(
    0,
    ONSET_END_S,
)


ax_b.set_ylim(
    0,
    1.0,
)


ax_b.set_xlabel(
    "Time from stimulus onset (s)"
)


ax_b.set_ylabel(
    "Cumulative fraction of sessions\n"
    "meeting onset criterion"
)


ax_b.set_title(
    "Cumulative separation-onset detection",
    fontsize=10,
    fontweight="bold",
)


ax_b.legend(
    title="Contrast",
    frameon=False,
    fontsize=8,
    title_fontsize=8.5,
    loc="upper left",
)


ax_b.text(
    0.97,
    0.04,
    "n = 22 sessions",
    transform=ax_b.transAxes,
    fontsize=8,
    color=MUTED_TEXT,
    ha="right",
    va="bottom",
)


clean_axis(
    ax_b
)


add_panel_label(
    ax_b,
    "B",
)


# ============================================================
# 13. Panel C:
#     existing notebook-generated primary timing result
# ============================================================

timing_img = plt.imread(
    TIMING_PANEL_PATH
)


ax_c.imshow(
    timing_img
)


ax_c.axis(
    "off"
)


add_panel_label(
    ax_c,
    "C",
    x=-0.035,
    y=1.02,
)


ax_c.text(
    0.99,
    -0.015,
    "Primary timing inference: n = 18 subjects",
    transform=ax_c.transAxes,
    fontsize=8,
    color=MUTED_TEXT,
    ha="right",
    va="top",
)


# ============================================================
# 14. Save
# ============================================================

png_path = (
    OUTPUT_DIR
    / "Figure4_temporal_emergence.png"
)


pdf_path = (
    OUTPUT_DIR
    / "Figure4_temporal_emergence.pdf"
)


svg_path = (
    OUTPUT_DIR
    / "Figure4_temporal_emergence.svg"
)


fig.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight",
    facecolor="white",
)


fig.savefig(
    pdf_path,
    bbox_inches="tight",
    facecolor="white",
)


fig.savefig(
    svg_path,
    bbox_inches="tight",
    facecolor="white",
)


print(
    "\nSaved:"
)

print(
    png_path
)

print(
    pdf_path
)

print(
    svg_path
)


plt.show()