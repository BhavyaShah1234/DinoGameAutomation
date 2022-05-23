import cv2 as cv
import keyboard as kb
from utils import capture_window, detect_needle, list_window_names, display, calculate_horizontal_distance, calculate_vertical_distance

# NEEDLE PATHS
dino_path = 'dino.png'
cactus1_path = 'cactus1.png'
cactus2_path = 'cactus2.png'

# NEEDLE IMAGES AND DIMENSIONS
dino = cv.imread(dino_path)
dino_h, dino_w, _ = dino.shape
print(dino_h, dino_w)
cactus1 = cv.imread(cactus1_path)
cactus1_h, cactus1_w, _ = cactus1.shape
cactus2 = cv.imread(cactus2_path)
cactus2_h, cactus2_w, _ = cactus2.shape

# VISUALIZE NEEDLE IMAGES
# cv.imshow('CACTUS 1', cactus1)
# cv.imshow('CACTUS 2', cactus2)
# cv.waitKey(0)
# cv.destroyAllWindows()

# INITIALIZE NECESSARY AND CONSTANT VALUES
x, y = 470, 150
w, h = 660, 120
p = 0
window_name = 'vtop.vit.ac.in - Google Chrome'
threshold = 0.5

# LIST AVAILABLE WINDOWS
list_window_names()

while not kb.is_pressed('esc'):
    # CAPTURE SCREEN
    haystack_image = capture_window(window_name, x, y, w, h, p, p)
    # GET RECTANGLES
    dino_rectangles = detect_needle(haystack_image, dino, cv.TM_SQDIFF_NORMED, 0.5, True)
    cactus1_rectangles = detect_needle(haystack_image, cactus1, cv.TM_SQDIFF_NORMED, 0.5, True)
    cactus2_rectangles = detect_needle(haystack_image, cactus2, cv.TM_SQDIFF_NORMED, 0.5, True)
    print(f'DINO: {dino_rectangles}')
    print(f'CACTUS1: {cactus1_rectangles}')
    print(f'CACTUS2: {cactus2_rectangles}')
    # CALCULATE DISTANCES BETWEEN DINO AND CACTI
    horizontal_dist1 = calculate_horizontal_distance(dino_rectangles, cactus1_rectangles)
    horizontal_dist2 = calculate_horizontal_distance(dino_rectangles, cactus2_rectangles)
    vertical_dist1 = calculate_vertical_distance(dino_rectangles, cactus1_rectangles)
    vertical_dist2 = calculate_vertical_distance(dino_rectangles, cactus2_rectangles)
    # LOGIC TO CLEAR OBSTACLES
    if horizontal_dist1[0] and horizontal_dist1[1] <= 32:
        print(f'HORIZONTAL DISTANCE BETWEEN DINO AND CACTUS1: {horizontal_dist1[1]}')
    if horizontal_dist2[0] and horizontal_dist2[1] <= 32:
        print(f'HORIZONTAL DISTANCE BETWEEN DINO AND CACTUS2: {horizontal_dist2[1]}')
    # DISPLAY RECTANGLES
    haystack_image = display(dino_rectangles, haystack_image, (0, 255, 0), 'both', 'dino')
    haystack_image = display(cactus1_rectangles, haystack_image, (255, 0, 0), 'both', 'cactus1')
    haystack_image = display(cactus2_rectangles, haystack_image, (0, 0, 255), 'both', 'cactus2')
    cv.imshow('Frame', haystack_image)
    cv.waitKey(1)
