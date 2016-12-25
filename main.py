import cv2
import numpy as np
import glob

lower = np.array([130, 100, 160])
upper = np.array([210, 255, 255])

current_area = 0
prev_area = None
for img_path in glob.glob('cut_images/*.jpg'):
    img_origin = cv2.imread(img_path)

    hsv = cv2.cvtColor(img_origin, cv2.COLOR_BGR2HSV)
    text_mask = cv2.inRange(hsv, lower, upper)

    current_area = cv2.countNonZero(text_mask)

    if current_area >= 100 and prev_area is None:
        # can start
        print 'start ' + img_path
        prev_area = current_area
        continue

    if current_area >= 100 and (prev_area-99 < current_area):
        # continue
        prev_area = current_area
        continue

    if current_area < 100 and prev_area is not None:
        # stop
        print 'stop ' + img_path
        prev_area = None
        continue

    if current_area < 100 and prev_area is None:
        # do nothing
        continue

    print 'analize me ' + img_path + ' {} {} '.format(prev_area, current_area)