import numpy as np
import pandas as pd
from scipy import signal

def generate_test_data(num_samples=10000, num_channels=3, sampling_rate=1000):
    time = np.arange(num_samples) / sampling_rate
    data = {}

    for channel in range(num_channels):
        # Base signal: sum of sine waves
        base_signal = (
            np.sin(2 * np.pi * 1 * time) +  # 1 Hz
            0.5 * np.sin(2 * np.pi * 10 * time) +  # 10 Hz
            0.3 * np.sin(2 * np.pi * 20 * time)  # 20 Hz
        )

        # Add some noise
        noise = np.random.normal(0, 0.1, num_samples)
        
        # Add some artifacts
        artifacts = np.zeros(num_samples)
        artifact_positions = np.random.choice(num_samples, 5, replace=False)
        artifacts[artifact_positions] = np.random.uniform(2, 5, 5) * np.random.choice([-1, 1], 5)

        # Add some peaks
        peaks = np.zeros(num_samples)
        peak_positions = np.random.choice(num_samples, 20, replace=False)
        peaks[peak_positions] = np.random.uniform(1, 2, 20)

        # Combine all components
        channel_data = base_signal + noise + artifacts + peaks

        # Add power line interference (50 Hz and 60 Hz)
        channel_data += 0.5 * np.sin(2 * np.pi * 50 * time)
        channel_data += 0.3 * np.sin(2 * np.pi * 60 * time)

        # Add low frequency drift
        drift = np.linspace(0, np.random.uniform(0.5, 1.5), num_samples)
        channel_data += drift

        data[f'Channel_{channel+1}'] = channel_data

    df = pd.DataFrame(data, index=time)
    return df

def main():
    # Generate test data
    test_data = generate_test_data()

    # Save to CSV
    test_data.to_csv('test_data.csv')
    print("Test data saved to 'test_data.csv'")

    # Display some basic information about the generated data
    print("\nGenerated Data Information:")
    print(f"Number of samples: {len(test_data)}")
    print(f"Number of channels: {len(test_data.columns)}")
    print(f"Sampling rate: 1000 Hz")
    print(f"Duration: {len(test_data)/1000:.2f} seconds")
    print("\nChannel statistics:")
    print(test_data.describe())

if __name__ == "__main__":
    main()