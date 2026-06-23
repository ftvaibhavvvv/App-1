import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Excel Forecast Check App", layout="wide")

st.title("Excel Forecast Check App")
st.write(
    "Upload an Excel file. The app will detect numeric columns, "
    "create histograms, and calculate mean and median."
)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

def is_close(mean_value, median_value, tolerance=0.10):
    if pd.isna(mean_value) or pd.isna(median_value):
        return False

    base = max(abs(mean_value), abs(median_value), 1)
    difference = abs(mean_value - median_value)

    return difference <= tolerance * base

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            st.warning("No numeric columns were found in this Excel file.")
        else:
            st.subheader("Analysis Results")

            summary_rows = []

            for column in numeric_df.columns:
                series = pd.to_numeric(numeric_df[column], errors="coerce").dropna()

                if series.empty:
                    continue

                mean_value = series.mean()
                median_value = series.median()

                if is_close(mean_value, median_value):
                    forecast_message = "The data can be used for forecasting"
                else:
                    forecast_message = "The data may need more analysis before forecasting"

                summary_rows.append({
                    "Column": column,
                    "Mean": round(mean_value, 4),
                    "Median": round(median_value, 4),
                    "Forecast Check": forecast_message
                })

                st.markdown(f"### {column}")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Mean", f"{mean_value:.4f}")

                with col2:
                    st.metric("Median", f"{median_value:.4f}")

                st.info(forecast_message)

                fig, ax = plt.subplots(figsize=(7, 4))
                ax.hist(series, bins=20, edgecolor="black")
                ax.set_title(f"Histogram of {column}")
                ax.set_xlabel(column)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
                plt.close(fig)

            if summary_rows:
                st.subheader("Summary Table")
                summary_df = pd.DataFrame(summary_rows)
                st.dataframe(summary_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.info("Please upload an Excel file to start.")
