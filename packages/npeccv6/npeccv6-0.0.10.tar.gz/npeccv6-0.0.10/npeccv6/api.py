import os
import shutil
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

try:
    from .data import load_and_preprocess_data
    from .model_func import create_model, load_pretrained_model, train_model
    from .predict import predict
    from .train import main as train
    from .utils import create_config_json, read_config, setup_logger

except:
    from model_func import create_model, load_pretrained_model, train_model
    from predict import predict
    from train import main as train
    from utils import create_config_json, read_config, setup_logger

    from data import load_and_preprocess_data


UPLOAD_DIRECTORY = "../user_data/to_predict/"


app = FastAPI()
logger = setup_logger()

# Move your existing prediction code here
# Ensure that `load_pretrained_model`, `predict`, and all other required functions are imported


class PredictionResult(BaseModel):
    predicted_mask: List[List[int]]
    mean_conf_score: float


class TrainResult(BaseModel):
    history: dict


class ModelParams(BaseModel):
    name_model: str
    input_shape: Tuple[int] = (256, 256, 1)
    output_classes: int = 1
    optimizer: str = "adam"
    loss: str = "binary_crossentropy"
    output_activation: str = "sigmoid"
    dropout_1: float = 0.1
    dropout_2: float = 0.2
    dropout_3: float = 0.3
    summary: bool = False
    models_path: str = "../models"


@app.post("/predict", response_model=List[PredictionResult])
async def predict_image_endpoint(
    name_model: str = "test",
    user_folder: str = "../user_data/anonymous",
    files: List[UploadFile] = File(...),
) -> List[PredictionResult]:
    results = []
    try:

        print(files)
        for file in files:
            # Make sure folders exist
            print(file)
            print(UPLOAD_DIRECTORY)
            os.makedirs(os.path.dirname(UPLOAD_DIRECTORY), exist_ok=True)
            os.makedirs(os.path.dirname(user_folder + "/images/"), exist_ok=True)
            os.makedirs(os.path.dirname(user_folder + "/masks/"), exist_ok=True)
            print("-----")
            print("Uploda directory" + UPLOAD_DIRECTORY)
            # Save the uploaded file locally
            image_file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
            print("path" + image_file_path)
            with open(image_file_path, "wb") as f:
                f.write(await file.read())

            # Get filename without extension
            base = os.path.basename(image_file_path)
            base_file_name = os.path.splitext(base)[0]

            # Load the pretrained model
            model = load_pretrained_model(name_model, "../models")

            # Predict using your existing function and save mask in history
            predicted_mask, mean_conf_score = predict(
                model,
                image_file_path,
                save_path=user_folder + "/masks/" + base_file_name + "_root_mask.tif",
            )

            # Move base image to history
            shutil.move(
                image_file_path, user_folder + "/images/" + base_file_name + ".png"
            )

            # Append the prediction result
            results.append(
                PredictionResult(
                    predicted_mask=predicted_mask, mean_conf_score=mean_conf_score
                )
            )

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")


@app.post("/create_model")
async def create_model_endpoint(params: ModelParams):
    try:
        model = create_model(
            params.name_model,
            params.input_shape,
            params.output_classes,
            params.optimizer,
            params.loss,
            params.output_activation,
            params.dropout_1,
            params.dropout_2,
            params.dropout_3,
            params.summary,
            params.models_path,
        )
        return model.summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/train")
async def train_model_endpoint(
    model_name: str = "test",
    classes: list = ["root"],
    patch_dir: str = "../data_patched",
    seed: int = 42,
    batch_size: int = 16,
    epochs: int = 20,
    models_path: str = "../models",
) -> TrainResult:
    try:
        logger.info(f"Reading config for model '{model_name}' at {models_path}")
        config = read_config(model_name, models_path)
        logger.info("Config loaded")
        (
            train_generator,
            test_generator,
            steps_per_epoch,
            validation_steps,
        ) = load_and_preprocess_data(
            classes=classes,
            name_model=model_name,
            patch_size=config["input_shape"][0],
            patch_dir=patch_dir,
            seed=seed,
            batch_size=batch_size,
        )

        logger.info(f"Training model\n{steps_per_epoch}\n{validation_steps}")
        logger.info(config["input_shape"])

        history = train_model(
            model_name=model_name,
            train_generator=train_generator,
            test_generator=test_generator,
            steps_per_epoch=steps_per_epoch,
            validation_steps=validation_steps,
            epochs=epochs,
            models_path=models_path,
        )

        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {e}")
