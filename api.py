from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from phishingdetection import FeatureExtraction, gbc

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.post("/verify_url")
async def verify_url(request: URLRequest):
    obj = FeatureExtraction(request.url)
    features = np.array(obj.getFeaturesList()).reshape(1, -1)
    y_pred = gbc.predict(features)[0]
    result = "safe" if y_pred == 1 else "phishing"
    return {"status": result, "prediction": y_pred}
