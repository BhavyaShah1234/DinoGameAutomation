import cv2 as cv
import numpy as np
import win32gui
import win32ui
import win32con


# CAPTURE WINDOW FUNCTION TO GET SCREENSHOTS
def capture_window(window, xmin, ymin, width, height, pad_w, pad_h):
    hwnd = win32gui.FindWindow(None, window)
    w_dc = win32gui.GetWindowDC(hwnd)
    dc_obj = win32ui.CreateDCFromHandle(w_dc)
    c_dc = dc_obj.CreateCompatibleDC()
    data_bitmap = win32ui.CreateBitmap()
    data_bitmap.CreateCompatibleBitmap(dc_obj, width, height)
    c_dc.SelectObject(data_bitmap)
    c_dc.BitBlt((pad_w, pad_h), (width, height), dc_obj, (xmin, ymin), win32con.SRCCOPY)
    signed_ints_array = data_bitmap.GetBitmapBits(True)
    img = np.frombuffer(signed_ints_array, dtype='uint8')
    img.shape = (height, width, 4)
    dc_obj.DeleteDC()
    c_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, w_dc)
    win32gui.DeleteObject(data_bitmap.GetHandle())
    return np.ascontiguousarray(img[..., :3])


# GET ALL ACTIVE WINDOWS
def list_window_names():
    def win_enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(win_enum_handler, None)


# MATCH TEMPLATE BETWEEN HAYSTACK AND NEEDLE IMAGE AND GET LIST OF ALL MATCHES
def detect_needle(haystack, needle, m, t, group_rect):
    result = cv.matchTemplate(haystack, needle, m)
    locations = np.where(result <= t)
    locations = list(zip(*locations[::-1]))
    rectangles = []
    for location in locations:
        rectangles.append([int(location[0]), int(location[1]), needle.shape[1], needle.shape[0]])
    if group_rect:
        rectangles, _ = cv.groupRectangles(rectangles, 1, 0.5)
    return rectangles


# DISPLAY MATCHED TEMPLATES ON HAYSTACK IMAGE
def display(rectangles, haystack, color, mode, text):
    for x1, y1, width, height in rectangles:
        if mode == 'rect':
            haystack = cv.rectangle(haystack, (x1, y1), (x1 + width, y1 + height), color, 2)
        if mode == 'circle':
            haystack = cv.circle(haystack, (x1 + int(width / 2), y1 + int(height / 2)), 3, color, -1)
        if mode == 'text':
            haystack = cv.putText(haystack, f'{text}', (x1, y1-10), cv.FONT_HERSHEY_PLAIN, 1, color, 1)
        else:
            haystack = cv.rectangle(haystack, (x1, y1), (x1 + width, y1 + height), color, 2)
            haystack = cv.circle(haystack, (x1 + int(width / 2), y1 + int(height / 2)), 3, color, -1)
            haystack = cv.putText(haystack, f'{text}', (x1, y1 - 10), cv.FONT_HERSHEY_PLAIN, 1, color, 1)
    return haystack


def calculate_horizontal_distance(rect1, rect2):
    if type(rect1) == tuple or type(rect2) == tuple:
        return False, None
    x1, y1, w1, h1 = rect1[-1]
    x2, y2, w2, h2 = rect2[-1]
    distance = abs(x2 - x1)
    return True, distance


def calculate_vertical_distance(rect1, rect2):
    if type(rect1) == tuple or type(rect2) == tuple:
        return False, None
    x1, y1, w1, h1 = rect1[-1]
    x2, y2, w2, h2 = rect2[-1]
    distance = abs(y2 - y1)
    return True, distance
