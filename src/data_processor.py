"""
Data processing functions for time series analysis.

This module contains functions for applying filters, detecting artifacts,
and detecting peaks in time series data.
"""

import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal import find_peaks

def apply_filters(data, fs=1000):
    """
    Apply pre-processing filters to the input data.

    Args:
        data (pd.DataFrame): Input time series data.
        fs (int): Sampling frequency in Hz. Default is 1000 Hz.

    Returns:
        pd.DataFrame: Filtered time series data.
    """
    nyquist = 0.5 * fs
    filtered_data = data.copy()

    for column in filtered_data.columns:
        # Apply notch filters at 50 Hz and 60 Hz
        #notch_50 = signal.notch(50, fs)
        #notch_60 = signal.notch(60, fs)
        #filtered_data[column] = signal.filtfilt(notch_50, [1], filtered_data[column])
        #filtered_data[column] = signal.filtfilt(notch_60, [1], filtered_data[column])

        # Apply high pass filter (1 Hz cutoff)
        high_pass = signal.butter(4, 1 / nyquist, btype='high', output='sos')
        filtered_data[column] = signal.sosfilt(high_pass, filtered_data[column])

        # Apply low pass filter (100 Hz cutoff)
        low_pass = signal.butter(4, 100 / nyquist, btype='low', output='sos')
        filtered_data[column] = signal.sosfilt(low_pass, filtered_data[column])

    return filtered_data

def run_artifact_detection(data, threshold):
    """
    Detect artifacts in the time series data.

    Args:
        data (pd.DataFrame): Input time series data.
        threshold (float): Z-score threshold for artifact detection.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: Filtered data with artifacts removed.
            - int: Number of artifacts detected.
            - dict: Dictionary of artifact indices for each channel.
    """
    filtered_data = data.copy()
    artifact_count = 0
    artifact_indices = {}

    for column in filtered_data.columns:
        z_scores = np.abs((filtered_data[column] - filtered_data[column].mean()) / filtered_data[column].std())
        artifacts = z_scores > threshold
        artifact_count += artifacts.sum()
        artifact_indices[column] = artifacts[artifacts].index
        filtered_data[column] = filtered_data[column].mask(artifacts, np.nan)

    return filtered_data.interpolate(), artifact_count, artifact_indices

def run_peak_detection(filtered_data, height, distance, artifact_indices):
    """
    Detect peaks in the filtered time series data.

    Args:
        filtered_data (pd.DataFrame): Filtered time series data.
        height (float): Minimum peak height.
        distance (int): Minimum distance between peaks.
        artifact_indices (dict): Dictionary of artifact indices for each channel.

    Returns:
        tuple: A tuple containing:
            - dict: Dictionary of peak indices for each channel.
            - dict: Dictionary of extracted signals around peaks for each channel.
            - int: Total number of peaks detected across all channels.
    """
    peaks = {}
    extracted_signals = {}
    peak