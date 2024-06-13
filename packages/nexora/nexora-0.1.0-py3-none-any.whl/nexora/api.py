import os

from fastapi import FastAPI

from .predict import AutoTunaPredict


app = FastAPI()
atunap = AutoTunaPredict(model_path=os.environ.get("AUTOTUNA_MODEL_PATH"))
schema = atunap.get_prediction_schema()


@app.post("/predict")
def predict(sample: schema):
    sample = sample.json()
    return atunap.predict_single(sample)
