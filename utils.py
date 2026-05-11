import math

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def smooth_coordinate(prev, current, smoothening):
    return prev + (current - prev) / smoothening