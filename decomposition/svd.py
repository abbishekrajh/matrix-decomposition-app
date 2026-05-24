import numpy as np

def compute_svd(matrix):
    """
    Decomposes a matrix into U, Sigma (diagonal), and V^T.
    """
    try:
        # numpy.linalg.svd returns U, S (1D array), and V^T
        # full_matrices=False keeps the dimensions manageable for display
        U, S, VT = np.linalg.svd(matrix, full_matrices=False)
        
        # Convert the 1D array of singular values (S) into a proper diagonal matrix (Sigma)
        Sigma = np.diag(S)
        
        return {
            "U": U,
            "Sigma": Sigma,
            "V^T": VT
        }
    except Exception as e:
        raise ValueError(f"SVD Decomposition failed: {e}")