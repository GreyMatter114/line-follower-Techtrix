import cv2 as cv
import numpy as np

def getAvg(lis):
    x = 0
    y = 0
    length = len(lis)
    if length <= 0:
        return None
    for n in lis :
        x += n[0]
        y += n[1]
    x = int(x/length)
    y = int(y/length)
    return (x, y)

def getCntour (gFrame,ThreshHoldOfContourArea) :
    _, threshFrame = cv.threshold(gFrame, 70, 255, cv.THRESH_BINARY_INV)
    hight = int(frame.shape[0] / 3)
    width = int(frame.shape[1] / 3)
    cntourList = []
    for i in range(3):
        arr = []
        for j in range(3):
            cont, _ = cv.findContours(threshFrame[hight * i:hight * (i + 1), width * j: width * (j + 1)],
                                      mode=cv.RETR_LIST, method=cv.CHAIN_APPROX_SIMPLE)
            arr.append(cont)

        cntourList.append(arr)

    contImage = np.zeros(frame.shape, dtype=np.uint8)
    contureCentreList = []
    averageContourCneterList = []
    for i in range(3):
        arr2 = []
        avgArr = []
        for j in range(3):
            cv.drawContours(contImage[hight * i:hight * (i + 1), width * j: width * (j + 1)], cntourList[i][j], -1,
                            (0, 255, 0), thickness=1)
            arr = []
            for c in cntourList[i][j]:
                area = cv.contourArea(c)
                if area < ThreshHoldOfContourArea:
                    continue
                M = cv.moments(c)
                if M['m00'] <= 0:
                    continue
                cx = int(M['m10'] / M['m00']) + (width * i)
                cy = int(M['m01'] / M['m00']) + (hight * j)
                arr.append((cx, cy))
                # cv.circle(contImage, (cx, cy), 7, (0, 0, 255), -1)
            avg = getAvg(arr)
            cv.circle(contImage, avg, 7, (0, 0, 255), -1)
            avgArr.append(avg)
            arr2.append(arr)

        averageContourCneterList.append(avgArr)
        contureCentreList.append(arr2)

    return contImage, cntourList, contureCentreList, averageContourCneterList


cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 300)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 400)
if not cam.isOpened():
    exit(0)


cam.set(cv.CAP_PROP_BRIGHTNESS, 100)
cv.namedWindow("OriginalImage")
while True:
    succ, frame = cam.read()
    gFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    contImage, contList, contCentList, contAvgCentList = getCntour(gFrame, 50)
    cv.imshow("Origial", gFrame)
    cv.imshow('contFrame', contImage)
    x = cv.waitKey(15)
    print(contAvgCentList)
    if x & 0xFF == ord('q'):
            break
    #for n in range(1, 3):
        #cv.line(contImage, (width * n, 0), (width * n, hight * 3), (255, 255, 0), 1)
    #for n in range(1, 3):
        #cv.line(contImage, (0, hight * n), (width * 3, hight * n), (255, 255, 0), 1)
    # for n in range(len(centArr) - 1):
    # cv.line(contImage, centArr[n], centArr[n+1], (255,255,0), 1)
    # print(centArr)
cam.release()
cv.destroyAllWindows()