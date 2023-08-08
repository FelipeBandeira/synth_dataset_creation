import os
from PIL import Image
import torchvision.transforms as T
import time

# Create the perspective transformer
perspective_transformer = T.RandomPerspective(distortion_scale=0.2, p=0.8)

# Sets paths for output and input folders
output_path = "/Users/felipebandeira/Desktop/test/warped"
input_path = "/Users/felipebandeira/Desktop/test/low_and_grained"

# Lists all files in input folder
files = os.listdir(input_path)

for file in files:
    # Creates final path for each image file
    input_image_path = os.path.join(input_path, file)
    
    # Loads image
    orig_img = Image.open(input_image_path)
    
    # Adds perspective effect
    modified_image = perspective_transformer(orig_img)
    
    # Builds output path for each file
    output_image_path = os.path.join(output_path, file)
    
    # Saves final image
    modified_image.save(output_image_path)