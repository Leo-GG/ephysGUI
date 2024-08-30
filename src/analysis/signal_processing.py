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

def detect_peaks(data, distance, threshold, window_size):
    peaks, _ = find_peaks(data, distance=distance, height=threshold)
    return peaks

def extract_peak_windows(data, peaks, window_size):
    half_window = window_size // 2
    peak_windows = []
    for peak in peaks:
        start = max(0, peak - half_window)
        end = min(len(data), peak + half_window)
        window = data[start:end]
        if len(window) == window_size:
            peak_windows.append(window)
    return np.array(peak_windows)