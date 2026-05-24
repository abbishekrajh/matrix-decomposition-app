import scipy.linalg
import numpy as np

def compute_lu(matrix):
    """
    Factorizes a matrix into Permutation (P), Lower (L), and Upper (U) matrices.
    """
    try:
        # scipy.linalg.lu returns P, L, U 
        P, L, U = scipy.linalg.lu(matrix)
        
        return {
            "P (Permutation)": P,
            "L (Lower Triangular)": L,
            "U (Upper Triangular)": U
        }
    except Exception as e:
        raise ValueError(f"LU Decomposition failed: {e}")