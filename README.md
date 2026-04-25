# Color Detection and Interactive Pixel Transition System
### Robotics & Drones Laboratory Project (22MEC37N)

## Project Overview
This application provides an interactive platform for color identification and procedural image transformation using the OpenCV library. Designed for the Robotics and Drones final project, it implements real-time color categorization and state-based image morphing using vectorized mathematical operations.

## Core Functionality
- **Color Identification**: Maps RGB pixel values to a dataset of 865 named colors using a 3D Euclidean distance algorithm.
- **Procedural Morphing**: Implements state-based transitions where the current frame morphs into a pixelated representation of selected shapes (A-I).
- **Image Quantization**: Transforms procedural drawings into a 35x25 quantized color grid to simulate low-resolution sensory data.
- **Linear Interpolation (LERP)**: All transitions are calculated using linear alpha-blending for smooth visual continuity.
- **Detail Enhancement**: Applies local contrast normalization and sharpening via `cv2.detailEnhance` for improved clarity.

## System Controls
| Key Input | Function |
| :--- | :--- |
| **A - I** | Trigger morph to procedural target (Apple, Ball, Car, Donut, Egg, Flower, Grapes, Heart, Ice Cream) |
| **R** | Execute reset transition back to the original image |
| **ESC** | Terminate application |
| **Mouse Hover** | Display real-time RGB values and nearest named color match |

## Technical Implementation

### Color Matching Algorithm
The system utilizes vectorized Euclidean distance calculations to find the nearest neighbor in the RGB color space:
$$d = \sqrt{(R_{target}-R_{data})^2 + (G_{target}-G_{data})^2 + (B_{target}-B_{data})^2}$$
This is implemented using NumPy to ensure O(1) identification latency relative to user interaction.

### Image Processing Pipeline
1. **Procedural Drawing**: Shapes are generated on a 700x500 canvas using OpenCV drawing primitives.
2. **Quantization**: The canvas is downsampled to a 35x25 grid, where each cell is assigned the nearest color from the `colors.csv` dataset.
3. **Transition Engine**: Frame-by-frame interpolation is managed via `cv2.addWeighted`, performing a 25-step transition over ~400ms.

## Project Structure
- `colorDetect.py`: Core application script.
- `create_report.py`: Automated documentation generator.
- `colors.csv`: Dataset containing 865 color records.
- `pallete.jpg`: Standardized color grid image.

**Mentor**: Dr. Kiran Kumar Amireddy (Assistant Professor, Department of Mechanical Engineering, CBIT)

---
Department of Mechanical Engineering  
Chaitanya Bharathi Institute of Technology (A)  
2025 - 2026
