import cv2
import pandas as pd

img = cv2.resize(cv2.imread("pallete.jpg"), (700, 500))
csv = pd.read_csv('colors.csv', names=["c", "name", "hex", "R", "G", "B"], header=None)
xpos = ypos = r = g = b = 0

def draw_function(event, x, y, flags, param):
    global xpos, ypos, r, g, b
    xpos, ypos = x, y
    b, g, r = [int(c) for c in img[y, x]]

cv2.namedWindow('color detector')
cv2.setMouseCallback('color detector arrow', draw_function)

while True:
    temp = img.copy()
    d = (csv['R']-r)**2 + (csv['G']-g)**2 + (csv['B']-b)**2
    name = csv.loc[d.idxmin(), 'name']
    text = f"{name} R={r} G={g} B={b}"
    (w, h), _ = cv2.getTextSize(text, 2, 0.5, 1)
    cv2.rectangle(temp, (xpos, ypos-h-15), (xpos+w+30, ypos), (255,255,255), -1)
    cv2.putText(temp, text, (xpos+5, ypos-10), 2, 0.5, (0,0,0), 1, cv2.LINE_AA)
    # Small box showing the actual color
    cv2.rectangle(temp, (xpos+w+10, ypos-h-10), (xpos+w+25, ypos-5), (b,g,r), -1)
    cv2.imshow("color", temp)
    if cv2.waitKey(1) & 0xFF == 27: break
cv2.destroyAllWindows()