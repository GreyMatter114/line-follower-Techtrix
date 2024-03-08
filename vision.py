import cv2

# import sys
import numpy as np

# import os

# np.set_printoptions(threshold=sys.maxsize)
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
# if not cam.isOpened():
#     exit(0)

# currentDirectory = os.getcwd()
# list = os.listdir(currentDirectory)
cv2.namedWindow("OriginalImage")


def crop_image_around_point(img_path, x, y):
    """
    Crop an image around a central point with a specified size.

    Args:
    - image: Input image (numpy array).
    - center: Central point (tuple) around which to crop the image.
    - crop_size: Size (tuple) of the cropped region (width, height).

    Returns:
    - Cropped image (numpy array).
    """
    center = (x, y)
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # Extract dimensions of the original image
    height, width = image.shape[:2]

    # Calculate coordinates for the top-left corner of the bounding box
    x = max(center[0] - 5, 0)
    y = max(center[1] - 5, 0)

    # Calculate coordinates for the bottom-right corner of the bounding box
    x2 = min(center[0] + 5, width)
    y2 = min(center[1] + 5, height)

    # Crop the image using the calculated bounding box
    cropped_image = image[y:y2, x:x2]
    return cropped_image


def determine_move_direction(direc):
    """
    Determine the direction of movement based on the centroids and the center of the region.

    Args:
    - centroids: List of centroids within the region.
    - center: Center of the region.

    Returns:
    - Direction of movement (string): "forward", "backward", "left", "right", or "stop".
    """
    switch = {
        1: [-1, -1],
        2: [0, -1],
        3: [1, -1],
        4: [-1, 0],
        5: [0, 0],
        6: [1, 0],
        7: [-1, 1],
        8: [0, 1],
        9: [1, 1],
        # Add more cases as needed
    }
    return switch[direc]


# cv2.createTrackbar("Brightness", "OriginalImage", 100, 200, on_trackbar)
def compute(image_path, center_x, center_y):
    frame = crop_image_around_point(image_path, center_x, center_y)
    if frame is None:
        return None

    gFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshFrame = cv2.threshold(
        gFrame, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    height = int(frame.shape[0] / 3)
    width = int(frame.shape[1] / 3)
    contArr = []

    for i in range(3):
        row_contours = []
        for j in range(3):
            cont, _ = cv2.findContours(
                threshFrame[height * i : height * (i + 1), width * j : width * (j + 1)],
                mode=cv2.RETR_LIST,
                method=cv2.CHAIN_APPROX_SIMPLE,
            )
            row_contours.append(cont)
        contArr.append(row_contours)

    centArr = []

    for i in range(3):
        row_centroids = []
        for j in range(3):
            centroids = []
            for c in contArr[i][j]:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) + (width * j)
                    cy = int(M["m01"] / M["m00"]) + (height * i)
                    centroids.append((cx, cy))
            row_centroids.append(centroids)
        centArr.append(row_centroids)
    direc = 5
    move = 0
    for i in range(3):
        for j in range(3):
            curr = centArr[i][j]
            if curr > move:
                move = curr
                direc = ((i + 1) * 3) + (j + 1)
    move_direction = determine_move_direction(direc)

    return move_direction


# Example usage
def main(center_x, center_y):
    image_path = "maze.png"
    center_x = 100
    center_y = 100
    directions = compute(image_path, center_x, center_y)
    return directions
