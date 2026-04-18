# Color Detection System using OpenCV- Robotics & Drones Final Project


## 🚀 Overview
This project is an advanced **Color Detection System** developed for the Robotics and Drones final project. Leveraging the power of **OpenCV** and **Pandas**, this tool provides real-time color identification from any image. By calculating the mathematical "distance" between colors, it precisely matches pixel values to a database of over 800 named colors.

## ✨ Key Features
- **Real-time Identification**: Instantaneous color naming as you interact with the image.
- **Precision Matching**: Uses Euclidean distance algorithm for high-accuracy color mapping.
- **Extensive Database**: Includes a dataset of 800+ colors with names, HEX codes, and RGB values.
- **Dynamic UI**: Hover-based feedback with a custom information overlay showing:
  - Color Name
  - RGB Composition
  - Live Color Preview Box

## 🛠️ Prerequisites
To run this project, you need:
- **Python 3.10+**
- **OpenCV**: `pip install opencv-python`
- **Pandas**: `pip install pandas`

## 📥 Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ronaksarda/ColorDetection_UsingOpenCV.git
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # Or manually:
   pip install opencv-python pandas
   ```
3. **Verify files**: Ensure `colorDetect.py`, `colors.csv`, and `pallete.jpg` are in the same directory.

## 🚀 Usage
1. Execute the main script:
   ```bash
   python colorDetect.py
   ```
2. **Interact**:
   - Move your mouse over any part of the image.
   - The UI will update in real-time with the detected color information.
3. **Exit**: Press the `ESC` key to close the application.

## 🧠 How It Works: The Math
The core of the detection logic relies on the **Euclidean Distance** between colors in the 3D RGB space. 

Given a pixel color $(r, g, b)$ and a dataset color $(R, G, B)$, the distance $d$ is calculated as:
$$d = \sqrt{(R-r)^2 + (G-g)^2 + (B-b)^2}$$

The program iterates through the `colors.csv` file, calculates this distance for every entry, and returns the name associated with the minimum value.

## 📂 Project Structure
- `colorDetect.py`: The main application logic.
- `colors.csv`: The database containing 865 color names and values.
- `pallete.jpg`: The default sample image for testing.
- `banner.png`: Project visual assets.

---
Developed for the **Robotics and Drones** Final Project.
