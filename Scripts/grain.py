import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def apply_grain_effect(image, grain_intensity):
    # Convert image to numpy array
    img_array = np.array(image)

    # Generate random noise with the same size as the image
    noise = np.random.randint(-grain_intensity, grain_intensity, size=img_array.shape, dtype='int')

    # Add noise to the image
    noisy_image = np.clip(img_array + noise, 0, 255).astype('uint8')

    # Convert back to PIL image
    noisy_pil_image = Image.fromarray(noisy_image)
    return noisy_pil_image

input_image_path = "/Users/felipebandeira/Desktop/test/licenses/generated_license_1.png"
grain_intensity = 100  # Intensity of the grain effect (adjust as needed)

# Open the input image using PIL
image = Image.open(input_image_path)

# Apply the grain effect
noisy_image = apply_grain_effect(image, grain_intensity)

# Plot the images using matplotlib
plt.figure(figsize=(10, 5))

# Plot the original image
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")

# Plot the image with grain effect
plt.subplot(1, 2, 2)
plt.imshow(noisy_image)
plt.title("Image with Grain Effect")
plt.axis("off")

plt.show()
