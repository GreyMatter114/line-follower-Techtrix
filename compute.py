import cv2 as cv
import sys
import numpy as np
import os

# np.set_printoptions(threshold=sys.maxsize)
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 300)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 300)
if not cam.isOpened():
    exit(0)

# currentDirectory = os.getcwd()
# list = os.listdir(currentDirectory)
cv.namedWindow("OriginalImage")
# cv.createTrackbar("Brightness", "OriginalImage", 100, 200, on_trackbar)
while True:
    # if x.split('.')[1] != 'png':
    # continue
    cam.set(cv.CAP_PROP_BRIGHTNESS, 100)
    succ, frame = cam.read()
    # frame = cv.GaussianBlur(frame, (5,5),1)
    gFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, threshFrame = cv.threshold(
        gFrame, 70, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU
    )
    cannyFrame = cv.Canny(threshFrame, 50, 50)
    cv.imshow("OriginalImage", gFrame)
    cv.imshow("threshImage", threshFrame)
    hight = int(frame.shape[0] / 3)
    width = int(frame.shape[1] / 3)
    contArr = []
    for m in range(3):
        arr = []
        for n in range(3):
            cont, _ = cv.findContours(
                threshFrame[hight * m : hight * (m + 1), width * n : width * (n + 1)],
                mode=cv.RETR_LIST,
                method=cv.CHAIN_APPROX_SIMPLE,
            )
            arr.append(cont)
        contArr.append(arr)

    contImage = np.zeros(frame.shape, dtype=np.uint8)
    centArr = []
    for m in range(3):
        arr2 = []
        for n in range(3):
            cv.drawContours(
                contImage[hight * m : hight * (m + 1), width * n : width * (n + 1)],
                contArr[m][n],
                -1,
                (0, 255, 0),
                thickness=1,
            )
            arr = []
            for c in contArr[m][n]:
                M = cv.moments(c)
                cx = int(M["m10"] / max(M["m00"], 1)) + (width * n)
                cy = int(M["m01"] / max(M["m00"], 1)) + (hight * m)
                arr.append((cx, cy))
                cv.circle(contImage, (cx, cy), 7, (0, 0, 255), -1)

            arr2.append(arr)
        centArr.append(arr2)
    for n in range(1, 3):
        cv.line(contImage, (width * n, 0), (width * n, hight * 3), (255, 255, 0), 1)
    for n in range(1, 3):
        cv.line(contImage, (0, hight * n), (width * 3, hight * n), (255, 255, 0), 1)
    # for n in range(len(centArr) - 1):
    # cv.line(contImage, centArr[n], centArr[n+1], (255,255,0), 1)
    # print(centArr)
    cv.imshow("contFrame", contImage)
    # print(len(cont))
    # print(cont)
    x = cv.waitKey(15)
    if x & 0xFF == ord("q"):
        break

cam.release()
cv.destroyAllWindows()
