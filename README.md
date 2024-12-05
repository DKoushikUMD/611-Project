# ENPM611 Project Application Template

This is the template for the ENPM611 class project. Use this template in conjunction with the provided data to implement an application that analyzes GitHub issues for the [poetry](https://github.com/python-poetry/poetry/issues) Open Source project and generates interesting insights.

This application template implements some of the basic functions:

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration paramters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With the utility functions provided, you should focus on implementing creative analyses that generate intersting and insightful insights.

In addition to the utility functions, an example analysis has also been implemented in `example_analysis.py`. It illustrates how to use the provided utility functions and how to produce output.

## Setup

To get started, your team should create a fork of this repository. Then, every team member should clone your repository to their local computer. 


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Download the data file (in `json` format) from the project assignment in Canvas and update the `config.json` with the path to the file. Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis

With everything set up, you should be able to run the existing example analysis:

```
python run.py --feature 0
```

That will output basic information about the issues to the command line.


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.

# GitHub Issue Analysis for Poetry Project

An analytical tool for extracting insights from Poetry package manager's GitHub issues, featuring interactive visualizations and detailed metrics.

## Features

**1. User Label Trend Analysis**
- Tracks how users interact with issue labels over time
- Interactive line chart with hover functionality
- Draggable legend for customizable view
- Command: `python run.py --feature 1 --user <username>`

**2. Label Interaction Metrics**
- Visualizes top 20 users' engagement with specific labels
- Interactive bar chart with detailed tooltips
- Comprehensive interaction statistics
- Command: `python run.py --feature 2 --label <label_name>`

**3. Label Distribution Analysis**
- Analyzes label popularity trends across years
- Interactive stacked bar visualization
- Percentage-based distribution view
- Command: `python run.py --feature 3`

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure data file
# Update config.json with data file path or set ENPM611_PROJECT_DATA_PATH environment variable
```

## Project Structure

```
├── data_loader.py            # Data loading utilities
├── model.py                  # Data models
├── config.py                 # Configuration handler
├── user_analysis.py         # User trend analysis
├── label_analysis.py        # Label interaction analysis
├── label_interest_analysis.py # Label distribution analysis
└── run.py                   # Main entry point
/tests
    test_label_analysis.py
    test_label_interest_analysis.py
    test_user_analysis.py
```

## Requirements

- Python 3.6+
- matplotlib
- pandas
- plotly
- numpy

## Development Setup

**VSCode Configuration**
- Debugging configurations available in `.vscode/launch.json`
- Customized settings in `.vscode/settings.json`
- Run configurations for each analysis feature

## Testing

Run the example analysis to verify setup:
```bash
python run.py --feature 0

Install these packages using the following command:
pip install pytest coverage

Execute the following command in the terminal from the project directory:
pytest

To test a specific file, use:
pytest test_label_analysis.py

Use coverage to measure code coverage:
coverage run -m pytest

After running the above command, generate a coverage report in the terminal:
coverage report -m

For a more detailed view, generate an HTML coverage report:
coverage html

```

## Output Types

- Feature 1: Time-series line charts with interactive elements
- Feature 2: Interactive bar charts with user statistics
- Feature 3: HTML-based stacked bar visualization

## Error Handling

- Validates command-line arguments
- Provides clear error messages for missing data
- Handles empty datasets and invalid inputs