# Time Series Analyzer

A Python application for analyzing and visualizing multi-channel time series data.

## Features

- Load and visualize multi-channel time series data
- Apply pre-processing filters
- Detect and visualize artifacts
- Detect and visualize peaks
- Extract and plot signals around detected peaks

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/time-series-analyzer.git
   cd time-series-analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Use the GUI to load data, select channels, and perform analysis.

## Generating Test Data

To generate artificial test data:

1. Run the test data generator:
   ```
   python tests/generate_test_data.py
   ```

2. The generated data will be saved as `test_data.csv` in the current directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.