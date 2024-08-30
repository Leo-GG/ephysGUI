import numpy as np
from scipy import signal

def generate_ecg_like_signal(duration, fs):
    """Generate an ECG-like signal."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)
    ecg = np.zeros_like(t)
    
    # Generate QRS complexes
    for i in np.arange(0, duration, np.random.uniform(1, 3)):
        qrs_center = int(i * fs)
        qrs_width = int(0.1 * fs)  # 100 ms wide QRS complex
        qrs = signal.gaussian(2 * qrs_width, std=qrs_width / 5)
        start = max(0, qrs_center - qrs_width)
        end = min(len(ecg), qrs_center + qrs_width)
        ecg[start:end] -= qrs[:end-start]
    
    return ecg

def generate_artificial_data(duration=10, fs=20000, num_channels=5):
    """
    Generate artificial test data.
    
    Args:
    duration (float): Duration of the signal in seconds
    fs (int): Sampling frequency in Hz
    num_channels (int): Number of channels to generate
    
    Returns:
    numpy.ndarray: 2D array of artificial data (samples x channels)
    """
    num_samples = int(duration * fs)
    
    # Generate white noise (below 10 microvolts)
    noise = np.random.normal(0, 3, (num_samples, num_channels))  # 3 microvolts std dev
    
    # Generate ECG-like signal
    ecg = generate_ecg_like_signal(duration, fs)
    
    # Combine noise and ECG-like signal
    data = noise + ecg[:, np.newaxis]
    
    return data

if __name__ == "__main__":
    # Generate test data
    duration = 10  # seconds
    fs = 20000  # Hz
    num_channels = 5
    
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
    t = np.linspace(0, 1, fs)  # Plot first second
    plt.plot(t, artificial_data[:fs, 0])
    plt.title("First Second of Artificial Data (Channel 1)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (μV)")
    plt.grid(True)
    plt.savefig('data/artificial_data_plot.png')
    print("Plot of the first second saved to 'data/artificial_data_plot.png'")