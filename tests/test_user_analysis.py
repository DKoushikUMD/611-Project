from unittest.mock import patch
import pandas as pd
from user_analysis import UserAnalysis
from model import Issue, Event
@patch("config.get_parameter")
@patch("user_analysis.DataLoader")
def test_run(mock_data_loader, mock_get_parameter):
    """
    Test the main `run` method of the UserAnalysis class.
    """
    mock_get_parameter.return_value = "test_user"
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
                "author": "test_user",
                "event_date": "2023-01-15T00:00:00Z",
                "label": "bug",
                "comment": "Added bug label",
            },
            {
                "event_type": "labeled",
                "author": "test_user",
                "event_date": "2023-02-20T00:00:00Z",
                "label": "enhancement",
                "comment": "Added enhancement label",
            },
        ],
    })
    mock_data_loader.return_value.get_issues.return_value = [mock_issue]
    with patch.object(UserAnalysis, "_plot_line_chart") as mock_plot_chart:
        analysis = UserAnalysis()
        analysis.run()
        mock_get_parameter.assert_called_with("user")
        mock_data_loader.return_value.get_issues.assert_called_once()
        assert mock_plot_chart.called
        plot_data = mock_plot_chart.call_args[0][0]
        assert isinstance(plot_data, pd.DataFrame)
        assert "bug" in plot_data.columns
        assert "enhancement" in plot_data.columns

@patch("matplotlib.pyplot.show")
def test_plot_line_chart(mock_show):
    """
    Test the `_plot_line_chart` method of the UserAnalysis class.
    """
    mock_data = pd.DataFrame({
        "bug": [1, 0],
        "enhancement": [0, 2]
    }, index=pd.to_datetime(["2023-01", "2023-02"]).to_period("M"))
    analysis = UserAnalysis()
    analysis._plot_line_chart(mock_data)
    mock_show.assert_called_once()


def test_no_events():
    """
    Test the behavior when no events are present for the user.
    """
    with patch("config.get_parameter", return_value="unknown_user"):
        with patch("user_analysis.DataLoader") as mock_data_loader:
            mock_data_loader.return_value.get_issues.return_value = []
            
            analysis = UserAnalysis()
            analysis.run()
            with patch.object(UserAnalysis, "_plot_line_chart") as mock_plot_chart:
                analysis.run()
                mock_plot_chart.assert_not_called()
