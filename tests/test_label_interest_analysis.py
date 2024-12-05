from unittest.mock import patch
import pandas as pd
from label_interest_analysis import LabelInterestAnalysis
from model import Issue, Event


@patch("label_interest_analysis.DataLoader")
def test_run(mock_data_loader):
    """
    Test the main `run` method of the LabelInterestAnalysis class.
    """
    mock_event_1 = Event(None)
    mock_event_1.event_type = "labeled"
    mock_event_1.author = "user1"
    mock_event_1.event_date = "2023-01-15T00:00:00Z"
    mock_event_1.label = "bug"
    mock_event_1.comment = "Bug added"

    mock_event_2 = Event(None)
    mock_event_2.event_type = "labeled"
    mock_event_2.author = "user2"
    mock_event_2.event_date = "2023-02-20T00:00:00Z"
    mock_event_2.label = "enhancement"
    mock_event_2.comment = "Enhancement added"

    mock_issue_1 = Issue(None)
    mock_issue_1.labels = ["bug"]
    mock_issue_1.events = [mock_event_1]

    mock_issue_2 = Issue(None)
    mock_issue_2.labels = ["enhancement"]
    mock_issue_2.events = [mock_event_2]
    mock_data_loader.return_value.get_issues.return_value = [mock_issue_1, mock_issue_2]
    with patch.object(LabelInterestAnalysis, "_plot_interactive_bar_chart") as mock_plot_chart:
        analysis = LabelInterestAnalysis()
        analysis.run()
        assert mock_plot_chart.called
        plot_data = mock_plot_chart.call_args[0][0]
        assert isinstance(plot_data, pd.DataFrame)
        assert "Year" in plot_data.columns
        assert "Label" in plot_data.columns
        assert "Percentage" in plot_data.columns
        percentages = plot_data[plot_data["Label"] == "bug"]["Percentage"].values
        assert len(percentages) == 1
        assert round(percentages[0], 1) == 50.0 


@patch("plotly.graph_objects.Figure.show")
@patch("plotly.graph_objects.Figure.write_html")
def test_plot_interactive_bar_chart(mock_write_html, mock_show):
    """
    Test the `_plot_interactive_bar_chart` method of the LabelInterestAnalysis class.
    """
    mock_data = pd.DataFrame({
        "Year": [2023, 2023],
        "Label": ["bug", "enhancement"],
        "Percentage": [50.0, 50.0],
    })
    analysis = LabelInterestAnalysis()
    analysis._plot_interactive_bar_chart(mock_data)
    mock_write_html.assert_called_once_with("interactive_bar_chart.html", auto_open=True)
    mock_show.assert_called_once()


def test_no_data():
    """
    Test the behavior when no data is available.
    """
    with patch("label_interest_analysis.DataLoader") as mock_data_loader:
        mock_data_loader.return_value.get_issues.return_value = []

        with patch.object(LabelInterestAnalysis, "_plot_interactive_bar_chart") as mock_plot_chart:
            analysis = LabelInterestAnalysis()
            analysis.run()
            mock_plot_chart.assert_not_called()
