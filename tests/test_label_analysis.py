from unittest.mock import patch
import pandas as pd
from label_analysis import LabelAnalysis
from model import Issue, Event
import matplotlib
matplotlib.use("Agg")


@patch("config.get_parameter")
@patch("label_analysis.DataLoader")
def test_run(mock_data_loader, mock_get_parameter):
    """
    Test the main `run` method of the LabelAnalysis class.
    """
    mock_get_parameter.return_value = "bug"
    mock_issue = Issue({
        "url": "http://example.com",
        "creator": "creator_user",
        "labels": ["bug", "enhancement"],
        "state": "open",
        "assignees": ["user1"],
        "title": "Sample issue",
        "text": "Sample issue description",
        "number": 1,
        "created_date": "2023-01-01T00:00:00Z",
        "updated_date": "2023-02-01T00:00:00Z",
        "events": [
            {
                "event_type": "labeled",
                "author": "user1",
                "event_date": "2023-01-15T00:00:00Z",
                "label": "bug",
                "comment": "Added bug label",
            },
            {
                "event_type": "labeled",
                "author": "user2",
                "event_date": "2023-02-20T00:00:00Z",
                "label": "bug",
                "comment": "Added bug label",
            },
        ],
    })
    mock_data_loader.return_value.get_issues.return_value = [mock_issue]
    with patch.object(LabelAnalysis, "_plot_bar_chart") as mock_plot_chart:
        analysis = LabelAnalysis()
        analysis.run()
        mock_get_parameter.assert_called_with("label")
        mock_data_loader.return_value.get_issues.assert_called_once()
        assert mock_plot_chart.called
        plot_data = mock_plot_chart.call_args[0][0]
        assert isinstance(plot_data, pd.DataFrame)
        assert "User" in plot_data.columns
        assert "Interactions" in plot_data.columns


@patch("config.get_parameter", return_value="bug")
@patch("matplotlib.pyplot.show")
def test_plot_bar_chart(mock_show, mock_get_parameter):
    """
    Test the `_plot_bar_chart` method of the LabelAnalysis class.
    """
    mock_data = pd.DataFrame({
        "User": ["user1", "user2"],
        "Interactions": [5, 3]
    })
    analysis = LabelAnalysis()
    analysis._plot_bar_chart(mock_data)
    mock_show.assert_called_once()
