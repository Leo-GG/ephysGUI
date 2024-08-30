import numpy as np
from scipy import signal
from scipy.signal import find_peaks  # Add this import

def apply_filter(data, lowcut=0.5, highcut=50, fs=1000, order=5):
    """
    Apply a bandpass filter to the data.
    
    Args:
    data (numpy.ndarray): 2D array of voltage data (samples x channels)
    lowcut (float): Lower frequency bound
    highcut (float): Upper frequency bound
    fs (float): Sampling frequency
    order (int): Filter order
    
    Returns:
    numpy.ndarray: Filtered data
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    
    filtered_data = np.zeros_like(data)
    for i in range(data.shape[1]):
        filtered_data[:, i] = signal.filtfilt(b, a, data[:, i])
    
    return filtered_data

def apply_notch_filter(data, fs, freq, q=30):
    nyq = 0.5 * fs
    freq = freq / nyq
    b, a = signal.iirnotch(freq, q)
    return signal.filtfilt(b, a, data, axis=0)

def apply_lowpass_filter(data, fs, freq, order=5):
    nyq = 0.5 * fs
    normal_cutoff = freq / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, data, axis=0)

def apply_highpass_filter(data, fs, freq, order=5):
    nyq = 0.5 * fs
    normal_cutoff = freq / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return signal.filtfilt(b, a, data, axis=0)

def detect_peaks(data, sampling_rate, threshold, min_distance=0.5, detect_positive=False, window_size=None):
    """
    Detect peaks in the data, discarding peaks near the edges.

    Args:
        data (numpy.ndarray): Input signal.
        sampling_rate (float): Sampling rate of the data in Hz.
        threshold (float): Minimum absolute height of peaks.
        min_distance (float): Minimum distance between peaks in seconds.
        detect_positive (bool): If True, detect positive peaks; if False, detect negative peaks.
        window_size (int): Size of the window around each peak (in samples).

    Returns:
        numpy.ndarray: Array of peak indices.
    """
    min_distance_samples = int(min_distance * sampling_rate)
    
    if detect_positive:
        peaks, _ = find_peaks(data, height=threshold, distance=min_distance_samples)
    else:
        peaks, _ = find_peaks(-data, height=threshold, distance=min_distance_samples)
    
    if window_size is not None:
        edge_threshold = 2 * window_size
        peaks = peaks[(peaks >= edge_threshold) & (peaks < len(data) - edge_threshold)]
    
    return peaks

def extract_peak_windows(data, peak_indices, window_size):
    """
    Extract windows around detected peaks.

    Args:
        data (numpy.ndarray): Input signal.
        peak_indices (numpy.ndarray): Indices of detected peaks.
        window_size (int): Size of the window around each peak (in samples).

    Returns:
        numpy.ndarray: Array of peak windows.
    """
    half_window = window_size // 2
    peak_windows = []
    for peak in peak_indices:
        start = max(0, peak - half_window)
        end = min(len(data), peak + half_window)
        window = data[start:end]
        if len(window) == window_size:
            peak_windows.append(window)
    return np.array(peak_windows)