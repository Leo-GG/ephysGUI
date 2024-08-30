import numpy as np
from scipy import signal

def detect_artifacts(data, threshold=5, segment_size=1000, positive_penalty=1.5):
    """
    Detect artifacts in a single channel of data using time-averaged segments.
    
    Args:
    data (numpy.ndarray): 1D array of voltage data for a single channel
    threshold (float): Number of standard deviations to use as threshold
    segment_size (int): Number of samples to average over
    positive_penalty (float): Extra penalty for positive signals
    
    Returns:
    numpy.ndarray: Boolean array where True indicates an artifact
    """
    # Compute time-averaged segments
    num_segments = len(data) // segment_size
    segments = data[:num_segments * segment_size].reshape(-1, segment_size)
    averaged_segments = np.mean(segments, axis=1)
    
    # Compute the z-score of the averaged segments
    z_scores = (averaged_segments - np.mean(averaged_segments)) / np.std(averaged_segments)
    
    # Apply extra penalty to positive signals
    z_scores[z_scores > 0] *= positive_penalty
    
    # Identify artifacts
    artifacts = np.abs(z_scores) > threshold
    
    # Expand artifacts to original data size
    expanded_artifacts = np.repeat(artifacts, segment_size)
    
    # Pad the array if necessary
    if len(expanded_artifacts) < len(data):
        expanded_artifacts = np.pad(expanded_artifacts, (0, len(data) - len(expanded_artifacts)), 'constant')
    
    return expanded_artifacts

def detect_artifacts_all_channels(data, threshold=5, segment_size=1000, positive_penalty=1.5):
    """
    Detect artifacts in all channels of data.
    
    Args:
    data (numpy.ndarray): 2D array of voltage data (samples x channels)
    threshold (float): Number of standard deviations to use as threshold
    segment_size (int): Number of samples to average over
    positive_penalty (float): Extra penalty for positive signals
    
    Returns:
    numpy.ndarray: 2D boolean array where True indicates an artifact
    """
    return np.apply_along_axis(lambda x: detect_artifacts(x, threshold, segment_size, positive_penalty), 0, data)