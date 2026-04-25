import cv2
import pandas as pd
import numpy as np
import time

# --- Configuration and Setup ---
CSV_PATH = 'colors.csv'
IMAGE_PATH = 'pallete.jpg'

try:
    # Load and enhance image clarity
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        raise FileNotFoundError
    img = cv2.resize(img, (700, 500))
    # Apply professional detail enhancement
    img = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
except:
    # Fallback if image file is missing
    img = np.zeros((500, 700, 3), dtype=np.uint8)
    cv2.putText(img, "Image Not Found", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Global State Management
img_original = img.copy()
csv_data = pd.read_csv(CSV_PATH, names=["c", "name", "hex", "R", "G", "B"], header=None)
palette_bgr = csv_data[['B', 'G', 'R']].to_numpy()
x_mouse = y_mouse = 0
window_name = 'Color Detection & Morph Project'

def get_procedural_target(char, shape=(500, 700, 3)):
    """Generates procedural canvases based on keyboard input."""
    canvas = np.zeros(shape, dtype=np.uint8)
    h, w = shape[:2]
    cx, cy = w // 2, h // 2
    char = char.lower()

    if char == 'a': # Apple (with Glint & Leaf)
        cv2.ellipse(canvas, (cx, cy+20), (120, 100), 0, 0, 360, (0, 0, 200), -1) # Body
        cv2.circle(canvas, (cx-40, cy-20), 15, (100, 100, 255), -1) # Glossy highlight
        cv2.line(canvas, (cx, cy-80), (cx+20, cy-130), (20, 50, 100), 10) # Stem
        cv2.ellipse(canvas, (cx+30, cy-110), (40, 20), -30, 0, 360, (0, 180, 0), -1) # Green Leaf
    elif char == 'b': # Shiny Ball
        cv2.circle(canvas, (cx, cy), 150, (200, 0, 0), -1) # Blue body
        cv2.circle(canvas, (cx-50, cy-50), 40, (255, 150, 150), -1) # 3D highlight
    elif char == 'c': # Car (with Windows & Headlights)
        cv2.rectangle(canvas, (cx-150, cy), (cx+150, cy+80), (0, 0, 150), -1) # Body
        cv2.rectangle(canvas, (cx-80, cy-60), (cx+80, cy), (255, 200, 150), -1) # Window/Cabin
        cv2.circle(canvas, (cx-90, cy+80), 40, (30, 30, 30), -1) # Wheels
        cv2.circle(canvas, (cx+90, cy+80), 40, (30, 30, 30), -1)
        cv2.rectangle(canvas, (cx-160, cy+10), (cx-145, cy+30), (100, 255, 255), -1) # Headlight
    elif char == 'd': # Donut (with Sprinkles!)
        cv2.circle(canvas, (cx, cy), 140, (50, 100, 180), -1) # Dough
        cv2.circle(canvas, (cx, cy), 120, (150, 100, 255), -1) # Frosting
        # Add random colorful sprinkles
        for i in range(15):
            sx, sy = cx + np.random.randint(-80, 80), cy + np.random.randint(-80, 80)
            cv2.circle(canvas, (sx, sy), 5, (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), -1)
        cv2.circle(canvas, (cx, cy), 40, (0, 0, 0), -1) # Hole
    elif char == 'e': # Egg
        cv2.ellipse(canvas, (cx, cy), (80, 110), 0, 0, 360, (230, 240, 255), -1)
        cv2.circle(canvas, (cx-20, cy-40), 10, (255, 255, 255), -1) # Glint
    elif char == 'f': # Flower
        cv2.circle(canvas, (cx, cy), 40, (0, 255, 255), -1)
        for i in range(0, 360, 45):
            rad = np.deg2rad(i)
            px, py = int(cx + 80*np.cos(rad)), int(cy + 80*np.sin(rad))
            cv2.circle(canvas, (px, py), 45, (150, 100, 255), -1)
    elif char == 'g': # Grapes (Juicy)
        for x in range(-2, 3):
            for y in range(0, 4):
                gx, gy = cx + x*40 + abs(y)*10, cy + y*50
                cv2.circle(canvas, (gx, gy), 30, (150, 0, 100), -1)
                cv2.circle(canvas, (gx-10, gy-10), 8, (200, 100, 150), -1) # Shine
    elif char == 'h': # Glowing Heart
        pts = np.array([[cx, cy+100], [cx-120, cy-50], [cx-60, cy-120], [cx, cy-50], [cx+60, cy-120], [cx+120, cy-50]], np.int32)
        cv2.fillPoly(canvas, [pts], (50, 50, 255))
        cv2.ellipse(canvas, (cx-40, cy-60), (30, 15), 30, 0, 360, (150, 150, 255), -1) # Highlight
    elif char == 'i': # Ice Cream (with Cherry!)
        cv2.fillPoly(canvas, [np.array([[cx, cy+150], [cx-80, cy], [cx+80, cy]])], (50, 120, 200)) # Cone
        cv2.circle(canvas, (cx, cy-20), 80, (200, 240, 255), -1) # Scoop
        cv2.circle(canvas, (cx, cy-100), 25, (30, 30, 220), -1) # Cherry
        cv2.line(canvas, (cx, cy-100), (cx+10, cy-130), (50, 100, 50), 3) # Stem
    else: # Default Star
        pts = np.array([[cx, cy-150], [cx+40, cy-40], [cx+150, cy-40], [cx+60, cy+30], [cx+100, cy+140], [cx, cy+70], [cx-100, cy+140], [cx-60, cy+30], [cx-150, cy-40], [cx-40, cy-40]], np.int32)
        cv2.fillPoly(canvas, [pts], (0, 255, 255))
    return canvas

def pixelate_and_quantize(image):
    """Transforms image into a blocky, color-quantized version."""
    h, w = image.shape[:2]
    # Downsample to a 35x25 grid
    small = cv2.resize(image, (35, 25), interpolation=cv2.INTER_AREA)
    pixels = small.reshape(-1, 3).astype(np.float32)
    # Calculate Euclidean distance to each color in our dataset
    dists = np.sum((pixels[:, np.newaxis, :] - palette_bgr[np.newaxis, :, :]) ** 2, axis=2)
    min_indices = np.argmin(dists, axis=1)
    quantized = palette_bgr[min_indices].astype(np.uint8).reshape(25, 35, 3)
    # Upscale back to window size using nearest-neighbor
    return cv2.resize(quantized, (w, h), interpolation=cv2.INTER_NEAREST)

def draw_ui_overlay(frame, x, y):
    """Draws color identification tooltip near the cursor."""
    h_f, w_f = frame.shape[:2]
    safe_y, safe_x = np.clip(y, 0, h_f-1), np.clip(x, 0, w_f-1)
    b, g, r = [int(c) for c in frame[safe_y, safe_x]]
    
    # Identify the closest named color
    dists = (csv_data['R']-r)**2 + (csv_data['G']-g)**2 + (csv_data['B']-b)**2
    color_name = csv_data.loc[dists.idxmin(), 'name']
    text = f"{color_name} (R:{r} G:{g} B:{b})"
    
    # UI Positioning logic
    tw, th = cv2.getTextSize(text, 2, 0.6, 1)[0]
    tx, ty = x + 20, y - 20
    if tx + tw + 50 > w_f: tx = x - tw - 50
    if ty - th - 10 < 0: ty = y + th + 20
    
    # Draw text box and color preview
    cv2.rectangle(frame, (tx, ty-th-10), (tx+tw+40, ty+10), (255, 255, 255), -1)
    cv2.rectangle(frame, (tx, ty-th-10), (tx+tw+40, ty+10), (0, 0, 0), 1)
    cv2.putText(frame, text, (tx+5, ty), 2, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.rectangle(frame, (tx+tw+10, ty-th-2), (tx+tw+30, ty+2), (b, g, r), -1)
    cv2.rectangle(frame, (tx+tw+10, ty-th-2), (tx+tw+30, ty+2), (0, 0, 0), 1)

def mouse_callback(event, x, y, flags, param):
    global x_mouse, y_mouse
    x_mouse, y_mouse = x, y

# --- Main Application Loop ---
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_callback)

print("Project Active. Controls: A-I (Shapes), R (Reset), ESC (Quit)")

while True:
    display_frame = img.copy()
    draw_ui_overlay(display_frame, x_mouse, y_mouse)
    cv2.imshow(window_name, display_frame)
    
    key = cv2.waitKey(20) & 0xFF
    if key == 27: # Exit
        break
    elif key == ord('r'): # Smooth Reset
        start, end = img.copy().astype(np.float32), img_original.copy().astype(np.float32)
        for i in range(16):
            img = cv2.addWeighted(start, 1.0 - i/15.0, end, i/15.0, 0).astype(np.uint8)
            cv2.imshow(window_name, img); cv2.waitKey(10)
    elif ord('a') <= key <= ord('z') and key != ord('r'):
        # Smooth Morph to Target Shape
        target = pixelate_and_quantize(get_procedural_target(chr(key)))
        start, end = img.copy().astype(np.float32), target.astype(np.float32)
        for i in range(26):
            img = cv2.addWeighted(start, 1.0 - i/25.0, end, i/25.0, 0).astype(np.uint8)
            cv2.imshow(window_name, img); cv2.waitKey(15)

cv2.destroyAllWindows()