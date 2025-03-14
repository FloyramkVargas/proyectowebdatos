import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the title of the app
st.title("Load and Visualize Your Dataset")

# File uploader widget to upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the dataframe
    st.subheader("Dataset Overview")
    st.write(df.head())  # Display first 5 rows of the dataset

    # Handle non-numeric data by attempting to convert columns to numeric
    def clean_column(col):
        # Try converting to numeric, forcing errors to NaN
        return pd.to_numeric(col, errors='coerce')
    
    # Apply cleaning to all columns
    df_cleaned = df.apply(clean_column)

    # Show cleaned dataset statistics
    st.subheader("Dataset Statistics")
    st.write(df_cleaned.describe())  # Display statistical summary of the cleaned dataset

    # Display column names for selection
    columns = df_cleaned.columns.tolist()

    # Select a column to create a histogram
    st.subheader("Histogram of a Column")
    column_for_hist = st.selectbox("Select a column to plot histogram", columns)
    if column_for_hist:
        fig, ax = plt.subplots()
        sns.histplot(df_cleaned[column_for_hist], kde=True, ax=ax)
        st.pyplot(fig)

    # Scatter plot - user selects two columns
    st.subheader("Scatter Plot")
    column_x = st.selectbox("Select X-axis column", columns)
    column_y = st.selectbox("Select Y-axis column", columns)

    if column_x and column_y:
        fig, ax = plt.subplots()
        sns.scatterplot(x=df_cleaned[column_x], y=df_cleaned[column_y], ax=ax)
        ax.set_title(f"Scatter plot of {column_x} vs {column_y}")
        st.pyplot(fig)

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    numeric_df = df_cleaned.select_dtypes(include=["number"])  # Select only numeric columns
    if numeric_df.shape[1] > 1:  # Ensure there are at least two numeric columns
        correlation_matrix = numeric_df.corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Dataset doesn't contain enough numeric columns to generate a correlation heatmap.")
else:
    st.info("Please upload a CSV file to get started.")
