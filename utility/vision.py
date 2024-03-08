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


def crop_image_around_point(x, y):
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
    image = cv2.imread("./assets/maze.png", cv2.IMREAD_COLOR)
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


# cv2.createTrackbar("Brightness", "OriginalImage", 100, 200, on_trackbar)
def compute(x, y):
    # if x.split('.')[1] != 'png':
    # continue
    # cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
    # succ, frame = cam.read()
    frame = crop_image_around_point(x, y)
    # frame = cv2.GaussianBlur(frame, (5,5),1)
    gFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshFrame = cv2.threshold(
        gFrame, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    # cannyFrame = cv2.Canny(threshFrame, 50, 50)
    cv2.imshow("OriginalImage", gFrame)
    cv2.imshow("threshImage", threshFrame)
    hight = int(frame.shape[0] / 3)
    width = int(frame.shape[1] / 3)
    contArr = []
    for m in range(3):
        arr = []
        for n in range(3):
            cont, _ = cv2.findContours(
                threshFrame[hight * m : hight * (m + 1), width * n : width * (n + 1)],
                mode=cv2.RETR_LIST,
                method=cv2.CHAIN_APPROX_SIMPLE,
            )
            arr.append(cont)
        contArr.append(arr)

    contImage = np.zeros(frame.shape, dtype=np.uint8)
    centArr = []
    for m in range(3):
        arr2 = []
        for n in range(3):
            cv2.drawContours(
                contImage[hight * m : hight * (m + 1), width * n : width * (n + 1)],
                contArr[m][n],
                -1,
                (0, 255, 0),
                thickness=1,
            )
            arr = []
            for c in contArr[m][n]:
                M = cv2.moments(c)
                cx = int(M["m10"] / max(M["m00"], 1)) + (width * n)
                cy = int(M["m01"] / max(M["m00"], 1)) + (hight * m)
                arr.append((cx, cy))
                cv2.circle(contImage, (cx, cy), 7, (0, 0, 255), -1)

            arr2.append(arr)
        centArr.append(arr2)
    for n in range(1, 3):
        cv2.line(contImage, (width * n, 0), (width * n, hight * 3), (255, 255, 0), 1)
    for n in range(1, 3):
        cv2.line(contImage, (0, hight * n), (width * 3, hight * n), (255, 255, 0), 1)
    # conditions to be added for movment
    # for n in range(len(centArr) - 1):
    # cv2.line(contImage, centArr[n], centArr[n+1], (255,255,0), 1)
    # print(centArr)
    cv2.imshow("contFrame", contImage)
    # print(len(cont))
    # print(cont)
    # x = cv2.waitKey(15)
    # if x & 0xFF == ord("q"):
    #     return
    return centArr


# cam.release()
cv2.destroyAllWindows()
