"""
make_figure1.py

Generate Figure 1 for the IBL MOs population-dynamics project.

Figure 1
--------
A. Behavioral task schematic
B. Dataset/session selection
C. Inclusion and QC criteria
D. Population-analysis workflow

Outputs
-------
final_project/figures/figure1/
    Figure1_overview.png
    Figure1_overview.pdf
    Figure1_overview.svg

Dependencies
------------
numpy
matplotlib
"""

# ============================================================
# 1. Imports
# ============================================================

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import (
    FancyBboxPatch,
    Rectangle,
    Circle,
    Ellipse,
    Arc,
)


# ============================================================
# 2. Project paths
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

OUTPUT_DIR = (
    PROJECT_DIR
    / "figures"
    / "figure1"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# 3. Freeze project-level numbers
#
# Keep important project numbers in ONE place.
# If the final analysis changes later, edit them here only.
# ============================================================

N_ALL_SESSIONS = 459

N_MOS_SESSIONS = 55
N_MOS_SUBJECTS = 36

N_FINAL_SESSIONS = 22
N_FINAL_SUBJECTS = 18

MIN_GOOD_UNITS = 20
MIN_VALID_TRIALS_PER_CONDITION = 10

RT_MIN_S = 0.08
RT_MAX_S = 2.00

ANALYSIS_CONTRASTS = [
    6.25,
    12.5,
    25.0,
    100.0,
]

BIN_SIZE_MS = 20


# ============================================================
# 4. Figure style
# ============================================================

# Arial is common in scientific figures.
# DejaVu Sans acts as a fallback if Arial is unavailable.
plt.rcParams["font.family"] = [
    "Arial",
    "DejaVu Sans",
]

plt.rcParams["font.size"] = 9

plt.rcParams["axes.linewidth"] = 0.8

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


# ------------------------------------------------------------
# Centralized color definitions
# ------------------------------------------------------------

TEXT_COLOR = "#222222"

MUTED_TEXT = "#666666"

EDGE_COLOR = "#555555"

LIGHT_EDGE = "#B8BDC5"

BOX_COLOR = "#F5F6F8"

ACCENT = "#4C78A8"

ACCENT_LIGHT = "#E8F0F7"

WHITE = "#FFFFFF"


# Contrast colors
contrast_colors = plt.cm.viridis(
    np.linspace(
        0.18,
        0.88,
        len(ANALYSIS_CONTRASTS),
    )
)


# ============================================================
# 5. General drawing helper functions
# ============================================================

def setup_panel(ax):
    """
    Use a normalized 0-1 coordinate system.

    This makes schematic drawing much easier:
    x=0 means left edge
    x=1 means right edge
    y=0 means bottom
    y=1 means top
    """

    ax.set_xlim(
        0,
        1,
    )

    ax.set_ylim(
        0,
        1,
    )

    ax.axis(
        "off"
    )


def add_panel_label(
    ax,
    label,
):
    """
    Add A/B/C/D panel label.
    """

    ax.text(
        -0.03,
        1.03,
        label,
        fontsize=14,
        fontweight="bold",
        color=TEXT_COLOR,
        va="top",
        ha="left",
        transform=ax.transAxes,
    )


def add_box(
    ax,
    x,
    y,
    width,
    height,
    text,
    facecolor=BOX_COLOR,
    edgecolor=LIGHT_EDGE,
    fontsize=9,
    fontweight="normal",
    text_color=TEXT_COLOR,
    linewidth=1.0,
    rounding=0.025,
):
    """
    Draw a rounded rectangle with centered text.
    """

    patch = FancyBboxPatch(
        (
            x,
            y,
        ),
        width,
        height,
        boxstyle=(
            f"round,pad=0.015,"
            f"rounding_size={rounding}"
        ),
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
    )

    ax.add_patch(
        patch
    )

    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=fontweight,
        color=text_color,
        linespacing=1.25,
    )

    return patch


def add_arrow(
    ax,
    start,
    end,
    color=EDGE_COLOR,
    linewidth=1.2,
    mutation_scale=12,
):
    """
    Draw an arrow between two points.

    start/end:
        tuples like (0.5, 0.8)
    """

    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            linewidth=linewidth,
            mutation_scale=mutation_scale,
            shrinkA=0,
            shrinkB=0,
        ),
    )


# ============================================================
# 6. Panel A helper: abstract IBL task schematic
# ============================================================

def draw_gabor_like_patch(
    ax,
    center_x,
    center_y,
    radius=0.045,
):
    """
    Draw a simple striped circular visual stimulus.

    This is only a schematic representation,
    not an exact experimental Gabor stimulus.
    """

    boundary = Circle(
        (
            center_x,
            center_y,
        ),
        radius,
        facecolor=WHITE,
        edgecolor=EDGE_COLOR,
        linewidth=0.8,
        zorder=3,
    )

    ax.add_patch(
        boundary
    )

    stripe_width = radius * 0.35

    stripe_x = np.arange(
        center_x - radius,
        center_x + radius,
        stripe_width * 2,
    )

    for x_position in stripe_x:

        stripe = Rectangle(
            (
                x_position,
                center_y - radius,
            ),
            stripe_width,
            2 * radius,
            facecolor="#777777",
            edgecolor="none",
            zorder=4,
        )

        stripe.set_clip_path(
            boundary
        )

        ax.add_patch(
            stripe
        )


def draw_screen(
    ax,
    x,
    y,
    width,
    height,
    stimulus_side,
):
    """
    Draw a simple visual display.
    """

    screen = FancyBboxPatch(
        (
            x,
            y,
        ),
        width,
        height,
        boxstyle=(
            "round,pad=0.01,"
            "rounding_size=0.02"
        ),
        facecolor=WHITE,
        edgecolor=EDGE_COLOR,
        linewidth=1.2,
    )

    ax.add_patch(
        screen
    )

    if stimulus_side == "left":

        stimulus_x = (
            x
            +
            width * 0.30
        )

    else:

        stimulus_x = (
            x
            +
            width * 0.70
        )

    stimulus_y = (
        y
        +
        height * 0.55
    )


    draw_gabor_like_patch(
        ax,
        center_x=stimulus_x,
        center_y=stimulus_y,
        radius=0.040,
    )


def draw_mouse_and_wheel(
    ax,
    center_x,
    center_y,
):
    """
    Draw a minimal mouse + wheel schematic using
    matplotlib primitives.

    No external icons are required.
    """

    # Wheel
    wheel = Circle(
        (
            center_x,
            center_y - 0.02,
        ),
        0.085,
        facecolor="none",
        edgecolor=LIGHT_EDGE,
        linewidth=2.0,
    )

    ax.add_patch(
        wheel
    )


    # Body
    body = Ellipse(
        (
            center_x,
            center_y + 0.01,
        ),
        width=0.10,
        height=0.065,
        facecolor="#BBBBBB",
        edgecolor=EDGE_COLOR,
        linewidth=0.8,
        zorder=3,
    )

    ax.add_patch(
        body
    )


    # Head
    head = Circle(
        (
            center_x + 0.055,
            center_y + 0.025,
        ),
        radius=0.027,
        facecolor="#BBBBBB",
        edgecolor=EDGE_COLOR,
        linewidth=0.8,
        zorder=4,
    )

    ax.add_patch(
        head
    )


    # Ear
    ear = Circle(
        (
            center_x + 0.047,
            center_y + 0.050,
        ),
        radius=0.012,
        facecolor="#CCCCCC",
        edgecolor=EDGE_COLOR,
        linewidth=0.7,
        zorder=5,
    )

    ax.add_patch(
        ear
    )


    # Tail
    tail = Arc(
        (
            center_x - 0.075,
            center_y + 0.005,
        ),
        width=0.10,
        height=0.09,
        theta1=70,
        theta2=190,
        edgecolor=EDGE_COLOR,
        linewidth=1.0,
    )

    ax.add_patch(
        tail
    )


# ============================================================
# 7. Panel A
# ============================================================

def draw_panel_a(ax):

    setup_panel(
        ax
    )

    add_panel_label(
        ax,
        "A",
    )


    ax.text(
        0.02,
        0.94,
        "Behavioral task",
        fontsize=11,
        fontweight="bold",
        color=TEXT_COLOR,
        va="top",
    )


    # --------------------------------------------------------
    # Left and right stimulus screens
    # --------------------------------------------------------

    draw_screen(
        ax,
        x=0.05,
        y=0.52,
        width=0.25,
        height=0.25,
        stimulus_side="left",
    )


    draw_screen(
        ax,
        x=0.70,
        y=0.52,
        width=0.25,
        height=0.25,
        stimulus_side="right",
    )


    ax.text(
        0.175,
        0.81,
        "Left stimulus",
        ha="center",
        va="bottom",
        fontsize=8.5,
    )


    ax.text(
        0.825,
        0.81,
        "Right stimulus",
        ha="center",
        va="bottom",
        fontsize=8.5,
    )


    # --------------------------------------------------------
    # Mouse
    # --------------------------------------------------------

    draw_mouse_and_wheel(
        ax,
        center_x=0.50,
        center_y=0.61,
    )


    ax.text(
        0.50,
        0.46,
        "Mouse wheel choice",
        ha="center",
        va="top",
        fontsize=8.5,
        color=MUTED_TEXT,
    )


    # --------------------------------------------------------
    # Contrast levels
    # --------------------------------------------------------

    ax.text(
        0.50,
        0.34,
        "Visual contrast",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
    )


    x_positions = np.linspace(
        0.25,
        0.75,
        len(
            ANALYSIS_CONTRASTS
        ),
    )


    for (
        x_position,
        contrast,
        color,
    ) in zip(
        x_positions,
        ANALYSIS_CONTRASTS,
        contrast_colors,
    ):

        ax.add_patch(
            Circle(
                (
                    x_position,
                    0.23,
                ),
                radius=0.027,
                facecolor=color,
                edgecolor=WHITE,
                linewidth=0.5,
            )
        )


        ax.text(
            x_position,
            0.15,
            f"{contrast:g}%",
            ha="center",
            va="top",
            fontsize=8,
        )


    ax.text(
        0.50,
        0.05,
        "Trials aligned to visual stimulus onset",
        ha="center",
        va="bottom",
        fontsize=8,
        color=MUTED_TEXT,
    )


# ============================================================
# 8. Panel B
# ============================================================

def draw_panel_b(ax):

    setup_panel(
        ax
    )

    add_panel_label(
        ax,
        "B",
    )


    ax.text(
        0.02,
        0.94,
        "Dataset selection",
        fontsize=11,
        fontweight="bold",
        color=TEXT_COLOR,
        va="top",
    )


    # --------------------------------------------------------
    # Funnel level 1
    # --------------------------------------------------------

    add_box(
        ax,
        x=0.08,
        y=0.69,
        width=0.84,
        height=0.15,
        text=(
            "IBL Brain-Wide Map\n"
            f"{N_ALL_SESSIONS} sessions"
        ),
        facecolor=BOX_COLOR,
        fontsize=9.5,
        fontweight="bold",
    )


    add_arrow(
        ax,
        start=(
            0.50,
            0.68,
        ),
        end=(
            0.50,
            0.60,
        ),
    )


    # --------------------------------------------------------
    # Funnel level 2
    # --------------------------------------------------------

    add_box(
        ax,
        x=0.18,
        y=0.44,
        width=0.64,
        height=0.15,
        text=(
            "Sessions containing MOs\n"
            f"{N_MOS_SESSIONS} sessions / "
            f"{N_MOS_SUBJECTS} subjects"
        ),
        facecolor=ACCENT_LIGHT,
        edgecolor=ACCENT,
        fontsize=9.3,
    )


    add_arrow(
        ax,
        start=(
            0.50,
            0.43,
        ),
        end=(
            0.50,
            0.35,
        ),
    )


    # --------------------------------------------------------
    # Funnel level 3
    # --------------------------------------------------------

    add_box(
        ax,
        x=0.28,
        y=0.16,
        width=0.44,
        height=0.18,
        text=(
            "Final MOs dataset\n"
            f"{N_FINAL_SESSIONS} sessions\n"
            f"{N_FINAL_SUBJECTS} subjects"
        ),
        facecolor=ACCENT,
        edgecolor=ACCENT,
        text_color=WHITE,
        fontsize=10,
        fontweight="bold",
    )


    ax.text(
        0.50,
        0.06,
        "Cross-session population analysis",
        ha="center",
        va="bottom",
        fontsize=8,
        color=MUTED_TEXT,
    )


# ============================================================
# 9. Panel C
# ============================================================

def draw_panel_c(ax):

    setup_panel(
        ax
    )

    add_panel_label(
        ax,
        "C",
    )


    ax.text(
        0.02,
        0.94,
        "Inclusion and QC criteria",
        fontsize=11,
        fontweight="bold",
        color=TEXT_COLOR,
        va="top",
    )


    # --------------------------------------------------------
    # Unit QC
    # --------------------------------------------------------

    add_box(
        ax,
        x=0.05,
        y=0.58,
        width=0.42,
        height=0.24,
        text=(
            "UNIT QC\n"
            "IBL quality score = 1\n"
            "Good units only"
        ),
        facecolor=BOX_COLOR,
        fontsize=9,
        fontweight="normal",
    )


    # --------------------------------------------------------
    # Trial QC
    # --------------------------------------------------------

    add_box(
        ax,
        x=0.53,
        y=0.58,
        width=0.42,
        height=0.24,
        text=(
            "TRIAL QC\n"
            "Required timestamps present\n"
            f"RT = {RT_MIN_S:.2f}–{RT_MAX_S:.2f} s"
        ),
        facecolor=BOX_COLOR,
        fontsize=9,
    )


    # --------------------------------------------------------
    # Conditions
    # --------------------------------------------------------

    contrast_text = (
        " / ".join(
            f"{contrast:g}"
            for contrast
            in ANALYSIS_CONTRASTS
        )
    )


    add_box(
        ax,
        x=0.05,
        y=0.25,
        width=0.42,
        height=0.24,
        text=(
            "ANALYSIS CONDITIONS\n"
            f"{contrast_text}% contrast\n"
            "Left and right stimulus sides"
        ),
        facecolor=ACCENT_LIGHT,
        edgecolor=ACCENT,
        fontsize=8.8,
    )


    # --------------------------------------------------------
    # Session inclusion
    # --------------------------------------------------------

    add_box(
        ax,
        x=0.53,
        y=0.25,
        width=0.42,
        height=0.24,
        text=(
            "SESSION INCLUSION\n"
            f"≥ {MIN_GOOD_UNITS} good MOs units\n"
            f"≥ {MIN_VALID_TRIALS_PER_CONDITION} "
            "valid trials / condition"
        ),
        facecolor=ACCENT_LIGHT,
        edgecolor=ACCENT,
        fontsize=8.8,
    )


    ax.text(
        0.50,
        0.08,
        "Criteria were fixed before cross-session inference.",
        ha="center",
        va="center",
        fontsize=8,
        color=MUTED_TEXT,
    )


# ============================================================
# 10. Panel D
# ============================================================

def draw_panel_d(ax):

    setup_panel(
        ax
    )

    add_panel_label(
        ax,
        "D",
    )


    ax.text(
        0.02,
        0.94,
        "Population-analysis workflow",
        fontsize=11,
        fontweight="bold",
        color=TEXT_COLOR,
        va="top",
    )


    # ========================================================
    # Top row
    # ========================================================

    top_y = 0.69

    box_width = 0.19
    box_height = 0.13


    top_x = [
        0.02,
        0.27,
        0.52,
        0.77,
    ]


    top_labels = [
        "Raw spike\ntimes",
        "Stimulus\nalignment",
        f"{BIN_SIZE_MS}-ms\nbinning",
        "Trial × neuron\n× time",
    ]


    for x, text in zip(
        top_x,
        top_labels,
    ):

        add_box(
            ax,
            x=x,
            y=top_y,
            width=box_width,
            height=box_height,
            text=text,
            fontsize=8.5,
        )


    # Top-row arrows
    for index in range(
        len(top_x) - 1
    ):

        add_arrow(
            ax,
            start=(
                top_x[index]
                +
                box_width,
                top_y
                +
                box_height / 2,
            ),
            end=(
                top_x[index + 1]
                -
                0.01,
                top_y
                +
                box_height / 2,
            ),
        )


    # ========================================================
    # Arrow down from population tensor
    # ========================================================

    add_arrow(
        ax,
        start=(
            0.865,
            top_y,
        ),
        end=(
            0.865,
            0.57,
        ),
    )


    # ========================================================
    # Middle row: three analysis branches
    # ========================================================

    branch_y = 0.35

    branch_width = 0.27
    branch_height = 0.18


    branch_x = [
        0.04,
        0.365,
        0.69,
    ]


    branch_labels = [
        (
            "PCA\n"
            "trajectory visualization"
        ),

        (
            "Full-space RMS\n"
            "trajectory separation"
        ),

        (
            "Unsmoothed timing\n"
            "permutation analysis"
        ),
    ]


    for index, (
        x,
        text,
    ) in enumerate(
        zip(
            branch_x,
            branch_labels,
        )
    ):

        if index == 0:

            facecolor = BOX_COLOR
            edgecolor = LIGHT_EDGE

        else:

            facecolor = ACCENT_LIGHT
            edgecolor = ACCENT


        add_box(
            ax,
            x=x,
            y=branch_y,
            width=branch_width,
            height=branch_height,
            text=text,
            facecolor=facecolor,
            edgecolor=edgecolor,
            fontsize=8.5,
        )


    # --------------------------------------------------------
    # Branching arrows
    # --------------------------------------------------------

    branch_source = (
        0.865,
        0.57,
    )


    for x in branch_x:

        target = (
            x
            +
            branch_width / 2,
            branch_y
            +
            branch_height,
        )

        ax.annotate(
            "",
            xy=target,
            xytext=branch_source,
            arrowprops=dict(
                arrowstyle="-|>",
                color=EDGE_COLOR,
                linewidth=1.0,
                mutation_scale=10,
                connectionstyle="arc3,rad=0.08",
            ),
        )


    # ========================================================
    # Final inference box
    # ========================================================

    final_x = 0.27
    final_y = 0.08
    final_width = 0.46
    final_height = 0.14


    add_box(
        ax,
        x=final_x,
        y=final_y,
        width=final_width,
        height=final_height,
        text=(
            "Cross-subject inference\n"
            "Magnitude + temporal emergence"
        ),
        facecolor=ACCENT,
        edgecolor=ACCENT,
        text_color=WHITE,
        fontsize=9,
        fontweight="bold",
    )


    # --------------------------------------------------------
    # Arrows from three branches to final box
    # --------------------------------------------------------

    for x in branch_x:

        start = (
            x
            +
            branch_width / 2,
            branch_y,
        )

        end = (
            final_x
            +
            final_width / 2,
            final_y
            +
            final_height,
        )

        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops=dict(
                arrowstyle="-|>",
                color=EDGE_COLOR,
                linewidth=0.9,
                mutation_scale=9,
                connectionstyle="arc3,rad=0.08",
            ),
        )


# ============================================================
# 11. Build complete Figure 1
# ============================================================

def make_figure():

    fig = plt.figure(
        figsize=(
            10,
            7.2,
        ),
        facecolor=WHITE,
    )


    grid = fig.add_gridspec(
        nrows=2,
        ncols=2,
        left=0.055,
        right=0.975,
        bottom=0.07,
        top=0.965,
        wspace=0.16,
        hspace=0.18,
    )


    ax_a = fig.add_subplot(
        grid[0, 0]
    )

    ax_b = fig.add_subplot(
        grid[0, 1]
    )

    ax_c = fig.add_subplot(
        grid[1, 0]
    )

    ax_d = fig.add_subplot(
        grid[1, 1]
    )


    draw_panel_a(
        ax_a
    )

    draw_panel_b(
        ax_b
    )

    draw_panel_c(
        ax_c
    )

    draw_panel_d(
        ax_d
    )


    # --------------------------------------------------------
    # Small figure-level data-source note
    # --------------------------------------------------------

    fig.text(
        0.975,
        0.018,
        "Data: IBL Brain-Wide Map (DANDI:000409)",
        ha="right",
        va="bottom",
        fontsize=7,
        color=MUTED_TEXT,
    )


    return fig


# ============================================================
# 12. Save outputs
# ============================================================

def save_figure(
    fig,
):

    png_path = (
        OUTPUT_DIR
        /
        "Figure1_overview.png"
    )

    pdf_path = (
        OUTPUT_DIR
        /
        "Figure1_overview.pdf"
    )

    svg_path = (
        OUTPUT_DIR
        /
        "Figure1_overview.svg"
    )


    fig.savefig(
        png_path,
        dpi=300,
        bbox_inches="tight",
        facecolor=WHITE,
    )


    fig.savefig(
        pdf_path,
        bbox_inches="tight",
        facecolor=WHITE,
    )


    fig.savefig(
        svg_path,
        bbox_inches="tight",
        facecolor=WHITE,
    )


    print(
        "Saved:"
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


# ============================================================
# 13. Main
# ============================================================

def main():

    fig = make_figure()

    save_figure(
        fig
    )

    plt.show()


if __name__ == "__main__":

    main()