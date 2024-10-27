from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from phishingdetection import FeatureExtraction, gbc

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
