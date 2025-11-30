import cv2
import matplotlib.pyplot as plt


path ="image copy.png"

img = cv2.imread(path).astype('float32') / 255.0

# 2️⃣ OpenCV loads images in BGR order — we’ll plot each channel separately
colors = ('b', 'g', 'r')

# 3️⃣ Draw histogram for each channel
for i, color in enumerate(colors):
    hist = cv2.calcHist([img], [i], None, [256], [0, 1])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])

# 4️⃣ Add labels and show
plt.title('RGB Color Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Number of Pixels')
plt.show()
