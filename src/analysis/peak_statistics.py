import numpy as np

def compute_channel_statistics(data):
    """
    Compute basic statistics for each channel.

    Args:
        data (numpy.ndarray): The electrophysiology data (samples x channels).

    Returns:
        list: List of dictionaries containing statistics for each channel.
    """
    channel_stats = []
    for channel in range(data.shape[1]):
        channel_data = data[:, channel]
        stats = {
            'channel': channel + 1,
            'mean': np.mean(channel_data),
            'std': np.std(channel_data)
        }
        channel_stats.append(stats)
    return channel_stats

def compute_peak_statistics(data, peaks, time):
    """
    Compute statistics for detected peaks.

    Args:
        data (numpy.ndarray): The electrophysiology data (samples x channels).
        peaks (list): List of arrays containing peak indices for each channel.
        time (numpy.ndarray): Time array corresponding to the data.

    Returns:
        list: List of dictionaries containing statistics for each channel.
    """
    statistics = []
    total_time = time[-1] - time[0]

    for channel, channel_peaks in enumerate(peaks):
        if len(channel_peaks) > 0:
            peak_amplitudes = data[channel_peaks, channel]
            stats = {
                'channel': channel + 1,
                'num_peaks': len(channel_peaks),
                'frequency': len(channel_peaks) / total_time,
                'avg_amplitude': np.mean(peak_amplitudes),
                'std_amplitude': np.std(peak_amplitudes)
            }
        else:
            stats = {
                'channel': channel + 1,
                'num_peaks': 0,
                'frequency': 0,
                'avg_amplitude': 0,
                'std_amplitude': 0
            }
        statistics.append(stats)

    return statistics