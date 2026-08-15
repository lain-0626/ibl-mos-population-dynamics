from pathlib import Path

import matplotlib.pyplot as plt


# ============================================================
# 1. Input paths
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

RESULTS_DIR = Path(
    r"D:\Ephys_analysis\ibl-population-dynamics\results\figures\Secondary_motor_area_4d8c7767"
)


RASTER_PATH = (
    RESULTS_DIR
    / "raster.png"
)

HEATMAP_PATH = (
    RESULTS_DIR
    / "heatmap_100pct_left_right.png"
)

PCA_PATH = (
    RESULTS_DIR
    / "PCA_all_contrasts_population_trajectories.png"
)

RMS_PATH = (
    RESULTS_DIR
    / "stimulus-side_population_separation_all_contrasts.png"
)

# ============================================================
# Output directory
# ============================================================

OUTPUT_DIR = (
    PROJECT_DIR
    / "figures"
    / "figure2"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Save Figure 2
# ============================================================

def save_figure(fig):

    png_path = (
        OUTPUT_DIR
        / "Figure2_overview.png"
    )

    pdf_path = (
        OUTPUT_DIR
        / "Figure2_overview.pdf"
    )

    svg_path = (
        OUTPUT_DIR
        / "Figure2_overview.svg"
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


    print("Saved:")
    print(png_path)
    print(pdf_path)
    print(svg_path)
# ============================================================
# 2. Read images
# ============================================================

raster_img = plt.imread(
    RASTER_PATH
)

heatmap_img = plt.imread(
    HEATMAP_PATH
)

pca_img = plt.imread(
    PCA_PATH
)

rms_img = plt.imread(
    RMS_PATH
)


# ============================================================
# 3. Create Figure 2 layout
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(10, 8),
)


# ============================================================
# 4. Place existing results
# ============================================================

axes[0, 0].imshow(
    raster_img
)

axes[0, 1].imshow(
    heatmap_img
)

axes[1, 0].imshow(
    pca_img
)

axes[1, 1].imshow(
    rms_img
)


# ============================================================
# 5. Remove axes around imported images
# ============================================================

for ax in axes.flat:

    ax.axis(
        "off"
    )


# ============================================================
# 6. Panel labels
# ============================================================

panel_labels = [
    "A",
    "B",
    "C",
    "D",
]


for ax, label in zip(
    axes.flat,
    panel_labels,
):

    ax.text(
        -0.03,
        1.03,
        label,
        transform=ax.transAxes,
        fontsize=16,
        fontweight="bold",
        ha="left",
        va="top",
    )


# ============================================================
# 7. Layout
# ============================================================

plt.tight_layout()

save_figure(fig)

plt.show()