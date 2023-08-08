import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import random
import os

def apply_random_low_exposure(image):

    # Defines range of possible exposures
    possibilities = [0.5, 0.6, 0.7, 0.8, 0.9]

    # Samples parameters randomly
    brightness_factor = random.choice(possibilities)
    contrast_factor = random.choice(possibilities)

    # Applies brightness adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)

    # Applies contrast adjustment
    adjusted_image = np.clip(adjusted_image * contrast_factor, 0, 255).astype(np.uint8)

    return adjusted_image

def apply_grain_effect(image):

    grain_range = [30, 40, 50, 60, 70, 80, 90]
    grain_intensity = random.choice(grain_range)

    # Convert image to numpy array
    img_array = np.array(image)

    # Generate random noise with the same size as the image
    noise = np.random.randint(-grain_intensity, grain_intensity, size=img_array.shape, dtype='int')

    # Add noise to the image
    noisy_image = np.clip(img_array + noise, 0, 255).astype('uint8')

    # Convert back to PIL image
    noisy_pil_image = Image.fromarray(noisy_image)
    
    return noisy_pil_image


input_folder = "/Users/felipebandeira/Desktop/test/blurred"
output_folder = "/Users/felipebandeira/Desktop/test/low_and_grained"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of image file names from the input folder
image_files = [file for file in os.listdir(input_folder) if file.lower().endswith((".jpg", ".jpeg", ".png"))]

# Loops through the selected images, applies effects, and saves the results to the output folder
for image_file in image_files:
    input_image_path = os.path.join(input_folder, image_file)
    output_image_path = os.path.join(output_folder, image_file)

    # Read the input image
    image = cv2.imread(input_image_path)

    random_1 = random.random()
    random_2 = random.random()

    if random_1 < 0.8:
        # Applies random low exposure effect
        modified_image = apply_random_low_exposure(image)

        if random_2 < 0.8:
            # Applies random grain effect
            grained_image = apply_grain_effect(modified_image)
            grained_image = np.array(grained_image) # converts back to numpy array so that we can use cv2.imwrite()
            cv2.imwrite(output_image_path, grained_image)
        else:
            # Saves the low light image to the output folder
            cv2.imwrite(output_image_path, modified_image)
    
    else:
        cv2.imwrite(output_image_path, image)