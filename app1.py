import sys
import streamlit as st
from phishingdetection import FeatureExtraction, gbc
import numpy as np
from urllib.parse import urlparse, parse_qs

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
