import json
import toml
import pandas as pd
from google.oauth2 import service_account
from google.generativeai import GenerativeModel, configure
import streamlit as st


# ✅ Load credentials properly from Streamlit secrets
# Parse multi-line private key correctly
creds_dict = dict(st.secrets["google_service_account"])
creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

credentials = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

configure(credentials=credentials)

# Load Gemini model
model = GenerativeModel("gemini-pro")


# 👇 Function to build context from your TSLA DataFrame
def get_table_context(df: pd.DataFrame) -> str:
    # Example: summarize the number of bullish/bearish days
    bullish_days = df[df["Trend"] == "Bullish"].shape[0]
    bearish_days = df[df["Trend"] == "Bearish"].shape[0]
    summary = f"The dataset contains {len(df)} total rows.\n"
    summary += f"There were {bullish_days} bullish days and {bearish_days} bearish days.\n"
    return summary


# 👇 Core function to send question to Gemini
def ask_gemini(df: pd.DataFrame, question: str) -> str:
    context = get_table_context(df)

    with open("C:/New folder/tsla_dashboard/prompts/template.txt") as f:
        template = f.read()

    prompt = template.replace("{{context}}", context).replace("{{question}}", question)

    # Send to Gemini
    response = model.generate_content(prompt)
    return response.text.strip()
