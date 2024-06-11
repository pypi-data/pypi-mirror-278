#!/bin/python3
import argparse
import glob
import os
import random
from typing import List, Tuple

import cv2
import numpy as np
from patchify import patchify
# from tensorflow.keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import Sequence

try:
    # Attempt relative imports (if run as a package module)
    from .utils import clear_destination_folder, setup_logger
except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from utils import clear_destination_folder, setup_logger

logger = setup_logger()


def compare_and_remove(folder1: str, folder2: str) -> None:
    """
    Compares files in two folders and removes files from the first folder
    that don't have corresponding matches in the second folder.

    Parameters:
        - folder1 (str): Path to the first folder containing files with extension .png.
        - folder2 (str): Path to the second folder containing files with various extensions such as '_root_mask.tif', '_occluded_root_mask.tif', '_shoot_mask.tif', '_seed_mask.tif'.

    Notes:
        - The function extracts filenames without extensions from folder1 and folder2.
        - It identifies files in folder1 that do not have corresponding matches in folder2.
        - Files without matches in folder2 are removed from folder1.
        - The function prints a message for each removed file.
    """

    # Get filenames in folder1 with extension .png
    png_files = [
        file.replace(".png", "")
        for file in os.listdir(folder1)
        if file.endswith(".png")
    ]
    logger.info(f"png_files lenght: {len(png_files)}")

    # Get filenames in folder2 with various extensions
    tif_files = [
        file.replace("_root_mask.tif", "")
        .replace("_occluded_root_mask.tif", "")
        .replace("_shoot_mask.tif", "")
        .replace("_seed_mask.tif", "")
        for file in os.listdir(folder2)
        if file.endswith(
            (
                "_root_mask.tif",
                "_occluded_root_mask.tif",
                "_shoot_mask.tif",
                "_seed_mask.tif",
            )
        )
    ]

    logger.info(f"tif_files lenght: {len(tif_files)}")

    # Find files that don't match
    files_to_remove = set(png_files) - set(tif_files)

    logger.info(
        f"Lenght files_to_remove: {len(files_to_remove)}\nFiles to remove: {files_to_remove}"
    )

    # Remove files from folder1
    for file_to_remove in files_to_remove:
        file_path = os.path.join(folder1, file_to_remove + ".png")
        os.remove(file_path)

        logger.info(f"Removed: {file_path}")


def crop_to_petri(im: np.ndarray) -> Tuple[np.ndarray, int, int, int, int]:
    """
    Detect and crop the petri dish from a grayscale image.

    Parameters:
        - im (np.ndarray): Input image (grayscale).

    Returns:
        - crop_im (np.ndarray): Cropped image containing the petri dish.
        - x (int): X-coordinate of the top-left corner of the petri dish ROI.
        - y (int): Y-coordinate of the top-left corner of the petri dish ROI.
        - w (int): Width of the petri dish ROI.
        - h (int): Height of the petri dish ROI.
    """
    logger.debug("Starting petri dish detection and cropping.")
    _, output_im = cv2.threshold(im, 100, 255, cv2.THRESH_BINARY)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(output_im)
    stats = stats[1:]
    max_area_index = np.argmax(stats[:, 4])
    x, y, w, h, _ = stats[max_area_index]
    side_length = min(w, h)
    x2 = x + side_length
    y2 = y + side_length
    crop_im = im[y:y2, x:x2]
    logger.debug("Petri dish cropping completed.")
    return crop_im, x, y, side_length, side_length
    # # Correct usage
    # image_path = 'youre_image_path_here'
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Ensure the image is read in grayscale

    # # Check if image was loaded successfully
    # if image is None:
    #     print("Error loading image")
    # else:
    #     cropped_image, x, y, w, h = crop_to_petri(image)
    #     print(f"Cropped region coordinates: x={x}, y={y}, width={w}, height={h}")
    #     # Optionally display the cropped image
    #     # cv2.imshow("Cropped Petri Dish", cropped_image)
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()

    # cropped_image.shape


def padder(image: np.ndarray, patch_size: int) -> np.ndarray:
    """
    Adds padding to an image to make its dimensions divisible by a specified patch size.

    This function calculates the amount of padding needed for both the height and width of an image
    so that its dimensions become divisible by the given patch size. The padding is applied evenly to both sides
    of each dimension (top and bottom for height, left and right for width). If the padding amount is odd,
    one extra pixel is added to the bottom or right side. The padding color is set to black (0, 0, 0).

    Parameters:
        - image (np.ndarray): The input image as a NumPy array. Expected shape is (height, width, channels).
        - patch_size (int): The patch size to which the image dimensions should be divisible. It's applied to both height and width.

    Returns:
        - np.ndarray: The padded image as a NumPy array with the same number of channels as the input.
          Its dimensions are adjusted to be divisible by the specified patch size.

    Example:
        - padded_image = padder(cv2.imread('example.jpg'), 128)
    """
    logger = setup_logger()
    logger.debug(
        f"Starting padding for image of shape {image.shape} to make dimensions divisible by {patch_size}."
    )

    h, w = image.shape[:2]
    height_padding = ((h // patch_size) + 1) * patch_size - h
    width_padding = ((w // patch_size) + 1) * patch_size - w

    top_padding = height_padding // 2
    bottom_padding = height_padding - top_padding

    left_padding = width_padding // 2
    right_padding = width_padding - left_padding

    logger.debug(
        f"Calculated padding: top={top_padding}, bottom={bottom_padding}, left={left_padding}, right={right_padding}"
    )

    padded_image = cv2.copyMakeBorder(
        image,
        top_padding,
        bottom_padding,
        left_padding,
        right_padding,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0],
    )

    logger.debug(f"Padding completed. New image shape is {padded_image.shape}.")

    return padded_image


def save_mask_patches(
    path: str,
    mask: np.ndarray,
    patch_size: int,
    root_path: str,
    subdir: str,
    patch_dir: str,
    dataset_type: str,
    i: int,
) -> None:
    """
    Supplemental function for patch_and_save.
    Creates and saves patches for a given mask image.

    Parameters:
        - path (str): Path to the original mask image file.
        - mask (numpy.ndarray): Mask image to create patches from.
        - patch_size (int): Size of the patches to be created.
        - subdir (str): Subdirectory within the dataset.
        - patch_dir (str): Directory where patches will be saved.
        - dataset_type (str): Type of the dataset (e.g., 'train', 'test').
        - i (int): Index used for saving numbered patches.

    Notes:
        - Utilizes the patchify method to create patches from the mask image.
        - Reshapes and saves patches to the specified patch directory with numbered filenames.
    """
    # Create patches for mask
    patches = patchify(mask, (patch_size, patch_size, 1), step=patch_size)
    patches = patches.reshape(-1, patch_size, patch_size, 1)

    # Make a correct path to save
    image_patch_path = path.replace(root_path, patch_dir)
    # image_patch_path = path
    image_patch_path = image_patch_path.replace(
        "masks/", dataset_type + "_masks/" + subdir + "/"
    )

    if i == 0:
        clear_destination_folder(image_patch_path)

    # print('mask save loacation: ' + image_patch_path)
    for j, patch in enumerate(patches):
        image_patch_path_numbered = f"{image_patch_path[:-4]}_{j}.tif"
        cv2.imwrite(image_patch_path_numbered, patch)


def process_image_and_mask(
    im_path: str,
    name_model: str,
    root_path: str,
    dataset_type: str,
    patch_size: int,
    patch_dir: str,
    i: int,
    scaling_factor: float,
    file_list: List[str],
    split: bool,
) -> None:
    """
    Used by patch_and_save, not ment to interact directly but possible to create
    own function based on this function.
    Process an image and its corresponding mask, create patches, and save them.

    Parameters:
        - im_path (str): Path to the original image file.
        - name_model (str): Name of the model or dataset.
        - dataset_type (str): Type of the dataset (e.g., 'train', 'test').
        - patch_size (int): Size of the patches to be created.
        - patch_dir (str): Directory where patches will be saved.
        - i (int): Index used for saving numbered patches.
        - scaling_factor (float): A factor to scale the images and masks.
        - file_list (list): List of file paths.

    Notes:
        - Loads image and masks, crops them to a petri dish area, and pads them to match patch size.
        - Rescales the images and masks if specified.
        - Creates patches for the image and saves them.
        - Reshapes the mask and passes it to save_mask_patches.

    Raises:
        ValueError: If either image fails to load.
    """

    # Extract image name by removing path and extension
    im_name = os.path.basename(im_path)
    im_name = im_name.replace(".png", "")

    # Get masks paths
    root_mask_path = root_path + name_model + "/masks/" + im_name + "_root_mask.tif"
    logger.debug(f"Processing image name: {im_name}")
    logger.debug(f"Processing root mask path: {root_mask_path}")
    logger.debug(f"Patch size: {patch_size}")

    # Load image and masks
    # Load grayscale for croping to petri dish
    im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
    root_mask = cv2.imread(root_mask_path, cv2.IMREAD_GRAYSCALE)

    # Check if the images were loaded successfully
    if im is None:
        raise ValueError(f"Failed to load image from path: {im_path}")
    if root_mask is None:
        raise ValueError(f"Failed to load root mask from path: {root_mask_path}")

    # Crop to petri dish using grayscale image
    _, roiX, roiY, roiW, roiH = crop_to_petri(im)
    # Crop image and masks to petri dish
    im = im[roiY : roiY + roiH, roiX : roiX + roiW]
    root_mask = root_mask[roiY : roiY + roiH, roiX : roiX + roiW]

    # Pad images and masks to be devidabe by patch size
    im = padder(im, patch_size)
    root_mask = padder(root_mask, patch_size)

    # Check if the shape of image and mask are corresponding
    if i == 0:
        if im.shape[0] == root_mask.shape[0] and im.shape[1] == root_mask.shape[1]:
            logger.info(f"Image size X: {im.shape[0]} Y: {im.shape[1]}")
            expected_files = (
                len(file_list) * (im.shape[0] / patch_size) * (im.shape[1] / patch_size)
            )

            logger.info(f"expected number of files: {expected_files}")
    elif i == 0:
        logger.error("ERROR: size don't match")
        return 1

    # Rescale if specified
    if scaling_factor != 1:
        logger.info(f"Rescaling with factor of {scaling_factor}")
        im = cv2.resize(im, (0, 0), fx=scaling_factor, fy=scaling_factor)
        root_mask = cv2.resize(root_mask, (0, 0), fx=scaling_factor, fy=scaling_factor)

    # Create patches for image
    patches = patchify(im, (patch_size, patch_size), step=patch_size)
    patches = patches.reshape(-1, patch_size, patch_size)

    # Save patches for image

    # TO-DO: Save in correct place
    # e.g. im_path: ../data/test/test/image.png
    # e.g. image_patch_path: ../data/test/test_images/test/image.png
    image_patch_path = im_path.replace(root_path, patch_dir)
    image_patch_path = image_patch_path.replace("\\", "/")

    # TO-DO: Fix path
    if split:
        image_patch_path = image_patch_path.replace(
            name_model + "/" + dataset_type + "/",
            name_model + "/" + dataset_type + "_images/" + dataset_type + "/",
        )
    else:
        image_patch_path = image_patch_path.replace(
            name_model + "/images/",
            name_model + "/" + dataset_type + "_images/" + dataset_type + "/",
        )

    logger.debug("Image patch path: " + image_patch_path)
    # print('=====')
    # print('original image path: ' + im_path)
    # print('name_model: ' + name_model)
    # print('dataset_type: ' + dataset_type)
    # print('image save location: ' + image_patch_path)
    if i == 0:
        clear_destination_folder(image_patch_path)

    for j, patch in enumerate(patches):
        image_patch_path_numbered = f"{image_patch_path[:-4]}_{j}.png"
        cv2.imwrite(image_patch_path_numbered, patch)

    # Reshape the mask
    root_mask = root_mask.reshape(root_mask.shape[0], root_mask.shape[1], 1)

    save_mask_patches(
        root_mask_path,
        root_mask,
        patch_size,
        root_path,
        "root",
        patch_dir,
        dataset_type,
        i,
    )
    return 0


def patch_and_save(
    name_model: str = "test",
    root_path: str = "./data/",
    patch_size: int = 256,
    scaling_factor: float = 1,
    patch_dir: str = "./data_patched/",
    test_split: float = 0.3,
    # uri: str = None,
    # azure: bool = False # OUTPUT
) -> None:
    """
    Generate and save patches for images and corresponding masks.

    Parameters:
        - name_model (str): Name of the model or dataset.
        - root_path (str): Path to the root of data folder.
        - patch_size (int): Size of the patches to be created.
        - scaling_factor (float): A factor to scale the images and masks.
        - patch_dir (str): Directory to save the patched images.
        - test_split (float): A split for test dataset if not split into train/test before upload.

    Returns:
        0 if the process is succesfull, 1 if an error occurs

    Note:
        This function assumes a specific dataset structure with separate subdirectories for images and masks.

    .. code-block::

        data/
        │
        ├── train/
        │   ├── Image1.png
        │   ├── Image2.png
        │   └── ...
        ├── test/
        │   ├── Image1.png
        │   ├── Image2.png
        │   └── ...
        └── masks/
            ├── Mask1_root_mask.tif
            ├── Mask1_shoot_mask.tif
            ├── ...
            ├── Mask2_root_mask.tif
            ├── Mask2_shoot_mask.tif
            └── ...

    The generated image and mask patches are saved in the specified patch_dir.

    """
    # ------------------------------------- #
    # TO-DO: Load data as separate function #
    # ------------------------------------- #
    # Get all image names in train_images
    folder_list = glob.glob(root_path + name_model + "/*")
    abs_folder_list = [os.path.abspath(folder) for folder in folder_list]
    # logger.info(f'Exploring {abs_folder_list} for images and masks folders')
    logger.info(f"Exploring {folder_list} for images and masks folders")

    folder_list = [file.replace("\\", "/") for file in folder_list]

    folder_list = [
        file.replace(root_path + name_model + "/", "") for file in folder_list
    ]

    logger.debug(folder_list)
    valid_names_train_test = ["train", "test", "masks"]
    valid_names_images_masks = ["masks", "images"]

    # Detect folder structure and separate files into train and test
    if all(name in folder_list for name in valid_names_train_test):
        # log("detected train, test, and masks.")
        logger.info("Processing pre-split dataset")

        train_folder = root_path + name_model + "/train"
        test_folder = root_path + name_model + "/test"
        masks_folder = root_path + name_model + "/masks"

        logger.info("Cleaining folders")
        compare_and_remove(train_folder, masks_folder)
        compare_and_remove(test_folder, masks_folder)
        logger.info("Folders cleaned")
        # Get a list of all files for train and test
        # Masks will be handled later alongside images
        train_file_list = glob.glob(train_folder + "/*")
        test_file_list = glob.glob(test_folder + "/*")
        split = True

    elif all(name in folder_list for name in valid_names_images_masks):
        # log("detected masks and images.")
        logger.info("Processing not pre-split dataset")
        images_folder = root_path + name_model + "/images"
        masks_folder = root_path + name_model + "/masks"

        logger.info("Cleaning folders")
        compare_and_remove(images_folder, masks_folder)
        logger.info("Folders cleaned")

        file_list = glob.glob(images_folder + "/*")

        # Get number of items to split into train/test
        num_files = len(file_list)
        logger.debug(f"Number of files in images folder: {num_files}")
        logger.debug(f"Test split: {test_split}")
        test_split_number = int(num_files * test_split)

        # Get test split
        test_file_list = random.sample(file_list, test_split_number)
        # Get train split, left over from test split
        train_file_list = [file for file in file_list if file not in test_file_list]
        split = False

    else:
        print("The file names do not match the expected pattern.")
        logger.info("The file names do not match the expected pattern.")

        return 1
    # ------------------------------------- #
    # TO-DO: Load data as separate function #
    # ------------------------------------- #
    logger.info("Processing train")
    i = 0
    for im_path in train_file_list:
        response = process_image_and_mask(
            im_path,
            name_model,
            root_path,
            "train",
            patch_size,
            patch_dir,
            i,
            scaling_factor,
            train_file_list,
            split,
        )
        if response == 1:
            return 1
        i += 1
    logger.info("Processing test")
    i = 0
    for im_path in test_file_list:
        response = process_image_and_mask(
            im_path,
            name_model,
            root_path,
            "test",
            patch_size,
            patch_dir,
            i,
            scaling_factor,
            train_file_list,
            split,
        )
        if response == 1:
            return 1
        i += 1
    # TO-DO: if azure and uri upload to uri
    return 0


class DataGenerator(Sequence):
    def __init__(self, image_gen, mask_gen):
        self.image_gen = image_gen
        self.mask_gen = mask_gen

    def __len__(self):
        return min(len(self.image_gen), len(self.mask_gen))

    def __getitem__(self, index):
        x = self.image_gen[index]
        y = self.mask_gen[index]
        return x[0], y[0]


def load_and_preprocess_data(
    classes: List[str],
    name_model: str = "test",
    patch_size: int = 256,
    patch_dir: str = "./data_patched/",
    seed: int = 42,
    batch_size: int = 16,
    image_color_mode: str = "grayscale",
) -> Tuple[DataGenerator, DataGenerator, int, int]:
    """
    Load and preprocess image and mask data for training and testing.

    Parameters:
        - classes (List[str]): List of class names for masks.
        - name_model (str): Name of the model or dataset. Default is "test".
        - patch_size (int): Size of the patches. Default is 256.
        - patch_dir (str): Directory containing image and mask patches. Default is "data_patched".
        - seed (int, optional): Seed for data generators. Default is 42.
        - batch_size (int): Batch size for the generators. Default is 16.
        - image_color_mode (str): Color mode for images. Default is 'grayscale'.

    Returns:
        Tuple[zip, zip, int, int]: A tuple containing:
            - train_generator: Training data generator (image and mask).
            - test_generator: Testing data generator (image and mask).
            - steps_per_epoch: Number of steps to be taken per epoch.
            - validation_steps: Number of steps to be taken for validation.

    Notes:
        - The function uses ImageDataGenerator to create data generators for image and mask patches.
        - Training and testing data generators are created for both images and masks.
    """

    logger.info("Initializing data generators for training and testing.")

    logger.debug("Creating ImageDataGenerator for training images.")
    train_image_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_image_generator = train_image_datagen.flow_from_directory(
        os.path.join(
            patch_dir,
            name_model,
            "train_images",
        ),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        color_mode=image_color_mode,
        seed=seed,
    )

    logger.debug("Creating ImageDataGenerator for training masks.")
    train_mask_datagen = ImageDataGenerator()

    train_mask_generator = train_mask_datagen.flow_from_directory(
        os.path.join(patch_dir, name_model, "train_masks"),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        classes=classes,
        color_mode="grayscale",
        seed=seed,
    )

    train_generator = DataGenerator(train_image_generator, train_mask_generator)

    logger.debug("Creating ImageDataGenerator for testing images.")
    test_image_datagen = ImageDataGenerator(rescale=1.0 / 255)

    test_image_generator = test_image_datagen.flow_from_directory(
        os.path.join(patch_dir, name_model, "test_images"),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        color_mode=image_color_mode,
        seed=seed,
    )

    logger.debug("Creating ImageDataGenerator for testing masks.")
    test_mask_datagen = ImageDataGenerator()

    test_mask_generator = test_mask_datagen.flow_from_directory(
        os.path.join(patch_dir, name_model, "test_masks"),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        classes=classes,
        color_mode="grayscale",
        seed=seed,
    )

    test_generator = DataGenerator(test_image_generator, test_mask_generator)

    steps_per_epoch = len(train_image_generator)
    validation_steps = test_image_generator.samples // batch_size

    logger.info(
        f"Data generators created successfully. Steps per epoch: {steps_per_epoch}, Validation steps: {validation_steps}"
    )

    return train_generator, test_generator, steps_per_epoch, validation_steps


def load_and_preprocess_image(
    im_path: str,
    patch_size: int = 256,
    scaling_factor: float = 1,
    num_channels: int = 1,
) -> Tuple[np.ndarray, int, int, np.ndarray]:
    """
    Load, crop, preprocess, and create patches from an image.

    Parameters:
        - im_path (str): Path to the image.
        - patch_size (int): Size of the patches to create.
        - scaling_factor (float): Scaling factor for the image.
        - num_channels (int): Number of channels for the image (1 for grayscale, 3 for color).

    Returns:
        - patches (np.ndarray): Patches created from the image.
        - i (int): Number of patches in the vertical dimension.
        - j (int): Number of patches in the horizontal dimension.
        - im (np.ndarray): Preprocessed image.
    """

    logger.info(f"Loading image from path: {im_path}")
    if num_channels == 1:
        im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
    else:
        im = cv2.imread(im_path, cv2.IMREAD_COLOR)

    if im is None:
        logger.error("Error loading image.")
        raise ValueError("Error loading image")

    if num_channels != 1:
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    else:
        im_gray = im

    logger.info("Cropping image to petri dish.")
    _, roiX, roiY, roiW, roiH = crop_to_petri(im_gray)
    cropped_im = im[roiX : roiX + roiW, roiY : roiY + roiH]

    logger.info("Padding cropped image.")
    padded_im = padder(cropped_im, patch_size)

    if scaling_factor != 1:
        logger.info(f"Scaling image by a factor of {scaling_factor}.")
        padded_im = cv2.resize(padded_im, (0, 0), fx=scaling_factor, fy=scaling_factor)

    logger.info("Creating patches from the padded image.")
    patches = patchify(padded_im, (patch_size, patch_size))
    i = patches.shape[0]
    j = patches.shape[1]
    patches = patches.reshape(-1, patch_size, patch_size, 1 if num_channels == 1 else 3)

    logger.info("Image preprocessing completed.")
    return patches, i, j, padded_im


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess data using predefinded folder struncture, /data/name_model/ train, test, masks or images, masks. If more flexible solution is needed please use process_image_and_mask function in this module to create a custom loop"
    )
    parser.add_argument(
        "name_model",
        default="test",
        help="Name of the model that data is being preprocessed.",
        type=str,
    )
    parser.add_argument(
        "-r",
        "--root_path",
        default="./data/",
        action="store",
        help="Path to the root of data folder. End with /.",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--patch_size",
        default=256,
        action="store",
        help="What patches to use douring preprocessing. Default is 256.",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--scaling_factor",
        default=1.0,
        action="store",
        help="Scaling factor of the images on the train and test dataset. Recommended 1",
        type=float,
    )
    parser.add_argument(
        "-d",
        "--patch_dir",
        default="./data_patched/",
        action="store",
        help="Root path for patched data for training. WARNING Changes to this variable may result in broken pipe. End with /.",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--test_split",
        default=0.3,
        action="store",
        help="Test split if the dataset is not alerady split into train and test dataset",
        type=float,
    )

    # TO-DO: Add azure and uri paths

    args = parser.parse_args()

    patch_and_save(
        args.name_model,
        args.root_path,
        args.patch_size,
        args.scaling_factor,
        args.patch_dir,
        args.test_split,
    )


if __name__ == "__main__":
    main()
