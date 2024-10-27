import streamlit as st
import numpy as np
import requests
import threading
import uvicorn
from api import app  # Import the FastAPI app from api.py

# Function to run FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start FastAPI in a separate thread
threading.Thread(target=run_fastapi, daemon=True).start()

# Streamlit UI for manual URL input and detection
st.title("Phishing Website Detection - Test Interface")

# User input for URL
url = st.text_input("Enter the URL to test:")

# Verify URL on button click
if st.button("Check") and url:
    try:
        # Call the FastAPI endpoint
        response = requests.post("http://localhost:8000/verify_url", json={"url": url})
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "safe":
                st.success("This site appears safe.")
            else:
                st.warning("Caution! This website may be suspicious.")
            st.write("Prediction:", result["prediction"])
        else:
            st.error("Error: Could not retrieve prediction.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the FastAPI service: {e}")
