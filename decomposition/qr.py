import numpy as np

def compute_qr(matrix):
    """
    Factorizes a matrix into an orthogonal matrix (Q) and an upper triangular matrix (R).
    """
    try:
        # numpy.linalg.qr returns Q, R
        Q, R = np.linalg.qr(matrix)
        
        return {
            "Q (Orthogonal)": Q,
            "R (Upper Triangular)": R
        }
    except Exception as e:
        raise ValueError(f"QR Decomposition failed: {e}")