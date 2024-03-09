import cv2

# import sys
import numpy as np

# import os
from PIL import Image

# np.set_printoptions(threshold=sys.maxsize)
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_img_rgb_WIDTH, 300)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
# if not cam.isOpened():
#     exit(0)

# currentDirectory = os.getcwd()
# list = os.listdir(currentDirectory)


def getPartOfImage(srcImage, points: list, shape):
    img = cv2.imread(srcImage)
    p1 = np.float32(points)
    p2 = np.float32([[0, 0], [shape[0], 0], [0, shape[1]], [shape[0], shape[1]]])
    matt = cv2.getPerspectiveTransform(p1, p2)
    out = cv2.warpPerspective(img, matt, shape)
    return out


# def determine_move_direction(centroids, center):
#     """
#     Determine the direction of movement based on the centroids and the center of the region.

#     Args:
#     - centroids: List of centroids within the region.
#     - center: Center of the region.

#     Returns:
#     - Direction of movement (string): "forward", "backward", "left", "right", or "stop".
#     """
#     """
#     Determine the direction of movement based on the centroids and the center of the region.

#     Args:
#     - centroids: List of centroids within the region.
#     - center: Center of the region.

#     Returns:
#     - Direction of movement (string): "forward", "backward", "left", "right", or "stop".
#     """
#     all_centroids = [centroid for row in centroids for cell in row for centroid in cell]

#     if not all_centroids:
#         return [0, 0]

#     total_x = sum(cx for cx, _ in all_centroids)
#     total_y = sum(cy for _, cy in all_centroids)
#     com = (total_x // len(all_centroids), total_y // len(all_centroids))
#     # total_length = max(1, abs(total_x) + abs(total_y))
#     # normalized_dx = total_x / total_length
#     # normalized_dy = total_y / total_length

#     # return [int(normalized_dx), int(normalized_dy)]
#     position = 5
#     if com[0] < center[0] - 10:
#         return [-1, 0]
#     elif com[0] > center[0] + 10:
#         return [1, 0]
#     elif com[1] < center[1] - 10:
#         return [0, 1]
#     elif com[1] > center[1] + 10:
#         return [0, -1]
#     else:
#         return [0, 0]

#     switch = {
#         1: [-1, -1],
#         2: [0, -1],
#         3: [1, -1],
#         4: [-1, 0],
#         5: [0, 0],
#         6: [1, 0],
#         7: [-1, 1],
#         8: [0, 1],
#         9: [1, 1],
#         # Add more cases as needed
#     }
#     return switch[direc]


def determine_move_direction(contAvgCentList):
    if contAvgCentList[0][1] != None:
        return [0, -1]

    if contAvgCentList[0][0] != None:
        return [-1, -1]

    if contAvgCentList[0][2] != None:
        return [1, -1]

    if contAvgCentList[1][0] != None:
        return [-1, 0]

    if contAvgCentList[1][2] != None:
        return [-1, 0]

    if contAvgCentList[1][1] != None:
        if contAvgCentList[2][0] != None:
            return [-2, 0]

        elif contAvgCentList[2][2] != None:
            return [2, 0]

        else:
            return [0, -0.5]
    if contAvgCentList[2][2] != None:

        if contAvgCentList[2][0] != None:
            return [-1, 0]

        elif contAvgCentList[2][2] != None:
            return [1, 0]
        return [0, -0.5]
    return [0, 0]


def getAvg(lis):
    x = 0
    y = 0
    length = len(lis)
    if length <= 0:
        return None
    for n in lis:
        x += n[0]
        y += n[1]
    x = int(x / length)
    y = int(y / length)
    return (x, y)


def getCntour(gFrame, ThreshHoldOfContourArea, frame):
    _, threshFrame = cv2.threshold(gFrame, 70, 255, cv2.THRESH_BINARY_INV)
    hight = int(frame.shape[0] / 3)
    width = int(frame.shape[1] / 3)
    cntourList = []
    for i in range(3):
        arr = []
        for j in range(3):
            cont, _ = cv2.findContours(
                threshFrame[hight * i : hight * (i + 1), width * j : width * (j + 1)],
                mode=cv2.RETR_LIST,
                method=cv2.CHAIN_APPROX_SIMPLE,
            )
            arr.append(cont)

        cntourList.append(arr)

    contImage = np.zeros(frame.shape, dtype=np.uint8)
    contureCentreList = []
    averageContourCneterList = []
    for i in range(3):
        arr2 = []
        avgArr = []
        for j in range(3):
            cv2.drawContours(
                contImage[hight * i : hight * (i + 1), width * j : width * (j + 1)],
                cntourList[i][j],
                -1,
                (0, 255, 0),
                thickness=1,
            )
            arr = []
            for c in cntourList[i][j]:
                area = cv2.contourArea(c)
                if area < ThreshHoldOfContourArea:
                    continue
                M = cv2.moments(c)
                if M["m00"] <= 0:
                    continue
                cx = int(M["m10"] / M["m00"]) + (width * i)
                cy = int(M["m01"] / M["m00"]) + (hight * j)
                arr.append((cx, cy))
                # cv2.circle(contImage, (cx, cy), 7, (0, 0, 255), -1)
            avg = getAvg(arr)
            cv2.circle(contImage, avg, 7, (0, 0, 255), -1)
            avgArr.append(avg)
            arr2.append(arr)

        averageContourCneterList.append(avgArr)
        contureCentreList.append(arr2)

    return contImage, cntourList, contureCentreList, averageContourCneterList


# cv2.createTrackbar("Brightness", "OriginalImage", 100, 200, on_trackbar)
def compute(image_path, center_x, center_y, snip):
    img_rgb = getPartOfImage(
        image_path,
        [
            [center_x + snip, center_y + snip],
            [center_x + snip, center_y - snip],
            [center_x - snip, center_y - snip],
            [center_x - snip, center_y - snip],
        ],
        [snip, snip],
    )
    # <class 'numpy.ndarray'>
    gFrame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    contImage, contList, contCentList, contAvgCentList = getCntour(
        gFrame, snip, img_rgb
    )
    direction = determine_move_direction(contAvgCentList)
    print(direction)
    return direction
    # _, threshFrame = cv2.threshold(
    #     gFrame, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    # )
    # cannyFrame = cv2.Canny(threshFrame, 50, 50)
    # cv2.imshow("OriginalImage", gFrame)
    # cv2.imshow("threshImage", threshFrame)
    # hight = int(img_rgb.shape[0] / 3)
    # width = int(img_rgb.shape[1] / 3)
    # contArr = []
    # for m in range(3):
    #     arr = []
    #     for n in range(3):
    #         cont, _ = cv2.findContours(
    #             threshFrame[hight * m : hight * (m + 1), width * n : width * (n + 1)],
    #             mode=cv2.RETR_LIST,
    #             method=cv2.CHAIN_APPROX_SIMPLE,
    #         )
    #         arr.append(cont)
    #     contArr.append(arr)

    # contImage = np.zeros(img_rgb.shape, dtype=np.uint8)
    # centArr = []
    # for m in range(3):
    #     arr2 = []
    #     for n in range(3):
    #         # cv2.drawContours(
    #         #     contImage[hight * m : hight * (m + 1), width * n : width * (n + 1)],
    #         #     contArr[m][n],
    #         #     -1,
    #         #     (0, 255, 0),
    #         #     thickness=1,
    #         # )
    #         arr = []
    #         for c in contArr[m][n]:
    #             M = cv2.moments(c)
    #             cx = int(M["m10"] / max(M["m00"], 1)) + (width * n)
    #             cy = int(M["m01"] / max(M["m00"], 1)) + (hight * m)
    #             arr.append((cx, cy))
    #             # cv2.circle(contImage, (cx, cy), 7, (0, 0, 255), -1)

    #         arr2.append(arr)
    #     centArr.append(arr2)
    # direction = determine_move_direction(centArr, [center_x, center_y])
    # print(direction)
    # return direction


# Example usage
def main(center_x, center_y, image_path):
    directions = compute(image_path, center_x, center_y, 40)
    return directions
