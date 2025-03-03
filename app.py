import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure Streamlit app with a modern UI
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Apply a sleek, modern UI theme with enhanced design
st.markdown(
    """
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            padding: 2rem;
            border-radius: 16px;
            background-color: #161b22;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }
        h1, h2, h3, h4, h5, h6 {
            color: #58a6ff;
        }
        .stButton>button {
            border: none;
            border-radius: 12px;
            background: linear-gradient(90deg, #0078D7, #005a9e);
            color: white;
            padding: 10px 20px;
            font-size: 1rem;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #005a9e, #003f7f);
            transform: scale(1.05);
        }
        .stDataFrame, .stTable {
            border-radius: 12px;
            overflow: hidden;
            background-color: #21262d;
            color: #c9d1d9;
        }
        .stDownloadButton>button {
            background: linear-gradient(90deg, #28a745, #218838);
            border-radius: 12px;
            color: white;
            padding: 10px 20px;
            transition: all 0.3s ease-in-out;
        }
        .stDownloadButton>button:hover {
            background: linear-gradient(90deg, #218838, #1c6d32);
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 Advanced Data Sweeper")
st.write("Transform and clean your data with ease while enjoying a modern UI experience.")

uploaded_files = st.file_uploader("Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        df = pd.read_csv(file) if file_extension == ".csv" else pd.read_excel(file)
        
        st.write(f"**📄 File:** {file.name} ({file.size / 1024:.2f} KB)")
        st.dataframe(df.head())
        
        st.subheader("🛠 Data Cleaning")
        if st.checkbox(f"Clean Data ({file.name})"):
            if st.button("Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                st.write("✅ Duplicates Removed!")
            if st.button("Fill Missing Values"):
                df.fillna(df.mean(), inplace=True)
                st.write("✅ Missing Values Filled!")
        
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio("Convert to:", ["CSV", "Excel"], key=file.name)
        if st.button("Convert & Download"):
            buffer = BytesIO()
            file_name = file.name.replace(file_extension, ".csv" if conversion_type == "CSV" else ".xlsx")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button("⬇ Download File", data=buffer, file_name=file_name, mime=mime_type)

st.success("🎉 Your files are ready!")