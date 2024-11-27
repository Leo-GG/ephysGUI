import numpy as np
from pathlib import Path
from typing import Tuple, Union
from intan_reader import IntanReader

def load_data(file_path: Union[str, Path]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load data from either a NumPy file (.npy) or Intan file (.rhd).
    
    Args:
        file_path (str or Path): Path to the data file (.npy or .rhd)
    
    Returns:
        tuple: (data, time), where:
            - data is a 2D numpy array (samples x channels)
            - time is a 1D numpy array with timestamps in seconds
    
    Raises:
        ValueError: If the file extension is not supported
        FileNotFoundError: If the file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.suffix == '.npy':
        data = np.load(file_path)
        time = np.arange(data.shape[0])
        return data, time
        
    elif file_path.suffix == '.rhd':
        # Load the Intan file
        reader = IntanReader(str(file_path))
        result = reader.read()
        
        # Extract amplifier data and convert to numpy array
        # The shape will be (samples x channels)
        data = np.array(result.data.amplifier_data).T
        
        # Create time array based on sampling rate
        sampling_rate = result.header.sample_rate
        duration = data.shape[0] / sampling_rate
        time = np.linspace(0, duration, data.shape[0])
        
        return data, time
        
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}. "
                        f"Supported formats are: .npy, .rhd")