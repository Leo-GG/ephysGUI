import numpy as np
from scipy import signal

def generate_ecg_like_signal(duration, fs):
    """Generate an ECG-like signal with random variations in amplitude and width."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)
    ecg = np.zeros_like(t)
    
    # Generate QRS complexes
    for i in np.arange(0, duration, np.random.uniform(1, 3)):
        qrs_center = int(i * fs)
        qrs_width = int(np.random.uniform(0.08, 0.12) * fs)  # Random width between 80-120 ms
        qrs = signal.gaussian(2 * qrs_width, std=qrs_width / 5)
        
        # Random amplitude variation around -300
        amplitude = np.random.uniform(.8, 1.2)*300
        
        start = max(0, qrs_center - qrs_width)
        end = min(len(ecg), qrs_center + qrs_width)
        ecg[start:end] -= amplitude * qrs[:end-start]
    
    return ecg
    
def generate_impulsive_noise(num_samples, num_channels, rate=0.001, amplitude_range=(50, 200)):
    """
    Generate impulsive noise.
    
    Args:
    num_samples (int): Number of samples in the signal
    num_channels (int): Number of channels
    rate (float): Probability of an impulse occurring at each sample
    amplitude_range (tuple): Range of possible amplitudes for impulses
    
    Returns:
    numpy.ndarray: 2D array of impulsive noise (samples x channels)
    """
    impulse_locations = np.random.random((num_samples, num_channels)) < rate
    impulse_amplitudes = np.random.uniform(amplitude_range[0], amplitude_range[1], (num_samples, num_channels))
    return impulse_locations * impulse_amplitudes

def generate_small_oscillations(num_samples, num_channels, num_oscillations=3, duration_range=(0.1, 0.5), amplitude_range=(50, 200)):
    """
    Generate sparse small oscillations.
    
    Args:
    num_samples (int): Number of samples in the signal
    num_channels (int): Number of channels
    num_oscillations (int): Number of oscillations to generate
    duration_range (tuple): Range of possible durations for oscillations (in seconds)
    amplitude_range (tuple): Range of possible amplitudes for oscillations
    
    Returns:
    numpy.ndarray: 2D array of small oscillations (samples x channels)
    """
    oscillations = np.zeros((num_samples, num_channels))
    for _ in range(num_oscillations):
        start = np.random.randint(0, num_samples)
        duration = np.random.uniform(*duration_range) * num_samples
        end = min(int(start + duration), num_samples)
        amplitude = np.random.uniform(*amplitude_range)
        channel = np.random.randint(0, num_channels)
        t = np.linspace(0, 2*np.pi, end-start)
        oscillations[start:end, channel] = amplitude * np.sin(t)
    return oscillations

def generate_artificial_data(duration=10, fs=20000, num_channels=5):
    """
    Generate artificial test data with variation per channel.
    
    Args:
    duration (float): Duration of the signal in seconds
    fs (int): Sampling frequency in Hz
    num_channels (int): Number of channels to generate
    
    Returns:
    numpy.ndarray: 2D array of artificial data (samples x channels)
    """
    num_samples = int(duration * fs)
    
    data = np.zeros((num_samples, num_channels))
    
    for channel in range(num_channels):
        # Generate white noise (below 10 microvolts)
        noise = np.random.normal(0, np.random.uniform(2, 4), num_samples)  # 2-4 microvolts std dev
        
        # Generate ECG-like signal with variation
        ecg = generate_ecg_like_signal(duration, fs)
        
        # Generate impulsive noise
        impulsive_noise = generate_impulsive_noise(num_samples, 1, rate=np.random.uniform(0.0005, 0.0015)).flatten()
        
        # Generate small oscillations
        small_oscillations = generate_small_oscillations(num_samples, 1, num_oscillations=np.random.randint(2, 5)).flatten()
        
        # Combine noise, ECG-like signal, impulsive noise, and small oscillations
        channel_data = noise + ecg + impulsive_noise + small_oscillations
        
        # Add some random drift
        drift = np.cumsum(np.random.normal(0, 0.01, num_samples))
        channel_data += drift
        
        data[:, channel] = channel_data
    
    return data

if __name__ == "__main__":
    # Generate test data
    duration = 30  # seconds
    fs = 20000  # Hz
    num_channels = 20
    
    artificial_data = generate_artificial_data(duration, fs, num_channels)
    
    print(f"Generated artificial data shape: {artificial_data.shape}")
    print(f"Data duration: {duration} seconds")
    print(f"Sampling rate: {fs} Hz")
    print(f"Number of channels: {num_channels}")
    
    # Save the artificial data
    np.save('data/artificial_test_data.npy', artificial_data)
    print("Artificial test data saved to 'data/artificial_test_data.npy'")

    # Optional: Plot a short segment of the first channel
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 6))
    t = np.linspace(0, 1, 10*fs)  # Plot first 10 seconds
    plt.plot(t, artificial_data[:10*fs, 0])
    plt.title("First 10 Seconds of Artificial Data (Channel 1)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (μV)")
    plt.grid(True)
    plt.savefig('data/artificial_data_plot.png')
    print("Plot of the first second saved to 'data/artificial_data_plot.png'")