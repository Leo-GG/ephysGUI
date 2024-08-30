# Electrophysiology Data Analyzer

## Overview

The Electrophysiology Data Analyzer is a Python-based application designed for analyzing and visualizing electrophysiological data. It provides a user-friendly graphical interface for loading, filtering, and analyzing multi-channel voltage data.

## Features

- Load and visualize multi-channel electrophysiological data
- Apply various filters (notch, low-pass, high-pass)
- Detect artifacts in the signal
- Detect and visualize peaks
- Interactive data visualization with zooming and panning capabilities
- Customizable analysis parameters

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leo-gg/ephysGUI.git
   cd ephysGUI
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command from the project root directory:

```
python main.py
```