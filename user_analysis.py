from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import numpy as np

from data_loader import DataLoader
from model import Issue
import config


class UserAnalysis:
    """
    Analyzes GitHub issues to display a line chart showing trends of label usage over time with an interactive legend and hover tooltips.
    """

    def __init__(self):
        """
        Constructor
        """
        self.USER: str = config.get_parameter("user")

    def run(self):
        """
        Main entry point for the analysis.
        """
        issues: List[Issue] = DataLoader().get_issues()
        user_events = [
            e for issue in issues for e in issue.events if e.event_type == "labeled" and (self.USER is None or e.author == self.USER)
        ]
        if not user_events:
            print(f"No events found for user {self.USER}.")
            return
        label_time_data = defaultdict(lambda: defaultdict(int))

        for event in user_events:
            label = event.label
            time = pd.to_datetime(event.event_date).to_period("M")
            label_time_data[label][time] += 1
        line_chart_data = pd.DataFrame(label_time_data).fillna(0).sort_index()
        non_zero_labels = line_chart_data.loc[:, (line_chart_data != 0).any(axis=0)]
        self._plot_line_chart(non_zero_labels)

    def _plot_line_chart(self, line_chart_data: pd.DataFrame):
        """
        Plots the line chart showing trends of label usage over time with an interactive legend and hover tooltips.
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        lines = {}
        for idx, label in enumerate(line_chart_data.columns):
            color = plt.cm.tab20(idx % 20)
            line, = ax.plot(
                line_chart_data.index.to_timestamp(),
                line_chart_data[label],
                label=label,
                color=color,
                visible=False,
                linewidth=2,
                picker=5
            )
            lines[label] = line

        ax.set_title(f"Label Trends Over Time for User {self.USER}", fontsize=16)
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Number of Issues", fontsize=12)
        ax.grid(alpha=0.3)
        legend = ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1), fontsize=10, title="Labels")
        legend.set_draggable(True)
        for text, line in zip(legend.texts, lines.values()):
            text.set_color(line.get_color())
            text.set_alpha(0.3)
        tooltip = ax.annotate(
            "", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        tooltip.set_visible(False)

        import matplotlib.dates as mdates

        def on_hover(event):
            """Handles hover events to display the label and corresponding y-axis value of the closest line."""
            if event.inaxes == ax:
                for label, line in lines.items():
                    if line.get_visible() and line.contains(event)[0]:
                        x_data, y_data = line.get_data()
                        x_data_numeric = mdates.date2num(x_data)
                        mouse_x_numeric = event.xdata
                        closest_index = (np.abs(x_data_numeric - mouse_x_numeric)).argmin()
                        y_value = y_data[closest_index]
                        tooltip.set_text(f"{label}: {y_value:.2f}")
                        tooltip.xy = (event.xdata, event.ydata)
                        tooltip.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            tooltip.set_visible(False)
            fig.canvas.draw_idle()
        fig.canvas.mpl_connect("motion_notify_event", on_hover)
        def toggle_visibility(event):
            if event.artist in legend.texts:
                label = event.artist.get_text()
                line = lines[label]
                visible = not line.get_visible()
                line.set_visible(visible)
                event.artist.set_alpha(1.0 if visible else 0.3)
                plt.draw()
        fig.canvas.mpl_connect("pick_event", toggle_visibility)
        for text in legend.texts:
            text.set_picker(True)
        plt.subplots_adjust(right=0.7)
        plt.show()


if __name__ == "__main__":
    UserAnalysis().run()
