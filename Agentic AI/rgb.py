import numpy as np
from PIL import Image

# Make a simple 2x2 RGB image
data = np.array([
    [[255, 0, 0], [0, 255, 0]],   # Red, Green
    [[0, 0, 255], [255, 255, 0]]  # Blue, Yellow
], dtype=np.uint8)

img = Image.fromarray(data, 'RGB')
img.show()

print("Raw array shape:", data.shape)
print("Raw values:\n", data)
