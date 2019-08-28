import matplotlib.pyplot as plt
import numpy as np

from . subplot import memory_trace, n_learnt, n_seen, success
from . tools.generic import save_fig


def summary(
        p_recall, seen, successes,
        font_size=10, label_size=8, line_width=1,
        normalize=True,
        extension='',
        window=np.inf
):

    n_rows, n_cols = 5, 1

    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(6, 14))

    ax1 = axes[0]
    memory_trace.summarize(
        p_recall=p_recall,
        normalize=normalize,
        ax=ax1,
        font_size=font_size,
        label_size=label_size,
        line_width=line_width,
    )

    ax2 = axes[1]
    memory_trace.summarize_over_seen(
        p_recall=p_recall,
        seen=seen,
        ax=ax2,
        font_size=font_size,
        label_size=label_size,
        line_width=line_width
    )

    ax3 = axes[2]
    n_learnt.curve(
        p_recall=p_recall,
        normalize=normalize,
        ax=ax3,
        font_size=font_size,
        label_size=label_size,
        line_width=line_width
    )

    ax4 = axes[3]
    n_seen.curve(
        seen=seen,
        normalize=normalize,
        ax=ax4,
        font_size=font_size,
        label_size=label_size,
        line_width=line_width * 2
    )

    ax5 = axes[4]
    success.curve(
        successes=successes,
        ax=ax5,
        font_size=font_size,
        label_size=label_size,
        line_width=line_width * 2,
        window=window
    )

    save_fig(f"simulation{extension}.pdf")