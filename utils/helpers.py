import numpy as np
import pandas as pd
import streamlit as st

def verify_reconstruction(method, original, results):
    """
    Reconstructs the original matrix from the decomposed parts 
    and verifies if it matches the original input.
    """
    reconstructed = None
    
    try:
        if method == "LU":
            # A = P @ L @ U (@ is the matrix multiplication operator in Python)
            reconstructed = results["P (Permutation)"] @ results["L (Lower Triangular)"] @ results["U (Upper Triangular)"]
        
        elif method == "QR":
            # A = Q @ R
            reconstructed = results["Q (Orthogonal)"] @ results["R (Upper Triangular)"]
            
        elif method == "Eigen":
            # A = V @ Lambda @ V^-1
            V = results["Eigenvectors"]
            Lambda = results["Eigenvalues (Diagonal)"]
            V_inv = np.linalg.inv(V)
            reconstructed = V @ Lambda @ V_inv
            
        elif method == "SVD":
            # A = U @ Sigma @ V^T
            reconstructed = results["U"] @ results["Sigma"] @ results["V^T"]
            
        elif method == "Cholesky":
            # A = L @ L^T
            reconstructed = results["L (Lower Triangular)"] @ results["L^T (Transpose)"]

        # Check if reconstructed matches original (allowing for floating point rounding errors)
        is_match = np.allclose(original, reconstructed, atol=1e-5)
        
        # Clean up complex numbers for Streamlit display if needed
        if np.iscomplexobj(reconstructed):
            reconstructed = np.real_if_close(reconstructed)
            
        return reconstructed, is_match
        
    except Exception as e:
        return None, False
    
@st.cache_data
def convert_df_to_csv(df):
    """Converts a pandas Dataframe to a CSV format for Streamlit downloading."""
    # Convert numpy array to dataframe if it isn't one already
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    return df.to_csv(index=False).encode('utf-8')
