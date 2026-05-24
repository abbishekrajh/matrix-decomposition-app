# Matrix Decomposition Visualizer

## Overview
This is an interactive web application built with Python and Streamlit that allows users to perform, visualize, and learn about different matrix decomposition techniques. The application takes a matrix as input, computes the selected decomposition using NumPy and SciPy, and displays the resulting matrices in a structured, interactive format.

## Setup Instructions
To run this application locally on your machine, follow these steps:

1. Clone or download this repository.
2. Navigate to the project folder in your terminal:
   cd matrix-decomposition-app
3. Install the required dependencies:
   pip install -r requirements.txt
4. Run the Streamlit application:
   python3 -m streamlit run app.py

## Key Features & Bonus Implementations
* **Multiple Algorithms:** Supports LU, QR, Eigenvalue, SVD, and Cholesky decompositions.
* **Random Matrix Generator:** Instantly populate the input grid with random values for rapid testing.
* **Interactive Heatmaps:** Toggle a color-coded heatmap (via Pandas/Matplotlib) to visually analyze matrix weights.
* **Educational Explanations:** Expandable step-by-step breakdowns explaining the underlying math for every decomposition method.
* **CSV Export Pipeline:** Download any decomposed matrix (P, L, U, Q, R, etc.) directly to your local machine as a clean `.csv` file.
* **Reconstruction Verification:** A built-in mathematical proof engine that multiplies the decomposed matrices back together to verify they match the original input (accounting for floating-point errors).

## Project Structure
matrix-decomposition-app/
├── app.py                # Main Streamlit frontend and routing
├── requirements.txt      # Project dependencies
├── README.md             # Documentation
├── decomposition/        # Core mathematical logic
│   ├── __init__.py
│   ├── lu.py             # LU Decomposition function
│   ├── qr.py             # QR Decomposition function
│   ├── eigen.py          # Eigenvalue Decomposition function
│   ├── svd.py            # Singular Value Decomposition function
│   └── cholesky.py       # Cholesky Decomposition function
└── utils/                # Helper functions and validation
    ├── __init__.py
    ├── helpers.py        # Matrix reconstruction and CSV export logic

## Screenshots

*(Drag and drop your updated screenshots here!)*

1. **User Interface & Input:**
![alt text](<Screenshot 2026-05-25 at 12.03.48 AM.png>)

2. **Heatmap & Decomposition Results:**
![alt text](<Screenshot 2026-05-25 at 12.04.17 AM.png>)

3. **Step-by-Step Educational View:**
![alt text](<Screenshot 2026-05-25 at 12.04.38 AM.png>)

4. **Bonus Reconstruction & Export:**
![alt text](<Screenshot 2026-05-25 at 12.04.46 AM.png>)

5. **Performance Comparison Chart**
![alt text](<Screenshot 2026-05-25 at 12.08.25 AM.png>)