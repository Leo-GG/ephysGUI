import numpy as np

def compute_channel_statistics(data):
    """
    Compute basic statistics for each channel in the electrophysiology data.

    This function calculates the mean and standard deviation for each channel
    in the input data.

    Args:
        data (numpy.ndarray): The electrophysiology data with shape (samples, channels).

    Returns:
        list: A list of dictionaries, where each dictionary contains statistics
              for a single channel. The keys in each dictionary are:
              - 'channel': The channel number (0-indexed)
              - 'mean': The mean value of the channel data
              - 'std': The standard deviation of the channel data

    Example:
        >>> data = np.array([[1, 2], [3, 4], [5, 6]])
        >>> stats = compute_channel_statistics(data)
        >>> print(stats)
        [{'channel': 0, 'mean': 3.0, 'std': 2.0}, {'channel': 1, 'mean': 4.0, 'std': 2.0}]
    """
    channel_stats = []
    for channel in range(data.shape[1]):
        channel_data = data[:, channel]
        stats = {
            'channel': channel,
            'mean': np.mean(channel_data),
            'std': np.std(channel_data)
        }
        channel_stats.append(stats)
    return channel_stats

def compute_peak_statistics(data, peaks, time, sampling_rate):
    """
    Compute statistics for detected peaks in each channel of the electrophysiology data.

    Args:
        data (numpy.ndarray): The electrophysiology data with shape (samples, channels).
        peaks (list): A list of numpy arrays, where each array contains the indices
                      of detected peaks for a single channel.
        time (numpy.ndarray): A 1D array of time points corresponding to the data samples.
        sampling_rate (float): The sampling rate of the data in Hz.

    Returns:
        list: A list of dictionaries containing peak statistics for each channel.
    """
    statistics = []
    total_time = time[-1] - time[0]
    print(sampling_rate)
    for channel, channel_peaks in enumerate(peaks):
        if len(channel_peaks) > 1:
            peak_amplitudes = data[channel_peaks, channel]
            inter_peak_distances = np.diff(channel_peaks)
            inter_peak_times = inter_peak_distances / sampling_rate
            stats = {
                'channel': channel,
                'num_peaks': len(channel_peaks),
                'frequency': len(channel_peaks) / total_time,
                'avg_amplitude': np.mean(peak_amplitudes),
                'std_amplitude': np.std(peak_amplitudes),
                'mean_inter_peak_distance': np.mean(inter_peak_distances),
                'std_inter_peak_distance': np.std(inter_peak_distances),
                'mean_inter_peak_time': np.mean(inter_peak_times),
                'std_inter_peak_time': np.std(inter_peak_times)
            }
        else:
            stats = {
                'channel': channel,
                'num_peaks': len(channel_peaks),
                'frequency': len(channel_peaks) / total_time,
                'avg_amplitude': np.mean(data[channel_peaks, channel]) if len(channel_peaks) > 0 else 0,
                'std_amplitude': 0,
                'mean_inter_peak_distance': 0,
                'std_inter_peak_distance': 0,
                'mean_inter_peak_time': 0,
                'std_inter_peak_time': 0
            }
        statistics.append(stats)

    return statistics