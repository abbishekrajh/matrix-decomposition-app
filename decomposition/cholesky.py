import numpy as np

def compute_cholesky(matrix):
    """
    Decomposes a symmetric positive-definite matrix into a Lower triangular matrix (L).
    """
    # Safety Check 1: Must be a square matrix
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Cholesky decomposition requires a square matrix.")
    
    # Safety Check 2: Must be symmetric (Matrix must equal its transpose)
    if not np.allclose(matrix, matrix.T):
        raise ValueError("Cholesky requires a symmetric matrix (values mirrored across the diagonal).")
        
    try:
        # numpy.linalg.cholesky returns the lower triangular matrix L
        L = np.linalg.cholesky(matrix)
        
        return {
            "L (Lower Triangular)": L,
            "L^T (Transpose)": L.T
        }
    except np.linalg.LinAlgError:
        # This specific error triggers if the matrix is not positive-definite
        raise ValueError("Matrix is not positive-definite. Cholesky decomposition failed.")
    except Exception as e:
        raise ValueError(f"Cholesky Decomposition failed: {e}")