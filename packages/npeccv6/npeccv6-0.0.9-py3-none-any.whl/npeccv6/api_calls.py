#!/bin/python3
import cv2
import requests
import cv2

# Define the endpoints URLs
url_predict = "http://localhost:8000/predict"
url_create_model = "http://localhost:8000/create_model/"
url_train = "http://localhost:8000/train"

# ------------ #
# create model #
# ------------ #

# Define the parameters
params = {
    "name_model": "test",
}

# Make the API call
response = requests.post(url_create_model, json=params)

# Check the response
if response.status_code == 200:
    print("Model created successfully!")
else:
    print("Failed to create model:", response.text)

print("-------------")
# ------- #
# predict #
# ------- #
files = {
    "files": open(
        "../data/test/test/035_43-14-ROOT1-2023-08-08_pvd_OD01_f6h1_03-Fish Eye Corrected.png",
        "rb",
    )
}
# Define the parameters

predict_data = {
    "name_model": "test",
}


response = requests.post(url_predict, files=files, data=predict_data)

if response.status_code == 200:
    print(
        "Prediction sucessful! Predicted mask and confidency returned but not printed"
    )
else:
    print("Prediction failed:", response.text)

parse_respons = response.json()
# print(parse_respons)

print("----------")
# ----- #
# Train #
# ----- #
params_train = {
    "model_name": "test",
    "classes": ["root"],
    "patch_dir": "../data_patched",
    "seed": 42,
    "batch_size": 16,
    "epochs": 20,
    "models_path": "../models",
}

response = requests.post(url_train, json=params_train)
parse_respons = response.json()

print(parse_respons)
