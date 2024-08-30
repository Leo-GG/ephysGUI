import numpy as np

def load_data(file_path):
    """
    Load data from a NumPy file.
    
    Args:
    file_path (str): Path to the .npy file
    
    Returns:
    tuple: (data, time), where data is a 2D numpy array (samples x channels)
           and time is a 1D numpy array
    """
    data = np.load(file_path)
    time = np.arange(data.shape[0])
    return data, time