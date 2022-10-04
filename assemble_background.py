import cv2
import numpy as np

image_path = r"C:\Users\logan\PycharmProjects\Space_Arcade\Assets\asteroid_belt.png"
Image_Path = r"C:\Users\logan\PycharmProjects\Space_Arcade\Assets\foreground.png"
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
# img = np.array([[1,2,3],[4,5,6]])

height = img.shape[0]
width = img.shape[1]

Height = height * 3
Width = width * 3

Img = np.zeros((Height, Width, 4))

for i in range(Height):
    for j in range(Width):
        Img[i, j, :] = img[i % height, j % width]

cv2.imwrite(Image_Path, Img)


