import cv2
import pandas as pd
import numpy as np
import os
import ctypes

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
CSV_PATH = 'colors.csv'
IMAGE_PATH = 'pallete.jpg'
WINDOW_NAME = 'Color Detection & Morph Project'
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
DISPLAY_SIZE = (700, 500)

# Virtual Key Codes for Shift Keys (Windows)
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1

# ==========================================
# GLOBAL STATE
# ==========================================
# Load Color Dataset
df = pd.read_csv(CSV_PATH, names=["c", "name", "hex", "R", "G", "B"], header=None)
palette_bgr = df[['B', 'G', 'R']].to_numpy()

# Image and View State
img = None
img_original = None
image_files = []
current_img_idx = 0

zoom_scale = 1.0
pan_x, pan_y = 0, 0
is_panning = False
last_mouse_pos = (0, 0)
x_mouse, y_mouse = 0, 0

# Sidebar and UI State
sidebar_scroll = 0
majority_colors = []
prev_lshift = False
prev_rshift = False

# ==========================================
# CORE UTILITY FUNCTIONS
# ==========================================

def get_image_files():
    """Scans the directory for valid image files."""
    return sorted([f for f in os.listdir('.') if f.lower().endswith(IMAGE_EXTENSIONS)])

def is_key_pressed(vk):
    """Detects if a physical key is held down (Windows Only)."""
    try:
        return ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000
    except:
        return False

def resize_and_pad(image, target_size=DISPLAY_SIZE):
    """Resizes image to fit window while preserving aspect ratio."""
    h, w = image.shape[:2]
    tw, th = target_size
    scale = min(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (nw, nh))
    canvas = np.zeros((th, tw, 3), dtype=np.uint8)
    canvas[(th - nh) // 2 : (th - nh) // 2 + nh, (tw - nw) // 2 : (tw - nw) // 2 + nw] = resized
    return canvas

def update_color_palette(image):
    """Finds the most frequent colors in the image for the sidebar."""
    global majority_colors
    # Quantize to find dominant colors efficiently
    small = cv2.resize(image, (35, 25), interpolation=cv2.INTER_AREA)
    pixels = small.reshape(-1, 3).astype(np.float32)
    distances = np.sum((pixels[:, np.newaxis, :] - palette_bgr[np.newaxis, :, :]) ** 2, axis=2)
    nearest_indices = np.argmin(distances, axis=1)
    colors, counts = np.unique(palette_bgr[nearest_indices], axis=0, return_counts=True)
    majority_colors = colors[np.argsort(-counts)][:35]

def get_procedural_shape(char):
    """Generates a highly detailed colorful shape based on the key pressed (A-I, M)."""
    canvas = np.zeros((DISPLAY_SIZE[1], DISPLAY_SIZE[0], 3), dtype=np.uint8)
    cx, cy = DISPLAY_SIZE[0] // 2, DISPLAY_SIZE[1] // 2
    c = char.lower()
    
    if c == 'a': # Detailed Apple
        cv2.ellipse(canvas, (cx, cy + 20), (120, 100), 0, 0, 360, (0, 0, 220), -1)
        cv2.circle(canvas, (cx - 45, cy - 20), 20, (150, 150, 255), -1)
        cv2.line(canvas, (cx, cy - 80), (cx + 20, cy - 130), (30, 80, 140), 12)
        cv2.ellipse(canvas, (cx + 35, cy - 115), (45, 25), -30, 0, 360, (0, 220, 0), -1)
    elif c == 'b': # Shiny Ball
        cv2.circle(canvas, (cx, cy), 155, (220, 0, 0), -1)
        cv2.circle(canvas, (cx - 60, cy - 60), 55, (255, 180, 180), -1)
    elif c == 'c': # Car
        cv2.rectangle(canvas, (cx - 160, cy), (cx + 160, cy + 90), (180, 0, 0), -1)
        cv2.rectangle(canvas, (cx - 95, cy - 70), (cx + 95, cy), (255, 220, 180), -1)
        cv2.circle(canvas, (cx - 100, cy + 90), 45, (40, 40, 40), -1)
        cv2.circle(canvas, (cx + 100, cy + 90), 45, (40, 40, 40), -1)
    elif c == 'd': # Donut with Sprinkles
        cv2.circle(canvas, (cx, cy), 145, (130, 180, 220), -1)
        cv2.circle(canvas, (cx, cy), 125, (180, 130, 255), -1)
        for _ in range(20):
            sx, sy = cx + np.random.randint(-80, 80), cy + np.random.randint(-80, 80)
            cv2.circle(canvas, (sx, sy), 6, (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), -1)
        cv2.circle(canvas, (cx, cy), 45, (0, 0, 0), -1)
    elif c == 'e': # Egg
        cv2.ellipse(canvas, (cx, cy), (110, 150), 0, 0, 360, (245, 255, 255), -1)
        cv2.circle(canvas, (cx - 35, cy - 50), 25, (255, 255, 255), -1)
    elif c == 'f': # Flower
        cv2.circle(canvas, (cx, cy), 60, (0, 255, 255), -1)
        for i in range(0, 360, 45):
            rad = np.deg2rad(i)
            cv2.circle(canvas, (int(cx + 95 * np.cos(rad)), int(cy + 95 * np.sin(rad))), 60, (160, 120, 255), -1)
    elif c == 'g': # Grapes
        cv2.line(canvas, (cx, cy - 110), (cx + 25, cy - 160), (30, 100, 30), 10)
        for i in range(-2, 3):
            for j in range(0, 4):
                cv2.circle(canvas, (cx + i * 48 + j * 12, cy + j * 55), 35, (150, 0, 120), -1)
    elif c == 'h': # Heart
        pts = np.array([[cx, cy + 130], [cx - 155, cy - 55], [cx - 85, cy - 135], [cx, cy - 55], [cx + 85, cy - 135], [cx + 155, cy - 55]], np.int32)
        cv2.fillPoly(canvas, [pts], (70, 70, 255))
        cv2.ellipse(canvas, (cx - 45, cy - 75), (35, 20), 30, 0, 360, (170, 170, 255), -1)
    elif c == 'i': # Ice Cream
        cv2.fillPoly(canvas, [np.array([[cx, cy + 160], [cx - 90, cy], [cx + 90, cy]])], (70, 140, 210))
        cv2.circle(canvas, (cx, cy - 40), 95, (230, 255, 255), -1)
        cv2.circle(canvas, (cx, cy - 115), 30, (50, 50, 240), -1)
    elif c == 'm': # Moon
        cv2.circle(canvas, (cx, cy), 165, (230, 255, 255), -1)
        cv2.circle(canvas, (cx + 75, cy - 55), 145, (0, 0, 0), -1)
    return canvas

def pixelate(image):
    """Returns a pixelated, quantized version of the input image."""
    h, w = image.shape[:2]
    small = cv2.resize(image, (35, 25), interpolation=cv2.INTER_AREA)
    pixels = small.reshape(-1, 3).astype(np.float32)
    distances = np.sum((pixels[:, np.newaxis, :] - palette_bgr[np.newaxis, :, :]) ** 2, axis=2)
    quantized = palette_bgr[np.argmin(distances, axis=1)].astype(np.uint8).reshape(25, 35, 3)
    return cv2.resize(quantized, (w, h), interpolation=cv2.INTER_NEAREST)

# ==========================================
# UI RENDERING FUNCTIONS
# ==========================================

def draw_interface(frame, mx, my):
    """Draws sidebar, navigation buttons, and color tooltip."""
    h, w = frame.shape[:2]
    font = 2 # DUPLEX
    
    # 1. Navigation Buttons
    for x_pos, label in [(60, "< PREV"), (w - 100, "NEXT >")]:
        cv2.rectangle(frame, (x_pos, 10), (x_pos + 90, 45), (40, 40, 40), -1)
        cv2.rectangle(frame, (x_pos, 10), (x_pos + 90, 45), (200, 200, 200), 1)
        cv2.putText(frame, label, (x_pos + 10, 33), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
    # 2. Scrollable Sidebar
    global sidebar_scroll
    sidebar_w = 46
    max_scroll = max(0, len(majority_colors) * 28 - (h - 100))
    sidebar_scroll = np.clip(sidebar_scroll, 0, max_scroll)
    cv2.rectangle(frame, (0, 0), (sidebar_w, h), (30, 30, 30), -1)
    cv2.rectangle(frame, (sidebar_w-1, 0), (sidebar_w, h), (80, 80, 80), -1)
    
    for i, color in enumerate(majority_colors):
        y = 70 + i * 28 - int(sidebar_scroll)
        if 55 < y < h - 30:
            c_tuple = tuple(int(x) for x in color)
            cv2.rectangle(frame, (12, y), (34, y + 22), c_tuple, -1)
            cv2.rectangle(frame, (12, y), (34, y + 22), (255, 255, 255), 1)
            
    # 3. Enhanced Color Tooltip
    sy, sx = np.clip(my, 0, h - 1), np.clip(mx, 0, w - 1)
    b, g, r = [int(x) for x in frame[sy, sx]]
    dist = (df['R'] - r)**2 + (df['G'] - g)**2 + (df['B'] - b)**2
    name = df.loc[dist.idxmin(), 'name']
    
    text = f"{name} ({r},{g},{b}) @ {mx},{my}"
    tw, th = cv2.getTextSize(text, font, 0.55, 1)[0]
    
    # Calculate position with robust clipping
    tx = mx + 20 if mx + tw + 85 < w else mx - tw - 85
    ty = my - 20 if my - 45 > 0 else my + 45
    
    # Final safety clip to ensure it stays inside the window
    tx = max(5, min(tx, w - tw - 70))
    ty = max(40, min(ty, h - 20))
    
    # Tooltip Background Box
    cv2.rectangle(frame, (tx, ty - th - 15), (tx + tw + 65, ty + 15), (255, 255, 255), -1)
    cv2.rectangle(frame, (tx, ty - th - 15), (tx + tw + 65, ty + 15), (0, 0, 0), 1)
    
    # Sample Color Square
    cv2.rectangle(frame, (tx + tw + 25, ty - th - 2), (tx + tw + 50, ty + 2), (b, g, r), -1)
    cv2.rectangle(frame, (tx + tw + 25, ty - th - 2), (tx + tw + 50, ty + 2), (0, 0, 0), 1)
    
    # Tooltip Text
    cv2.putText(frame, text, (tx + 10, ty), font, 0.55, (0, 0, 0), 1, cv2.LINE_AA)

# ==========================================
# MAIN APP FLOW
# ==========================================

def smooth_transition(target):
    """Morphs current image to target with a smooth fade effect."""
    global img
    start_f, end_f = img.copy().astype(np.float32), target.astype(np.float32)
    for i in range(16):
        alpha = i / 15.0
        img = cv2.addWeighted(start_f, 1 - alpha, end_f, alpha, 0).astype(np.uint8)
        display = img.copy()
        if zoom_scale > 1.0 or pan_x != 0 or pan_y != 0:
            M = np.float32([[zoom_scale, 0, pan_x], [0, zoom_scale, pan_y]])
            display = cv2.warpAffine(display, M, DISPLAY_SIZE, borderMode=cv2.BORDER_CONSTANT, borderValue=(20, 20, 20))
        draw_interface(display, x_mouse, y_mouse)
        cv2.imshow(WINDOW_NAME, display)
        cv2.waitKey(10)

def navigate(direction):
    """Switches to the next or previous image in the folder."""
    global current_img_idx, img_original, img, image_files, sidebar_scroll
    image_files = get_image_files()
    if not image_files: return
    current_img_idx = (current_img_idx + direction) % len(image_files)
    new_img = cv2.imread(image_files[current_img_idx])
    if new_img is not None:
        new_img = resize_and_pad(new_img)
        img_original = new_img.copy()
        update_color_palette(new_img)
        sidebar_scroll = 0
        smooth_transition(new_img)

def mouse_events(event, x, y, flags, param):
    """Handles click, drag, zoom, and sidebar scroll."""
    global x_mouse, y_mouse, zoom_scale, pan_x, pan_y, is_panning, last_mouse_pos, sidebar_scroll
    x_mouse, y_mouse = x, y
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
        if 60 <= x <= 150 and 10 <= y <= 45: navigate(-1)
        elif 600 <= x <= 690 and 10 <= y <= 45: navigate(1)
        else:
            is_panning, last_mouse_pos = True, (x, y)
    elif event in [cv2.EVENT_LBUTTONUP, cv2.EVENT_RBUTTONUP]:
        is_panning = False
    elif event == cv2.EVENT_MOUSEMOVE and is_panning:
        pan_x += (x - last_mouse_pos[0])
        pan_y += (y - last_mouse_pos[1])
        last_mouse_pos = (x, y)
    elif event == cv2.EVENT_MOUSEWHEEL:
        if x < 46: sidebar_scroll -= (flags / 8)
        else:
            old_z = zoom_scale
            zoom_scale = max(1.0, min(zoom_scale * (1.15 if flags > 0 else 0.87), 15.0))
            pan_x = x - (x - pan_x) * (zoom_scale / old_z)
            pan_y = y - (y - pan_y) * (zoom_scale / old_z)
            if 0.98 < zoom_scale < 1.02: zoom_scale, pan_x, pan_y = 1.0, 0, 0

# --- Initialization ---
image_files = get_image_files()
if IMAGE_PATH in image_files: current_img_idx = image_files.index(IMAGE_PATH)
img = cv2.imread(IMAGE_PATH)
img = resize_and_pad(img) if img is not None else np.zeros((500, 700, 3), np.uint8)
img_original = img.copy()
update_color_palette(img)

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_events)

while True:
    display_frame = img.copy()
    if zoom_scale > 1.0 or pan_x != 0 or pan_y != 0:
        M = np.float32([[zoom_scale, 0, pan_x], [0, zoom_scale, pan_y]])
        display_frame = cv2.warpAffine(display_frame, M, DISPLAY_SIZE, borderMode=cv2.BORDER_CONSTANT, borderValue=(20, 20, 20))
    
    draw_interface(display_frame, x_mouse, y_mouse)
    cv2.imshow(WINDOW_NAME, display_frame)
    
    l_held, r_held = is_key_pressed(VK_LSHIFT), is_key_pressed(VK_RSHIFT)
    if l_held and not prev_lshift: navigate(-1)
    if r_held and not prev_rshift: navigate(1)
    prev_lshift, prev_rshift = l_held, r_held
    
    key = cv2.waitKey(30) & 0xFF
    if key == 27: break
    elif key == ord('r'):
        zoom_scale, pan_x, pan_y, sidebar_scroll = 1.0, 0, 0, 0
        update_color_palette(img_original)
        smooth_transition(img_original)
    elif ord('a') <= key <= ord('i') or key == ord('m'):
        target = pixelate(get_procedural_shape(chr(key)))
        update_color_palette(target)
        smooth_transition(target)

cv2.destroyAllWindows()
