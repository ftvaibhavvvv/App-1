import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Excel Numeric Analyzer", layout="wide")
st.title("Excel Numeric Analyzer")
st.write("Upload an Excel file. The app will analyze numeric columns, plot histograms, and compare mean vs median.")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

def forecast_message(mean_val, median_val):
    if pd.isna(mean_val) or pd.isna(median_val):
        return "Not enough data to judge forecasting suitability."
    diff = abs(mean_val - median_val)
    avg = (abs(mean_val) + abs(median_val)) / 2 if (abs(mean_val) + abs(median_val)) != 0 else 1
    if diff <= 0.1 * avg:
        return "the data can be used for the forecasting"
    return "the data may need more analysis before forecasting"

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found in the uploaded file.")
        else:
            st.subheader("Numeric Column Analysis")

            results = []

            for col in numeric_cols:
                series = pd.to_numeric(df[col], errors="coerce").dropna()

                if series.empty:
                    continue

                mean_val = series.mean()
                median_val = series.median()
                message = forecast_message(mean_val, median_val)

                results.append({
                    "column": col,
                    "mean": mean_val,
                    "median": median_val,
                    "forecast_suitability": message
                })

                st.markdown(f"### {col}")
                st.write(f"Mean: **{mean_val:.4f}**")
                st.write(f"Median: **{median_val:.4f}**")
                st.write(message)

                fig, ax = plt.subplots()
                ax.hist(series, bins=20, edgecolor="black")
                ax.set_title(f"Histogram of {col}")
                ax.set_xlabel(col)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)

            if results:
                st.subheader("Summary Table")
                result_df = pd.DataFrame(results)
                st.dataframe(result_df)

    except Exception as e:
        st.error(f"Error reading file: {e}")
