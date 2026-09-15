"""Reusable plotting functions for exploratory data analysis."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_top_categories(df, category, top_n=20):
    """Plot the top categories of a categorical variable by unique game title count.

    Missing categories and missing titles are excluded from counts.
    Returns (top_counts, ax).
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    missing = {category, "title"} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    counts = (
        df.groupby(category, observed=True, dropna=True)["title"]
        .nunique()
        .sort_values(ascending=False)
    )

    if counts.empty or counts.sum() == 0:
        raise ValueError("No valid titles to count for this category.")

    top_counts = counts.head(top_n)
    n_shown = len(top_counts)

    fig, ax = plt.subplots(figsize=(13, 3.5))

    sns.barplot(
        x=top_counts.index,
        y=top_counts.values,
        hue=top_counts.index,
        order=top_counts.index,
        palette="mako_r",
        edgecolor="black",
        alpha=0.6,
        legend=False,
        ax=ax,
    )
    sns.despine(ax=ax)
    ax.tick_params(axis="x", labelrotation=90)
    ax.set(
        title=f"Top {n_shown} categories in {category} by title count",
        xlabel=category,
        ylabel="Unique titles",
    )
    # fig.tight_layout()
    plt.show()

    percentage = top_counts.sum() / counts.sum() * 100
    print(
        f"\nThe top {n_shown} categories in {category} "
        f"(out of {df[category].nunique()}) account for "
        f"{percentage:.2f}% of games with a non-missing {category}."
    )

    # return top_counts, ax
