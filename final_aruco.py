import cv2
import cv2.aruco as aruco
import time
import math
import numpy as np

marker_present = False

height = 1200 #x
width = 1200 #y
(centerX, centerY) = (width // 2, height // 2)
pixels_to_cm_x=0.05042# cm/pixel 60.5/1200 
pixels_to_cm_y=0.0292 # 35/1200

cap1 = cv2.VideoCapture(0) #external

def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    key = getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarker}")
    arucoDict = aruco.getPredefinedDictionary(key)

    arucoParam = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(arucoDict, arucoParam)
    bbox, ids, rejected = detector.detectMarkers(
        imgGray,
    )

    center = ()

    if draw:
        aruco.drawDetectedMarkers(img, bbox)

    total= len(bbox)

    warp_ids=[]
    other_ids=[]

    for i in range (total):

        id= ids[i][0]


        # in any orientation
        onex= int(bbox[i][0][0][0])
        oney= int(bbox[i][0][0][1])

        twox= int(bbox[i][0][1][0])
        twoy= int(bbox[i][0][1][1])

        threex= int(bbox[i][0][2][0])
        threey= int(bbox[i][0][2][1])

        fourx= int(bbox[i][0][3][0])
        foury= int(bbox[i][0][3][1])


    
        x = (onex + threex) / 2
        x1 = (twox + fourx) / 2

        y = (oney + threey) / 2
        y1 = (twoy + foury) / 2

        center = int((x1 + x) // 2), int((y + y1) // 2)
        arr=[]
        arr.append(id)
        arr.append(center)
        arr.append([onex, oney, twox, twoy, threex, threey, fourx, foury])

        if(id==10 or id==11 or id==12 or id==13):
            warp_ids.append(arr)
            other_ids.append(arr)
        else:
            other_ids.append(arr)
            

        warp_ids = sorted(warp_ids, key=lambda x: x[0])
        other_ids = sorted(other_ids, key=lambda x: x[0])

    # [[12, (159, 360), [82, 309, 220, 283, 246, 407, 91, 441]], [13, (430, 294), [362, 245, 465, 228, 499, 340, 397, 363]], [10, (382, 59), [325, 11, 431, 12, 440, 103, 333, 111]], [11, (168, 62), [112, 15, 221, 4, 227, 112, 113, 120]]]

    return warp_ids, other_ids




def warp(frame, corners):
    pts1 = np.float32(corners)
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))
    M = cv2.getRotationMatrix2D((centerX, centerY), 90, 1.0)
    frame = cv2.warpAffine(frame, M, (width, height))
    return frame


def warp_uitls(color_frame):

    flag=False
    warp_ids, _ = detectMarker(color_frame)

    if(len(warp_ids)==4):
        warp_corners=[]
        points_to_add = [[item[1][0], item[1][1]] for item in warp_ids if isinstance(item[1], tuple)]
        warp_corners.extend(points_to_add)
        warped_frame=warp(color_frame, warp_corners)
        color_frame=warped_frame
        flag=True


    return color_frame, flag


def real_coord(x_pixel,y_pixel):
    x_cm = x_pixel * pixels_to_cm_x
    y_cm = y_pixel * pixels_to_cm_y
    return x_cm,y_cm

def pixel_coord(x_cm,y_cm):
    x_pixel=  x_cm // pixels_to_cm_x
    y_pixel= y_cm // pixels_to_cm_y
    return x_pixel,y_pixel

if __name__ == "__main__":
 
    while True:
        print(marker_present)
        ret1, color_frame = cap1.read()
        color_frame,flag= warp_uitls(color_frame)

        warp_ids, other_ids= detectMarker(color_frame)

        total = len(other_ids)
        print(other_ids)
        for i in range (total):
            centerx= other_ids[i][1][0]
            centery= other_ids[i][1][1]
            cv2.circle(
                color_frame, (centerx, centery), 10, (0, 255, 255)
            )



        if flag ==False:
            color_frame = cv2.resize(color_frame, (1200, 1200))

        #to print circle on real coordinates
        if flag==True:
            x,y=pixel_coord(25.5,27.5)
            x= int(x)
            y= int(y)
            cv2.circle(color_frame, (x, y), radius=5, color=(255, 0, 0), thickness=50)  # radius=-1 for filled circle


        cv2.imshow("Frame for DropZone", color_frame)

        key = cv2.waitKey(1)
        if key == 27:
            break