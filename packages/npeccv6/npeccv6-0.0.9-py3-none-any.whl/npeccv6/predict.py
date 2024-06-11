#!/bin/python3
import argparse
from typing import Tuple

import cv2
import keras
import numpy as np
from keras.models import load_model
from keras.utils import custom_object_scope
from patchify import patchify, unpatchify

try:
    # Attempt relative imports (if run as a package module)
    from .data import crop_to_petri, padder
    from .postprocessing import process_image_for_roots
    from .utils import f1, iou, mean_confidence_score, setup_logger

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from postprocessing import process_image_for_roots
    from utils import f1, iou, mean_confidence_score, setup_logger

    from data import crop_to_petri, padder

logger = setup_logger()


def load_and_preprocess_image(
    im_path: str,
    patch_size: int = 256,
    scaling_factor: float = 1,
    num_channels: int = 1,
) -> Tuple[np.ndarray, int, int, np.ndarray]:
    """
    Load and preprocess an image for patch-based prediction.

    This function reads an image from the specified path, converts it to grayscale
    if required, crops it to the region of interest (ROI) determined by the `crop_to_petri`
    function, pads the image to the specified patch size, scales it, and finally divides
    the image into non-overlapping patches of the specified size.

    Parameters:
        - im_path (str): Path to the input image.
        - patch_size (int, optional): Size of the patches to extract from the image. Default is 256.
        - scaling_factor (float, optional): Factor by which to scale the image. Default is 1.
        - num_channels (int, optional): Number of channels to read from the image (1 for grayscale, 3 for color). Default is 1.

    Returns:
        tuple: A tuple containing:
            - patches (numpy.ndarray): Array of image patches with shape (num_patches, patch_size, patch_size, 1).
            - i (int): Number of patches along the height of the image.
            - j (int): Number of patches along the width of the image.
            - im (numpy.ndarray): The preprocessed image after cropping, padding, and scaling.

    Example:
        .. code-block:: python

            patches, i, j, im = load_and_preprocess_image('path/to/image.jpg', patch_size=128, scaling_factor=1, num_channels=3)
            print(patches.shape)
            (num_patches, 128, 128, 1)
            print(i, j)
            4 4
    """

    logger.info(f"Loading image from path: {im_path}")

    if num_channels == 1:
        im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
        logger.debug(f"load_and_preprocess_image:number of channels:{num_channels}")
        logger.debug(f"load_and_preprocess_image:im.shape:{im.shape}")
    else:
        im = cv2.imread(im_path, num_channels)
        logger.debug(f"load_and_preprocess_image:number of channels:{num_channels}")
        logger.debug(f"load_and_preprocess_image:im.shape:{im.shape}")

    if im is None:
        logger.error("Error loading image.")
        raise ValueError("Error loading image")

    if num_channels != 1:
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    else:
        im_gray = im

    logger.debug(f"load_and_preprocess_image:im_gray.shape:{im_gray.shape}")

    # Crop image
    _, roiX, roiY, roiW, roiH = crop_to_petri(im_gray)
    logger.debug(
        f"load_and_preprocess_image:output crop_petri:{roiX = }\n{roiY = }\n{roiW = }\n{roiH = }"
    )
    logger.debug(
        f"load_and_preprocess_image:image slice:[{roiY}:{roiY + roiH}, {roiX}:{roiX + roiW}]"
    )

    # Pad image
    im = im[roiY : roiY + roiH, roiX : roiX + roiW]

    padded_im = padder(im, patch_size)

    logger.debug(
        f"load_and_preprocess_image:im.shape:after ROI extraction & padder:{im.shape}"
    )

    if scaling_factor != 1:
        logger.info(f"Scaling image by a factor of {scaling_factor}.")
        padded_im = cv2.resize(padded_im, (0, 0), fx=scaling_factor, fy=scaling_factor)

    logger.debug(f"{len((patch_size, patch_size) * im.ndim)} - {im.ndim}")
    # if num_channels == 1 and padded_im.ndim == 2:
    #     padded_im = np.expand_dims(padded_im, axis=-1)

    # Create patches
    try:
        patches = patchify(padded_im, (patch_size, patch_size), step=patch_size)
    except ValueError as e:
        logger.error(f"Error in patchify: {e}")
        logger.debug(
            f"Image shape for patchify: {padded_im.shape}, Patch shape: {(patch_size, patch_size, num_channels)}"
        )
        raise

    logger.debug(f"load_and_preprocess_iamge:patches.shape:{patches.shape}")

    i = patches.shape[0]
    j = patches.shape[1]

    patches = patches.reshape(-1, patch_size, patch_size, 1)
    logger.debug(f"load_and_preprocess_image:reshaped patches:{patches.shape}")

    return patches, i, j, padded_im


def postprocess_prediction(
    preds: np.ndarray,
    i: int,
    j: int,
    im: np.ndarray,
    threshold: float = 0.8,
    patch_size: int = 256,
) -> np.ndarray[int]:
    """
    Post-process the model's predictions to create a final mask.

    Parameters:
        - preds (np.ndarray): Predictions from the model.
        - i (int): Number of patches in the vertical dimension.
        - j (int): Number of patches in the horizontal dimension.
        - im (np.ndarray): Original image.
        - threshold (float): Threshold value for binarizing the mask. Default is 0.8.
        - patch_size (int): Size of the patches. Default is 256.

    Returns:
        - np.ndarray: Post-processed binary mask.
    """

    logger.info("Starting post-processing of predictions.")

    # Reshape predictions
    preds = preds.reshape(i, j, patch_size, patch_size)

    # Slice predictions
    predicted_mask = unpatchify(preds, (im.shape[0], im.shape[1]))
    predicted_mask = np.where(predicted_mask > threshold, 1, 0)

    # Log successful
    logger.info("Post-processing completed.")
    return predicted_mask


def predict(
    model: keras.models.Model,
    im_path: str,
    save_path: str = "Predictions/Image.png",
    patch_size: int = 256,
    threshold: float = 0.8,
    scaling_factor: float = 1,
    num_channels: int = 1,
    models_path: str = "./models",
) -> Tuple[np.ndarray[int], float]:
    """
    Predict and post-process the mask for the given image.

    Parameters:
        - model (Model): Trained Keras model for prediction.
        - im_path (str): Path to the input image.
        - save_path (str): Path to save the predicted mask. Default is "Predictions/Image.png".
        - patch_size (int): Size of the patches. Default is 256.
        - threshold (float): Threshold value for binarizing the mask. Default is 0.8.
        - scaling_factor (float): Scaling factor for the image. Default is 1.
        - num_channels (int): Number of channels for the image (1 for grayscale, 3 for color). Default is 1.
        - models_path (str): Path to models directory. Default is "./models"

    Returns:
        - np.ndarray: Predicted binary mask.
        - float: Mean confidence score of prediction
    """

    logger.info(f"Loading and preprocessing image from path: {im_path}")

    # Preprocess image
    patches, i, j, im = load_and_preprocess_image(
        im_path, patch_size, scaling_factor, num_channels
    )

    logger.info("Image preprocessing completed. Starting prediction.")

    # Predict
    preds = model.predict(patches / 255)

    # Calculate mean confidence score
    mean_conf_score = mean_confidence_score(preds, threshold)

    logger.info("Prediction completed. Starting post-processing.")

    # Postprocess prediction
    predicted_mask = postprocess_prediction(preds, i, j, im, threshold, patch_size)

    logger.info(f"Saving predicted mask to: {save_path}")

    # Save predicted mask
    cv2.imwrite(
        save_path, predicted_mask.astype(np.uint8) * 255
    )  # Convert binary mask to uint8 image

    logger.info("Predicted mask saved successfully.")
    return predicted_mask, mean_conf_score


# Example usage
# Define a dummy model for demonstration purposes (replace with actual model)
# class DummyModel:
#     def predict(self, patches):
#         # Dummy prediction logic
#         return np.random.rand(*patches.shape)

# model = DummyModel()
# image_path = 'path_to_your_image.png'
# save_path = 'Predictions/Image.png'

# predicted_mask = predict(model, image_path, save_path)


def main():
    parser = argparse.ArgumentParser(
        description="Predict a root mask from an image using a trained model."
    )
    parser.add_argument("--image_path", type=str, help="Path to the input image file.")
    parser.add_argument(
        "--save_path", type=str, help="Where to save the predicted mask."
    )
    parser.add_argument(
        "-m",
        "--name_model",
        type=str,
        default="main",
        action="store",
        help="What model name to use. Default is main.",
    )
    parser.add_argument(
        "-p",
        "--patch_size",
        # dest = "patch_size",
        type=int,
        default=256,
        action="store",
        help="How to patch the images for prediction. Default: 256.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        # dest = "threshold",
        type=float,
        default=0.8,
        action="store",
        help="Threshold for the predicted mask. Defult: 0.8.",
    )
    parser.add_argument(
        "-s",
        "--scaling_factor",
        # dest = "scaling_factor",
        type=int,
        default=1,
        action="store",
        help="Scaling factor for the image. Default: 1",
    )
    parser.add_argument(
        "-n",
        "--num_channels",
        # dest = "num_channels",
        type=int,
        choices=[1, 3],
        default=1,
        action="store",
        help="Number of channels to use with image. Default: 1",
    )
    parser.add_argument(
        "--expected_nr_plants",
        # dest = "expected_nr_plants",
        type=int,
        default=5,
        action="store",
        help="Number of expected plant roots in the image. Default: 5",
    )
    parser.add_argument(
        "--models_path",
        type=str,
        default="./models",
        help="Path to models direcotry. Defautl is './modles'",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Load the pretrained model
    with custom_object_scope({"f1": f1, "iou": iou}):
        model = load_model(f"{args.models_path}/{args.model}.keras")

    # Predict the mask
    predicted_mask, mean_conf_score = predict(
        model,
        args.image_path,
        args.save_path,
        args.patch_size,
        args.threshold,
        args.scaling_factor,
        args.num_channels,
        args.model_path,
    )

    # Postprocess the image to get info about roots
    root_lengths, root_tip_coords, marked_image = process_image_for_roots(
        predicted_mask, args.expected_nr_plants
    )
    # Log the details
    logger.info(f"Mean confidence score: {mean_conf_score}")
    logger.info(f"Root lengths: {root_lengths}")
    logger.info(f"Root tips coordinates in image (px): {root_tip_coords}")

    # Save the marked mask
    cv2.imwrite(args.save_path, marked_image)


if __name__ == "__main__":
    main()
