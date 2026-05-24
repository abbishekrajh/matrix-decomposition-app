import numpy as np

def compute_eigen(matrix):
    """
    Computes eigenvalues and eigenvectors for a square matrix.
    """
    # Safety Check: Must be a square matrix
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Eigenvalue decomposition requires a square (N x N) matrix.")
        
    try:
        # numpy.linalg.eig returns a 1D array of eigenvalues and a 2D array of eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        
        # Convert the 1D eigenvalues array into a diagonal matrix for better visualization
        eigen_diag = np.diag(eigenvalues)
        
        return {
            "Eigenvalues (Diagonal)": eigen_diag,
            "Eigenvectors": eigenvectors
        }
    except Exception as e:
        raise ValueError(f"Eigenvalue Decomposition failed: {e}")