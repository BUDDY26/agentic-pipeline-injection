"""
scripts/generate_figures.py

Generates publication-quality figures from the corrected post-audit validation results.

Authoritative data source:
    results/validation/multi_run_results.csv
    (corrected post-audit record; supersedes all prior computation passes)

Output directory:
    results/figures/

Figures produced:
    fig_a_propagation_depth.{png,pdf}      — Depth by topology × condition
    fig_b_integrity_by_condition.{png,pdf} — Integrity score by topology × condition
    fig_c_cs_rate.{png,pdf}                — Compromise signal rate by topology × condition
    fig_d_hero_topology_depth.{png,pdf}    — Poster hero: depth by topology (injected only)
    fig_e_score_stability.{png,pdf}        — Per-run integrity score clustering

Run standalone:
    python scripts/generate_figures.py

Design constraints honoured:
  - No invented, smoothed, or resampled values
  - Error bars appear only where score_std > 0 (rag_rank3 and parallel_rank1)
  - depth_std = 0.0 for all configs; no error bars on depth
  - Zero values shown plainly; not forced off-axis
  - Topology colors are consistent across all figures
  - Condition colors are consistent across Figures A-C
  - White background; no dark theme
  - 300 dpi PNG + PDF for poster placement
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')                        # headless — no display required
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

# ─── Paths ────────────────────────────────────────────────────────────────────

ROOT        = Path(__file__).parent.parent
DATA_PATH   = ROOT / 'results' / 'validation' / 'multi_run_results.csv'
OUT_DIR     = ROOT / 'results' / 'figures'

# ─── Topology identity (must match CSV 'topology' column values) ──────────────

TOPOLOGY_ORDER  = ['rag', 'linear', 'parallel']
TOPOLOGY_LABELS = {
    'rag':      'RAG',
    'linear':   'Linear Chain',
    'parallel': 'Parallel Fan-out',
}
# Colorblind-accessible palette (blue / orange / green — ColorBrewer RdYlBu-like)
TOPOLOGY_COLORS = {
    'rag':      '#1565C0',   # blue
    'linear':   '#E65100',   # deep orange
    'parallel': '#2E7D32',   # forest green
}

# ─── Condition identity (must match CSV 'config' column values) ───────────────

CONDITION_ORDER  = ['baseline', 'rank1', 'rank3']
CONDITION_LABELS = {
    'baseline': 'Baseline',
    'rank1':    'Injected Rank-1',
    'rank3':    'Injected Rank-3',
}
# Neutral gray for baseline; pink/magenta scale for injected (no overlap with topology colors)
CONDITION_COLORS = {
    'baseline': '#BDBDBD',
    'rank1':    '#AD1457',   # deep magenta
    'rank3':    '#F48FB1',   # light pink
}

# ─── Matplotlib global style ──────────────────────────────────────────────────

plt.rcParams.update({
    'font.family':         'DejaVu Sans',
    'font.size':           13,
    'axes.titlesize':      14,
    'axes.labelsize':      13,
    'xtick.labelsize':     12,
    'ytick.labelsize':     12,
    'legend.fontsize':     11,
    'legend.framealpha':   0.92,
    'legend.edgecolor':    '#CCCCCC',
    'axes.spines.top':     False,
    'axes.spines.right':   False,
    'axes.grid':           True,
    'axes.grid.axis':      'y',
    'grid.color':          '#E8E8E8',
    'grid.linewidth':      0.8,
    'figure.facecolor':    'white',
    'axes.facecolor':      'white',
    'savefig.dpi':         300,
    'savefig.bbox':        'tight',
    'savefig.facecolor':   'white',
})

BAR_WIDTH  = 0.24          # width of individual bars in grouped charts
LABEL_PAD  = 0.04          # vertical padding for value labels


# ─── Data loading ─────────────────────────────────────────────────────────────

def load_data() -> tuple:
    """
    Load multi_run_results.csv and return (agg_df, runs_df).

    AGG rows (run_id starts with 'AGG_') carry aggregate stats per configuration.
    Per-run rows carry individual run metrics.
    """
    df = pd.read_csv(DATA_PATH)

    agg_mask = df['run_id'].str.startswith('AGG_')
    agg  = df[agg_mask].copy()
    runs = df[~agg_mask].copy()

    # In AGG rows: compromise_signal is stored as float (cs_rate: 0.0 / 0.3333 / 1.0)
    agg['cs_rate'] = agg['compromise_signal'].astype(float)

    # In per-run rows: compromise_signal is 'True' / 'False' string
    runs['cs_bool'] = runs['compromise_signal'].map(
        lambda v: str(v).strip() == 'True'
    )

    # Ensure numeric columns are float
    for col in ['propagation_depth', 'integrity_score', 'score_std']:
        agg[col] = pd.to_numeric(agg[col], errors='coerce').fillna(0.0)
    for col in ['propagation_depth', 'integrity_score']:
        runs[col] = pd.to_numeric(runs[col], errors='coerce').fillna(0.0)

    return agg, runs


# ─── Save helper ──────────────────────────────────────────────────────────────

def save(fig: plt.Figure, stem: str) -> None:
    """Save as PNG (300 dpi) and PDF under results/figures/."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUT_DIR / f'{stem}.png'
    pdf_path = OUT_DIR / f'{stem}.pdf'
    fig.savefig(png_path)
    fig.savefig(pdf_path)
    print(f'  Saved: results/figures/{stem}.png + .pdf')
    plt.close(fig)


# ─── Grouped-bar helper ───────────────────────────────────────────────────────

def _grouped_bar_positions(n_groups: int, n_bars: int, width: float) -> np.ndarray:
    """Return (n_bars, n_groups) matrix of bar centre x-positions."""
    x = np.arange(n_groups, dtype=float)
    offsets = np.linspace(-(n_bars - 1) / 2, (n_bars - 1) / 2, n_bars) * width
    return x[None, :] + offsets[:, None]


# ─── Figure A — Propagation Depth by Topology and Condition ───────────────────

def fig_a_propagation_depth(agg: pd.DataFrame) -> None:
    """
    Grouped bar chart: propagation depth for each topology × condition.

    Key result: topology determines depth; retrieval rank position does not.
    depth_std = 0.0 for all nine configurations — no error bars on any bar.
    Baseline always 0 (control validation); injected depth = pipeline length.
    """
    n_topo = len(TOPOLOGY_ORDER)
    n_cond = len(CONDITION_ORDER)
    positions = _grouped_bar_positions(n_topo, n_cond, BAR_WIDTH)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_axisbelow(True)

    for i, cond in enumerate(CONDITION_ORDER):
        depths = [
            float(agg.loc[
                (agg['topology'] == t) & (agg['config'] == cond),
                'propagation_depth'
            ].values[0])
            for t in TOPOLOGY_ORDER
        ]
        bars = ax.bar(
            positions[i], depths, BAR_WIDTH,
            color=CONDITION_COLORS[cond],
            label=CONDITION_LABELS[cond],
            edgecolor='white', linewidth=0.5,
            zorder=3,
        )
        # Value label on non-zero bars only
        for bar, d in zip(bars, depths):
            if d > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + LABEL_PAD,
                    str(int(d)),
                    ha='center', va='bottom', fontsize=11, fontweight='bold',
                    zorder=4,
                )

    # X-axis: topology labels centred on each group
    group_centres = np.arange(n_topo, dtype=float)
    ax.set_xticks(group_centres)
    ax.set_xticklabels([TOPOLOGY_LABELS[t] for t in TOPOLOGY_ORDER], fontsize=12)
    ax.set_xlabel('Pipeline Topology', fontsize=13)
    ax.set_ylabel('Propagation Depth (hops)', fontsize=13)
    ax.set_title(
        'Injection Propagation Depth by Topology and Corpus Configuration',
        fontsize=14, pad=12,
    )
    ax.set_ylim(0, 5.5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.tick_params(axis='x', bottom=False)

    ax.legend(loc='upper left', title='Corpus Configuration',
              title_fontsize=11)

    fig.tight_layout()
    save(fig, 'fig_a_propagation_depth')


# ─── Figure B — Integrity Score by Topology and Condition ─────────────────────

def fig_b_integrity_by_condition(agg: pd.DataFrame) -> None:
    """
    Grouped bar chart: mean integrity score by topology × condition.

    Error bars appear only for configurations with score_std > 0:
      - rag_rank3    (std = 0.0189)
      - parallel_rank1 (std = 0.0192)
    All other configurations have std = 0.0 and are shown without error bars.

    A dashed reference line at y = 1.0 marks the baseline (perfect integrity).
    """
    n_topo = len(TOPOLOGY_ORDER)
    n_cond = len(CONDITION_ORDER)
    positions = _grouped_bar_positions(n_topo, n_cond, BAR_WIDTH)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_axisbelow(True)

    for i, cond in enumerate(CONDITION_ORDER):
        scores = []
        stds   = []
        for t in TOPOLOGY_ORDER:
            row = agg.loc[(agg['topology'] == t) & (agg['config'] == cond)]
            scores.append(float(row['integrity_score'].values[0]))
            stds.append(float(row['score_std'].values[0]))

        # Only draw error bars where std is genuinely non-zero
        yerr = [s if s > 0 else None for s in stds]
        has_any_err = any(s is not None for s in yerr)

        # Build per-bar error arrays (NaN where no error)
        err_arr = np.array([s if s is not None else np.nan for s in yerr])

        bars = ax.bar(
            positions[i], scores, BAR_WIDTH,
            color=CONDITION_COLORS[cond],
            label=CONDITION_LABELS[cond],
            edgecolor='white', linewidth=0.5,
            zorder=3,
        )
        if has_any_err:
            # Draw error caps only for bars with real std
            for j, (pos, score, err) in enumerate(
                    zip(positions[i], scores, err_arr)):
                if not np.isnan(err):
                    ax.errorbar(
                        pos, score, yerr=err,
                        fmt='none', color='#333333',
                        capsize=4, linewidth=1.2, zorder=5,
                    )

    # Baseline reference line
    ax.axhline(1.0, color='#555555', linewidth=1.0, linestyle='--',
               zorder=2, label='_nolegend_')
    ax.text(0.01, 1.015, 'Baseline = 1.0',
            ha='left', va='bottom', fontsize=10, color='#555555',
            style='italic', transform=ax.get_yaxis_transform())

    group_centres = np.arange(n_topo, dtype=float)
    ax.set_xticks(group_centres)
    ax.set_xticklabels([TOPOLOGY_LABELS[t] for t in TOPOLOGY_ORDER], fontsize=12)
    ax.set_xlabel('Pipeline Topology', fontsize=13)
    ax.set_ylabel(
        'Integrity Score (character-level similarity\nto baseline output, 0 = total divergence)',
        fontsize=12,
    )
    ax.set_title(
        'Output Integrity Score by Topology and Corpus Configuration',
        fontsize=14, pad=12,
    )
    ax.set_ylim(0, 1.15)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
    ax.tick_params(axis='x', bottom=False)

    ax.legend(loc='upper right', title='Corpus Configuration',
              title_fontsize=11)

    # Annotation: error bars present only for configurations with non-zero variance
    fig.text(
        0.5, -0.04,
        'Error bars shown only where score_std > 0 '
        '(rag rank-3: ±0.019; parallel rank-1: ±0.019).',
        ha='center', va='top',
        fontsize=9, color='#666666', style='italic',
        transform=fig.transFigure,
    )

    fig.tight_layout()
    save(fig, 'fig_b_integrity_by_condition')


# ─── Figure C — Compromise Signal Rate by Topology and Condition ──────────────

def fig_c_cs_rate(agg: pd.DataFrame) -> None:
    """
    Grouped bar chart: compromise signal rate (proportion of runs with literal
    artifact match) by topology × injected condition.

    Baseline bars are excluded (cs_rate = 0.0 for all baselines by design;
    this figure focuses on the injected configurations).

    The literal match is a Stage-1 lower bound: cs_rate = 0 does not imply
    no injection influence; integrity scores confirm injection in all cases.
    """
    injected_conditions = ['rank1', 'rank3']
    n_topo = len(TOPOLOGY_ORDER)
    n_cond = len(injected_conditions)
    positions = _grouped_bar_positions(n_topo, n_cond, BAR_WIDTH)

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.set_axisbelow(True)

    for i, cond in enumerate(injected_conditions):
        rates = [
            float(agg.loc[
                (agg['topology'] == t) & (agg['config'] == cond),
                'cs_rate'
            ].values[0])
            for t in TOPOLOGY_ORDER
        ]
        bars = ax.bar(
            positions[i], rates, BAR_WIDTH,
            color=CONDITION_COLORS[cond],
            label=CONDITION_LABELS[cond],
            edgecolor='white', linewidth=0.5,
            zorder=3,
        )
        for bar, r in zip(bars, rates):
            label_y = bar.get_height() + 0.02 if r > 0 else 0.02
            frac = f'{r:.2f}' if r not in (0.0, 1.0) else ('0' if r == 0.0 else '1.0')
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                label_y,
                frac,
                ha='center', va='bottom', fontsize=11, fontweight='bold',
                color='#111111', zorder=4,
            )

    group_centres = np.arange(n_topo, dtype=float)
    ax.set_xticks(group_centres)
    ax.set_xticklabels([TOPOLOGY_LABELS[t] for t in TOPOLOGY_ORDER], fontsize=12)
    ax.set_xlabel('Pipeline Topology', fontsize=13)
    ax.set_ylabel(
        'Compromise Signal Rate\n(fraction of 3 runs with literal INJECTION_CONFIRMED match)',
        fontsize=11.5,
    )
    ax.set_title(
        'Literal Artifact Reproduction Rate by Topology and Corpus Configuration\n'
        '(Stage-1 compromise signal; lower bound on injection influence)',
        fontsize=13, pad=12,
    )
    ax.set_ylim(0, 1.25)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
    ax.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax.tick_params(axis='x', bottom=False)

    ax.legend(loc='upper right', title='Injection Position',
              title_fontsize=11)

    # Note: baseline excluded
    ax.annotate(
        'Baseline not shown (cs_rate = 0.0 for all topologies by construction).',
        xy=(0.02, 0.94), xycoords='axes fraction',
        fontsize=9, color='#666666', style='italic',
    )

    fig.tight_layout()
    save(fig, 'fig_c_cs_rate')


# ─── Figure D — Poster Hero: Propagation Depth by Topology ───────────────────

def fig_d_hero_topology_depth(agg: pd.DataFrame) -> None:
    """
    Poster hero figure: propagation depth for each topology under injection.

    Shows Rank-1 injected results (representative; Rank-3 produces identical depths).
    Uses topology colors rather than condition colors for maximum visual distinctiveness
    at poster-reading distance.

    Optimised for: large text, high contrast, immediate pattern recognition.
    Key message: RAG = 1 hop, Linear Chain = 3 hops, Parallel Fan-out = 4 hops.
    """
    depths = [
        int(agg.loc[
            (agg['topology'] == t) & (agg['config'] == 'rank1'),
            'propagation_depth'
        ].values[0])
        for t in TOPOLOGY_ORDER
    ]
    colors = [TOPOLOGY_COLORS[t] for t in TOPOLOGY_ORDER]
    labels = [TOPOLOGY_LABELS[t] for t in TOPOLOGY_ORDER]

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#E0E0E0', linewidth=1.0, zorder=0)
    ax.set_facecolor('white')

    x = np.arange(len(TOPOLOGY_ORDER))
    bars = ax.bar(x, depths, 0.52, color=colors, edgecolor='white',
                  linewidth=0.5, zorder=3)

    # Large value labels inside/above bars
    for bar, d in zip(bars, depths):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(d),
            ha='center', va='bottom',
            fontsize=28, fontweight='bold', color='#111111',
            zorder=4,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=16)
    ax.set_ylabel('Propagation Depth (pipeline hops)', fontsize=15)
    ax.set_title(
        'Injection Propagates Deeper in More Complex Topologies',
        fontsize=16, pad=14, fontweight='bold',
    )
    ax.set_ylim(0, 5.5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.tick_params(axis='both', labelsize=14)
    ax.tick_params(axis='x', bottom=False)

    # Topology legend patches (for accessibility; color-vision-impaired readers)
    legend_patches = [
        mpatches.Patch(color=TOPOLOGY_COLORS[t], label=TOPOLOGY_LABELS[t])
        for t in TOPOLOGY_ORDER
    ]
    ax.legend(
        handles=legend_patches,
        loc='upper left', fontsize=13,
        title='Topology', title_fontsize=13,
    )

    # Methodology note — placed below the x-axis label area
    fig.text(
        0.5, -0.04,
        'Injected Rank-1 condition shown (Rank-3 produces identical depth). '
        'depth_std = 0.00 across all 3 runs per configuration.',
        ha='center', va='top',
        fontsize=9, color='#666666', style='italic',
        transform=fig.transFigure,
    )

    fig.tight_layout()
    save(fig, 'fig_d_hero_topology_depth')


# ─── Figure E — Per-Run Integrity Score Clustering ───────────────────────────

def fig_e_score_stability(runs: pd.DataFrame) -> None:
    """
    Strip/scatter plot: individual integrity scores for all 27 runs, grouped by
    topology × condition.

    Reveals the clustering pattern produced by temperature=0 execution:
    - Most injected configurations show all 3 runs at a single point (std=0)
    - Two exceptions (rag_rank3, parallel_rank1) show minor spread
    - All baseline runs cluster exactly at 1.0

    This figure supports the reproducibility claim in the validation summary.
    """
    # Build display order: all 9 (topology, condition) pairs in natural order
    pairs = [(t, c) for t in TOPOLOGY_ORDER for c in CONDITION_ORDER]

    # X-axis positions
    x_pos = {pair: i for i, pair in enumerate(pairs)}

    # X-axis tick labels: show topology label on first condition, then indent
    xtick_labels = []
    for t, c in pairs:
        if c == 'baseline':
            xtick_labels.append(f'{TOPOLOGY_LABELS[t]}\n{CONDITION_LABELS[c]}')
        else:
            xtick_labels.append(CONDITION_LABELS[c])

    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.set_axisbelow(True)

    # Vertical separator lines between topology groups
    for sep in [2.5, 5.5]:
        ax.axvline(sep, color='#DDDDDD', linewidth=1.0, linestyle='--', zorder=1)

    # Plot points
    rng = np.random.default_rng(42)
    for (topo, cond), grp in runs.groupby(['topology', 'config']):
        if (topo, cond) not in x_pos:
            continue
        xi = x_pos[(topo, cond)]
        scores = grp['integrity_score'].values
        # Tiny horizontal jitter to separate overlapping dots
        jitter = rng.uniform(-0.08, 0.08, size=len(scores))
        color = TOPOLOGY_COLORS[topo]
        ax.scatter(
            xi + jitter, scores,
            color=color, s=60, alpha=0.85,
            edgecolors='white', linewidths=0.5,
            zorder=4,
        )
        # Mean marker
        ax.scatter(
            xi, np.mean(scores),
            color=color, s=100, marker='D',
            edgecolors='#333333', linewidths=0.8,
            zorder=5,
        )

    # Baseline reference
    ax.axhline(1.0, color='#888888', linewidth=0.8, linestyle=':', zorder=2)

    ax.set_xticks(range(len(pairs)))
    ax.set_xticklabels(xtick_labels, fontsize=9.5, rotation=0, ha='center')
    ax.set_ylabel('Integrity Score', fontsize=13)
    ax.set_title(
        'Per-Run Integrity Score Distribution Across All 27 Validation Runs',
        fontsize=14, pad=12,
    )
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlim(-0.6, len(pairs) - 0.4)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))

    # Topology region labels at top
    for i_group, topo in enumerate(TOPOLOGY_ORDER):
        centre = i_group * 3 + 1     # middle of the 3-condition group
        ax.text(
            centre, 1.1, TOPOLOGY_LABELS[topo],
            ha='center', va='center', fontsize=11, fontweight='bold',
            color=TOPOLOGY_COLORS[topo],
        )

    # Legend: dot = individual run, diamond = mean
    from matplotlib.lines import Line2D
    legend_handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#666666',
               markersize=8, alpha=0.85, label='Individual run'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='#666666',
               markeredgecolor='#333333', markersize=8, label='Mean (3 runs)'),
    ]
    ax.legend(handles=legend_handles, loc='lower right', fontsize=10)

    fig.tight_layout()
    save(fig, 'fig_e_score_stability')


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f'Data source : {DATA_PATH}')
    print(f'Output dir  : {OUT_DIR}')
    print()

    if not DATA_PATH.exists():
        sys.exit(
            f'ERROR: data file not found:\n  {DATA_PATH}\n'
            'Run scripts/recompute_validation_metrics.py first.'
        )

    agg, runs = load_data()

    # Sanity-check: expect 9 AGG rows and 27 per-run rows
    if len(agg) != 9:
        print(f'WARNING: expected 9 AGG rows, found {len(agg)}')
    if len(runs) != 27:
        print(f'WARNING: expected 27 per-run rows, found {len(runs)}')

    print('Generating figures...')
    fig_a_propagation_depth(agg)
    fig_b_integrity_by_condition(agg)
    fig_c_cs_rate(agg)
    fig_d_hero_topology_depth(agg)
    fig_e_score_stability(runs)

    print()
    print('Done. Figures written to results/figures/')


if __name__ == '__main__':
    main()
