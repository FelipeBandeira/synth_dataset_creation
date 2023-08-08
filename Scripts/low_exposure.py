import cv2
import numpy as np
import random
import os

def apply_random_low_exposure(image):

    # Defines range of possible exposures
    possibilities = [0.5, 0.6, 0.7, 0.8, 0.9]

    # Samples factors randomly
    brightness_factor = random.choice(possibilities)
    contrast_factor = random.choice(possibilities)

    # Applies brightness adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)

    # Applies contrast adjustment
    adjusted_image = np.clip(adjusted_image * contrast_factor, 0, 255).astype(np.uint8)

    return adjusted_image


input_folder = "/Users/felipebandeira/Desktop/test/blurred"
output_folder = "/Users/felipebandeira/Desktop/test/low_exposure"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of image file names from the input folder
image_files = [file for file in os.listdir(input_folder) if file.lower().endswith((".jpg", ".jpeg", ".png"))]

# Loop through the selected images, apply blur, and save the results to the output folder
for image_file in image_files:
    input_image_path = os.path.join(input_folder, image_file)
    output_image_path = os.path.join(output_folder, image_file)

    # Read the input image
    image = cv2.imread(input_image_path)

    if random.random() < 0.8:
        # Apply random blur effect
        modified_image = apply_random_low_exposure(image)
        # Save the blurred image to the output folder
        cv2.imwrite(output_image_path, modified_image)
    
    else:
        cv2.imwrite(output_image_path, image)
