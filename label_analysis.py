from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

from data_loader import DataLoader
from model import Issue
import config


class LabelAnalysis:
    """
    Analyzes GitHub issues to display a bar chart showing user interactions for a specific label.
    """

    def __init__(self):
        """
        Constructor
        """
        self.LABEL: str = config.get_parameter("label")

        if not self.LABEL:
            raise ValueError("Please provide a valid label using the --label argument.")

    def run(self):
        """
        Starting point for this analysis.
        """
        issues: List[Issue] = DataLoader().get_issues()
        user_interaction_count = defaultdict(int)

        for issue in issues:
            if self.LABEL in issue.labels:
                creator = issue.creator
                if creator:
                    user_interaction_count[creator] += 1
                for event in issue.events:
                    if event.label == self.LABEL:
                        author = event.author
                        if author:
                            user_interaction_count[author] += 1
        interaction_data = pd.DataFrame(
            user_interaction_count.items(), columns=["User", "Interactions"]
        ).sort_values(by="Interactions", ascending=False)
        interaction_data = interaction_data[interaction_data["Interactions"] > 0]
        if interaction_data.empty:
            print(f"No interactions found for label '{self.LABEL}'.")
            return
        self._plot_bar_chart(interaction_data)

    def _plot_bar_chart(self, interaction_data: pd.DataFrame):
        """
        Plots the bar chart showing user interactions for the specified label with hover functionality.
        """
        top_n = 20
        interaction_data = interaction_data.head(top_n)

        fig, ax = plt.subplots(figsize=(14, 8))
        x_positions = range(len(interaction_data["User"]))
        bars = ax.bar(x_positions, interaction_data["Interactions"], color="skyblue", width=0.5)
        ax.set_title(f"Top {top_n} User Interactions for Label: {self.LABEL}", fontsize=16)
        ax.set_xlabel("User", fontsize=12)
        ax.set_ylabel("Number of Interactions", fontsize=12)
        ax.set_xticks(x_positions)
        ax.set_xticklabels(interaction_data["User"], rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        tooltip = ax.annotate(
            "", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w", ec="b", alpha=0.8),
            arrowprops=dict(arrowstyle="->", color="blue")
        )
        tooltip.set_visible(False)
        def on_hover(event):
            if event.inaxes == ax:
                for bar, value in zip(bars, interaction_data["Interactions"]):
                    if bar.contains(event)[0]:
                        tooltip.set_text(f"{value}")
                        tooltip.xy = (event.xdata, event.ydata)
                        tooltip.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            tooltip.set_visible(False)
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        plt.tight_layout()
        plt.show()
    

if __name__ == "__main__":
    LabelAnalysis().run()
