import cv2
import numpy as np
import matplotlib.pyplot as plt

imgFront = cv2.imread('/Users/felipebandeira/Desktop/test/Figure_1.png')
imgBack = cv2.imread('/Users/felipebandeira/Desktop/test/pexels-josh-sorenson-139303.jpg')

height, width = imgFront.shape[:2]

resizeBack = cv2.resize(imgBack, (width, height), interpolation=cv2.INTER_CUBIC)

for i in range(width):
    for j in range(height):
        pixel = imgFront[j, i]
        if np.all(pixel == [0, 0, 0]):
            imgFront[j, i] = resizeBack[j, i]

# Plot the resulting image
plt.imshow(cv2.cvtColor(imgFront, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("Combined Image")
plt.show()