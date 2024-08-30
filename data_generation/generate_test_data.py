import numpy as np
import os

def generate_test_data(num_samples=10000, num_channels=5, sampling_rate=1000):
    """
    Generate test data for electrophysiology analysis.
    
    Args:
    num_samples (int): Number of time points
    num_channels (int): Number of channels
    sampling_rate (int): Sampling rate in Hz
    
    Returns:
    numpy.ndarray: 2D array of voltage data (samples x channels)
    """
    time = np.arange(num_samples) / sampling_rate
    data = np.zeros((num_samples, num_channels))
    
    for i in range(num_channels):
        # Generate a sine wave with different frequency for each channel
        frequency = 1 + i * 2  # Hz
        amplitude = 1 + i * 0.5  # mV
        data[:, i] = amplitude * np.sin(2 * np.pi * frequency * time)
        
        # Add some noise
        noise = np.random.normal(0, 0.1, num_samples)
        data[:, i] += noise
    
    return data

if __name__ == "__main__":
    # Generate test data
    test_data = generate_test_data()
    
    # Create a 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Save the test data
    np.save('data/test_data.npy', test_data)
    print(f"Test data saved to 'data/test_data.npy'")
    print(f"Data shape: {test_data.shape}")