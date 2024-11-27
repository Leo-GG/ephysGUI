# Electrophysiology Data Analyzer

## Description
This tool is designed for analyzing electrophysiological data, including filtering, artifact detection, and peak analysis. It provides a user-friendly graphical interface for loading, processing, and visualizing electrophysiological recordings. The GUI supports both NumPy (.npy) files and Intan (.rhd) files through the [intan_reader](https://github.com/Leo-GG/intanreader) package.

## Features
- Load and visualize electrophysiology data
- Apply various filters (notch, low-pass, high-pass)
- Detect and visualize artifacts
- Detect and analyze peaks
- Channel selection and management
- Interactive data trimming
- Statistical analysis of channels and peaks
- Export statistics to Excel

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- [intan_reader](https://github.com/Leo-GG/intanreader) package

### Installing from source

1. Clone the repository:
   ```bash
   git clone https://github.com/leo-gg/ephysGUI.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ephysGUI
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main script to start the application:

```
python main.py
```

### Loading Data

1. Click "File → Load Data" to select a data file:
   - .npy files: 2D NumPy array with shape (samples, channels)
   - .rhd files: Raw data files from Intan recording systems
2. Enter the sampling rate of your data in the "Sampling Rate (Hz)" field (not needed for .rhd files as it -should be- automatically detected)

### Applying Filters

1. Enter the desired frequency in the appropriate field for the filter you want to apply.
2. Click the corresponding "Apply" button for Notch, Low-pass, or High-pass filters.
3. The filtered data will automatically update in the visualization.

### Detecting Artifacts

1. Enter the artifact threshold value in the "Artifact Threshold" field.
2. Click the "Detect Artifacts" button.
3. Detected artifacts will be highlighted in the main plot.

### Detecting Peaks

1. Enter the peak threshold value in the "Peak Threshold" field.
2. Click the "Detect Peaks" button.
3. Detected peaks will be marked on the main plot, and average peak windows will be shown in the lower plot.

### Visualizing Data

- The main plot shows the selected channels and any detected artifacts or peaks.
- The lower plot displays the average peak windows for selected channels.
- Use the channel selection list on the right to choose which channels to display.
- Use the zoom and pan buttons below the plots to navigate through the data.

## Contributing

Contributions to the project are very welcome! Please feel free to submit pull requests, create issues, or suggest improvements. For major changes, please open an issue first to discuss what you would like to change.

## Authors

- [Leonardo Garma](https://www.linkedin.com/in/leonardo-garma/) - Development and Implementation
- [Erica Zeglio](https://www.kth.se/profile/zeglio) - Project Supervision and Testing
- [Kateryna Solodka](https://www.linkedin.com/in/kateryna-solodka/) - Testing and Validation

## Funding

This project was made possible through the generous support of:

- [The Swedish Research Council (VR)](https://www.vr.se)
- [Foundation for Research Without Animal Experiments (Forska Utan Djurförsök)](https://forskautandjurforsok.se)

## Contact

Leonardo Garma - leonardo.garma@gmail.com

Project Link: [https://github.com/leo-gg/ephysGUI](https://github.com/leo-gg/ephysGUI)

## Acknowledgements

- [Intan Technologies](http://intantech.com/) for their excellent electrophysiology recording systems and open-source software
