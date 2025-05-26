import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.oauth2 import service_account
from utils.data_loader import load_and_process_data
from utils.chart import plot_candlestick_chart_plotly, plot_candlestick_chart_mpf
from utils.ai_agent import ask_gemini


st.set_page_config(layout="wide", page_title="TSLA Dashboard")
st.title("📊 Stock Dashboard")

st.title("Candlestick Replay")

# Display the GIF
with open("candlestick_replay.gif", "rb") as f:
    gif = f.read()
st.image(gif)

# Load data
data = load_and_process_data("data/TSLA_data - Sheet1.csv")

# Show data
with st.expander("📋 View Processed Data"):
    st.dataframe(data)

# Choose chart type
st.subheader("📈 Chart Viewer")
chart_type = st.selectbox("Select Chart Type", ["Plotly", "mplfinance"])

if chart_type == "Plotly":
    plot_candlestick_chart_plotly(data)
else:
    plot_candlestick_chart_mpf(data)

# ---- Load Gemini API ----
#creds = service_account.Credentials.from_service_account_file(
#    "C:/New folder/tsla_dashboard/animated-flare-460706-g0-f396476bb79a.json",
#    scopes=['https://www.googleapis.com/auth/cloud-platform']
#)
#genai.configure(credentials=creds)
#model = genai.GenerativeModel('gemini-pro')

genai.configure(api_key = st.secrets["google_api"]["key"])

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")  # or another model you are using
response = model.generate_content("How many days was TSLA bullish in 2023?")

print(response.text)

# ---- Session state ----
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ---- App Layout ----

tab1, tab2 = st.tabs(["📊 Upload & View Data", "🤖 Ask AI"])

with tab1:
    st.title("Upload Spreadsheet")
    uploaded_file = st.file_uploader("Upload your stock spreadsheet (.csv or .xlsx)", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state.df = df  # Store DataFrame for use in chatbot
        st.dataframe(df)

with tab2:
    st.title("Agentic AI Chatbot")

    if 'df' not in st.session_state:
        st.warning("Please upload a spreadsheet first in the Upload tab.")
    else:
        question = st.text_input("Ask a question about the uploaded data:")

        if st.button("Ask"):
            df = st.session_state.df
            data_sample = df.head(50).to_csv(index=False)

            prompt = f"""
You are a helpful AI assistant. Here is a sample of the user's spreadsheet data:

{data_sample}

Answer the following question using this data only: 
{question}
"""

            response = model.generate_content(prompt)
            st.session_state.chat_history.append(("User", question))
            st.session_state.chat_history.append(("Agentic AI", response.text))

        # Display chat history
        for role, msg in st.session_state.chat_history:
            st.markdown(f"**{role}:** {msg}")

