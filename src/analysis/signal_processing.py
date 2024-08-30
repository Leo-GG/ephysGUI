import numpy as np
from scipy import signal

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

def detect_peaks(data, distance=1000, prominence=0.5, threshold=None, window_size=2000):
    """
    Detect peaks in the data, avoiding edges to ensure full windows can be extracted.
    
    Args:
    data (numpy.ndarray): 2D array of voltage data (samples x channels)
    distance (int): Minimum distance between peaks
    prominence (float): Minimum prominence of peaks
    threshold (float): Amplitude threshold for peak detection (detect peaks below -threshold)
    window_size (int): Size of the window to extract around each peak
    
    Returns:
    list: List of arrays containing peak indices for each channel
    """
    peaks = []
    edge_padding = window_size #// 2
    for channel in range(data.shape[1]):
        channel_data = data[:, channel]
        if threshold is not None:
            # Detect peaks below -threshold
            channel_peaks, _ = signal.find_peaks(-channel_data, 
                                                 distance=distance, 
                                                 prominence=prominence,
                                                 height=threshold)
        else:
            channel_peaks, _ = signal.find_peaks(-channel_data, 
                                                 distance=distance, 
                                                 prominence=prominence)
        
        # Remove peaks that are too close to the edges
        channel_peaks = channel_peaks[(channel_peaks >= edge_padding) & (channel_peaks < len(channel_data) - edge_padding)]
        
        peaks.append(channel_peaks)
    return peaks

def extract_peak_windows(data, peaks, window_size=2000):
    """
    Extract windows around detected peaks.
    
    Args:
    data (numpy.ndarray): 2D array of voltage data (samples x channels)
    peaks (list): List of arrays containing peak indices for each channel
    window_size (int): Size of the window to extract around each peak
    
    Returns:
    list: List of arrays containing peak windows for each channel
    """
    windows = []
    for channel, channel_peaks in enumerate(peaks):
        channel_windows = []
        for peak in channel_peaks:
            start = max(0, peak - window_size // 2)
            end = min(data.shape[0], peak + window_size // 2)
            window = data[start:end, channel]
            if len(window) < window_size:
                window = np.pad(window, (0, window_size - len(window)), mode='constant')
            channel_windows.append(window)
        windows.append(np.array(channel_windows))
    return windows