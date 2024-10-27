import sys
sys.path.append(r'C:\Users\InbaTamizhan\Desktop\Phishing_Website_detection')
from phishingdetection import FeatureExtraction
import numpy as np
from phishingdetection import gbc
import streamlit as st

st.title("Phishing Website Detection")
#
# User input for URL
url = st.text_input("Enter the Url:", key="url_input")
#can provide any URL. this URL was taken from PhishTank

# Predict and display the result
if st.button("Check"):
    if url:
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)
        y_pred = gbc.predict(x)[0]
        if y_pred == 1:
            st.write("We guess it is a safe website")
        else:
            st.write("Caution! Suspicious website detected")
        st.write(y_pred)
    else:
        st.write("Please enter a URL.")
