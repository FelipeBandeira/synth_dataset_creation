import os
import random
import cv2
#import numpy as np

def apply_random_blur(image):
    # Defines possible values for the blur
    blur_values = [5, 7, 9, 11, 13, 15]

    # Generate a random blur amount between 1 and max_blur_amount
    blur_amount = random.choice(blur_values)

    # Apply random blur effect
    blurred_image = cv2.GaussianBlur(image, (blur_amount, blur_amount), 0)
    return blurred_image

input_folder = "/Users/felipebandeira/Desktop/test/licenses"
output_folder = "/Users/felipebandeira/Desktop/test/blurred"

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
        blurred_image = apply_random_blur(image)

        # Save the blurred image to the output folder
        cv2.imwrite(output_image_path, blurred_image)
    else:
        cv2.imwrite(output_image_path, image)

