import numpy as np
import cv2

img = np.zeros((500, 700, 3), dtype=np.uint8)
target = np.ones((500, 700, 3), dtype=np.uint8) * 255
mask = np.random.rand(500, 700, 1)

try:
    current_blend = np.where(mask < 0.5, target, img)
    print(current_blend.dtype)
    temp_blend = current_blend.copy()
    cv2.rectangle(temp_blend, (0, 0), (10, 10), (255, 255, 255), -1)
    print("Success")
except Exception as e:
    print(f"Crash: {e}")
