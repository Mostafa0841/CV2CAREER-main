from transformers import AutoTokenizer, AutoModelForSequenceClassification , pipeline
import torch


def predict_segment(txt , classifier):
    # Use the pipeline's predict method to get predictions directly
    result = classifier(txt)
    predicted_label = result[0]["label"]
    print(f"{txt} : {predicted_label}")
    return predicted_label



