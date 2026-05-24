import streamlit as st
import pandas as pd
import numpy as np


from decomposition.lu import compute_lu
from decomposition.qr import compute_qr
from decomposition.eigen import compute_eigen
from decomposition.svd import compute_svd
from decomposition.cholesky import compute_cholesky


from utils.helpers import verify_reconstruction, convert_df_to_csv

# 1. Page Configuration
st.set_page_config(page_title="Matrix Decomposition Visualizer", layout="wide")
st.title("Matrix Decomposition Visualizer")

st.sidebar.header("Settings")
decomp_method = st.sidebar.selectbox(
    "Select Decomposition Method",
    ("LU", "QR", "Eigen", "SVD", "Cholesky")
)

# 2. Input Section
st.subheader("1. Input Matrix")

col1, col2 = st.columns(2)
with col1:
    rows = st.number_input("Rows", min_value=2, max_value=5, value=3)
with col2:
    cols = st.number_input("Columns", min_value=2, max_value=5, value=3)

if 'matrix_data' not in st.session_state or st.session_state.matrix_data.shape != (rows, cols):
    st.session_state.matrix_data = np.zeros((rows, cols))

if st.button("🎲 Generate Random Matrix"):
    st.session_state.matrix_data = np.random.randint(-10, 11, size=(rows, cols)).astype(float)

st.write("Enter values below or generate a random matrix:")
default_df = pd.DataFrame(st.session_state.matrix_data)
edited_df = st.data_editor(default_df, width="stretch", hide_index=True)

matrix_A = edited_df.to_numpy(dtype=float)

# 4. The Compute Trigger
st.subheader("2. Compute")

if 'is_computed' not in st.session_state:
    st.session_state.is_computed = False

if st.button("Compute Decomposition"):
    st.session_state.is_computed = True

if st.session_state.is_computed:
    if matrix_A is not None:
        st.write("### Results")
        
        # --- HEATMAP TOGGLE ---
        show_heatmap = st.checkbox("🎨 Enable Heatmap Visualization")
        
        # Helper function to render dataframes cleanly with or without heatmaps
        def render_df(data, is_eigen=False):
            df = pd.DataFrame(data)
            if is_eigen:
                st.dataframe(df.astype(str)) 
            elif show_heatmap:
                st.dataframe(df.style.background_gradient(cmap='coolwarm', axis=None))
            else:
                st.dataframe(df)

        st.write("**Original Matrix (A):**")
        render_df(matrix_A)
        
        # --- STEP-BY-STEP EXPLANATION ---
        with st.expander(f"📖 Learn the Math: How {decomp_method} Works"):
            if decomp_method == "LU":
                st.markdown("""
                **Step 1: Setup and Pivoting** We look for the largest number in the current column to act as our "pivot". If it's not in the top row, we swap rows to put it there. This creates our Permutation Matrix ($P$).
                **Step 2: Gaussian Elimination** We subtract multiples of the top row from the rows below it to create zeros under the pivot. This step-by-step reduction creates the Upper Triangular Matrix ($U$).
                **Step 3: Recording Multipliers** The exact multiples we used to zero out the rows are recorded. We place 1s on the diagonal and slot these multipliers below it to form the Lower Triangular Matrix ($L$).
                """)
            elif decomp_method == "QR":
                st.markdown("""
                **Step 1: Gram-Schmidt Process** We take the columns of your original matrix and process them one by one to make them completely perpendicular (orthogonal) to each other, and scale them to a length of 1.
                **Step 2: Forming Q** These newly polished, orthogonal vectors become the columns of our Orthogonal Matrix ($Q$).
                **Step 3: Forming R** We calculate the "shadows" (projections) of the original columns onto our new orthogonal vectors. These coefficients are placed into the Upper Triangular Matrix ($R$).
                """)
            elif decomp_method == "Eigen":
                st.markdown("""
                **Step 1: Characteristic Equation** We solve the determinant equation $det(A - \lambda I) = 0$ to find the roots. These roots are your **Eigenvalues** ($\lambda$).
                **Step 2: Diagonalization** We take those Eigenvalues and place them along the main diagonal of a matrix, with zeros everywhere else.
                **Step 3: Finding Eigenvectors** For each Eigenvalue, we plug it back into the equation $(A - \lambda I)v = 0$ and solve for $v$. These resulting vectors form the columns of our **Eigenvector Matrix**.
                """)
            elif decomp_method == "SVD":
                st.markdown("""
                **Step 1: Compute $A^T A$ and $A A^T$** We multiply the matrix by its transpose in both directions to create two new, symmetric matrices.
                **Step 2: Find Singular Values ($\Sigma$)** We find the eigenvalues of $A^T A$, take their square roots, and arrange them in descending order on the diagonal of matrix $\Sigma$.
                **Step 3: Form U and V** The eigenvectors of $A A^T$ become the columns of $U$ (Left Singular Vectors). The eigenvectors of $A^T A$ become the rows of $V^T$ (Right Singular Vectors).
                """)
            elif decomp_method == "Cholesky":
                st.markdown("""
                **Step 1: Symmetry and Definiteness Check** Before doing any math, the algorithm verifies that the matrix is symmetric and positive-definite.
                **Step 2: Diagonal Calculation** We calculate the top-left diagonal element by taking the square root of the first element in the original matrix: $L_{11} = \sqrt{A_{11}}$.
                **Step 3: Forward Substitution** Using the previously calculated elements, we iterate through the matrix solving for the remaining elements of the Lower Triangular Matrix ($L$).
                """)
        
        try:
            if decomp_method == "LU":
                results = compute_lu(matrix_A)
                st.write("**Decomposed Matrices:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Matrix P**")
                    render_df(results["P (Permutation)"])
                    st.download_button("Download P", data=convert_df_to_csv(results["P (Permutation)"]), file_name='matrix_P.csv', mime='text/csv')
                with col2:
                    st.write("**Matrix L**")
                    render_df(results["L (Lower Triangular)"])
                    st.download_button("Download L", data=convert_df_to_csv(results["L (Lower Triangular)"]), file_name='matrix_L.csv', mime='text/csv')
                with col3:
                    st.write("**Matrix U**")
                    render_df(results["U (Upper Triangular)"])
                    st.download_button("Download U", data=convert_df_to_csv(results["U (Upper Triangular)"]), file_name='matrix_U.csv', mime='text/csv')

            elif decomp_method == "QR":
                results = compute_qr(matrix_A)
                st.write("**Decomposed Matrices:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Matrix Q (Orthogonal)**")
                    render_df(results["Q (Orthogonal)"])
                    st.download_button("Download Q", data=convert_df_to_csv(results["Q (Orthogonal)"]), file_name='matrix_Q.csv', mime='text/csv')
                with col2:
                    st.write("**Matrix R (Upper Triangular)**")
                    render_df(results["R (Upper Triangular)"])
                    st.download_button("Download R", data=convert_df_to_csv(results["R (Upper Triangular)"]), file_name='matrix_R.csv', mime='text/csv')

            elif decomp_method == "Eigen":
                results = compute_eigen(matrix_A)
                st.write("**Decomposed Matrices:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Eigenvalues (Diagonal Matrix)**")
                    render_df(results["Eigenvalues (Diagonal)"], is_eigen=True)
                    st.download_button("Download Eigenvalues", data=convert_df_to_csv(results["Eigenvalues (Diagonal)"]), file_name='eigenvalues.csv', mime='text/csv')
                with col2:
                    st.write("**Eigenvectors Matrix**")
                    render_df(results["Eigenvectors"], is_eigen=True)
                    st.download_button("Download Eigenvectors", data=convert_df_to_csv(results["Eigenvectors"]), file_name='eigenvectors.csv', mime='text/csv')

            elif decomp_method == "SVD":
                results = compute_svd(matrix_A)
                st.write("**Decomposed Matrices:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Matrix U**")
                    render_df(results["U"])
                    st.download_button("Download U", data=convert_df_to_csv(results["U"]), file_name='matrix_U.csv', mime='text/csv')
                with col2:
                    st.write("**Matrix Σ (Sigma)**")
                    render_df(results["Sigma"])
                    st.download_button("Download Σ", data=convert_df_to_csv(results["Sigma"]), file_name='matrix_sigma.csv', mime='text/csv')
                with col3:
                    st.write("**Matrix V^T**")
                    render_df(results["V^T"])
                    st.download_button("Download V^T", data=convert_df_to_csv(results["V^T"]), file_name='matrix_Vt.csv', mime='text/csv')

            elif decomp_method == "Cholesky":
                results = compute_cholesky(matrix_A)
                st.write("**Decomposed Matrices:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Matrix L (Lower Triangular)**")
                    render_df(results["L (Lower Triangular)"])
                    st.download_button("Download L", data=convert_df_to_csv(results["L (Lower Triangular)"]), file_name='matrix_L.csv', mime='text/csv')
                with col2:
                    st.write("**Matrix L^T (Transpose)**")
                    render_df(results["L^T (Transpose)"])
                    st.download_button("Download L^T", data=convert_df_to_csv(results["L^T (Transpose)"]), file_name='matrix_Lt.csv', mime='text/csv')

            # --- MATRIX RECONSTRUCTION ---
            st.write("---") 
            st.subheader("Bonus: Matrix Reconstruction")
                
            if st.checkbox("Verify Decomposition"):
                reconstructed, is_match = verify_reconstruction(decomp_method, matrix_A, results)
                
                if reconstructed is not None:
                    if is_match:
                        st.success(f"Verification Successful! The decomposed matrices reconstruct the original matrix {matrix_A.shape}.")
                    else:
                        st.warning("Verification Failed. The reconstructed matrix does not perfectly match.")
                    
                    st.write("**Reconstructed Matrix:**")
                    render_df(reconstructed)
                else:
                    st.error("Could not verify reconstruction for this matrix.")
                        
        except ValueError as e:
            st.error(str(e))
    else:
        st.warning("Please provide a valid matrix first.")

# --- PERFORMANCE BENCHMARK ---
st.write("---")
st.subheader("Bonus: Algorithm Performance Benchmark")
st.write("Race the algorithms against each other to see which is the fastest on a 100x100 matrix.")

if st.button("⏱️ Run Performance Benchmark"):
    import time
    
    with st.spinner("Benchmarking algorithms..."):
        # Create a 100x100 symmetric positive-definite matrix so all methods (especially Cholesky) work
        test_mat = np.random.rand(100, 100)
        test_mat = np.dot(test_mat, test_mat.transpose())
        
        times = {}
        
        # Time LU
        start = time.time()
        compute_lu(test_mat)
        times["LU"] = time.time() - start
        
        # Time QR
        start = time.time()
        compute_qr(test_mat)
        times["QR"] = time.time() - start
        
        # Time Eigen
        start = time.time()
        compute_eigen(test_mat)
        times["Eigen"] = time.time() - start
        
        # Time SVD
        start = time.time()
        compute_svd(test_mat)
        times["SVD"] = time.time() - start
        
        # Time Cholesky
        start = time.time()
        compute_cholesky(test_mat)
        times["Cholesky"] = time.time() - start
        
        # Plot the results
        st.success("Benchmark complete!")
        time_df = pd.DataFrame(list(times.items()), columns=["Method", "Time (seconds)"]).set_index("Method")
        st.bar_chart(time_df)