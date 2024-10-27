import sys
import streamlit as st
from phishingdetection import FeatureExtraction, gbc
import numpy as np
from urllib.parse import urlparse, parse_qs
from fastapi import FastAPI
from pydantic import BaseModel
from streamlit.web import experimental_singleton

# FastAPI app initialization
app = FastAPI()

# Define request model for API endpoint
class URLRequest(BaseModel):
    url: str

# FastAPI endpoint for phishing detection
@app.post("/verify_url")
async def verify_url(request: URLRequest):
    obj = FeatureExtraction(request.url)
    x = np.array(obj.getFeaturesList()).reshape(1, 30)
    y_pred = gbc.predict(x)[0]
    result = "safe" if y_pred == 1 else "phishing"
    return {"status": result, "prediction": y_pred}

# Function to mount FastAPI app in Streamlit
@st.experimental_singleton
def get_api():
    from streamlit.web import StreamlitAPI
    api = StreamlitAPI(app)
    api.run(host="0.0.0.0", port=8000)
    return api

get_api()

# Streamlit UI for manual URL input and detection
st.title("Phishing Website Detection")

# Get the URL parameter from the query string
query_params = st.experimental_get_query_params()
url = query_params.get("url", [""])[0]  # Default to an empty string if no URL is provided

# User input for URL
if not url:  # If URL is not passed, show text input
    url = st.text_input("Enter the URL:", key="url_input")

# Verify URL on button click
if st.button("Check") or url:
    if url:
        st.write(f"Verifying URL: {url}")
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)
        y_pred = gbc.predict(x)[0]
        if y_pred == 1:
            st.write("This is likely a safe website.")
        else:
            st.write("Caution! This website may be suspicious.")
        st.write("Prediction:", y_pred)
    else:
        st.write("Please enter a URL.")
