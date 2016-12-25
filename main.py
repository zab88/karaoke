'''
<path_to_folders>
'''
import cv2
import numpy as np
import glob, os, sys
import helpers as hh

lower = np.array([130, 100, 160])
upper = np.array([210, 255, 255])

if len(sys.argv)<2:
    print(__doc__)
    sys.exit()
path_to_images = sys.argv[1]
if len(glob.glob(path_to_images)) == 0:
    print('not found <path_to_folders>')
    sys.exit()
path_to_images = os.path.abspath(path_to_images)

# if directories does not exist, let's create them
dirs_mast = ['out', 'xlsx']
for d in dirs_mast:
    if not os.path.exists(d):
        os.makedirs(d)

for sub_dir in glob.glob(path_to_images+os.sep+'*'+os.sep):
    for f_remove in glob.glob("out/*.jpg"):
        os.remove(f_remove)

    current_area = 0
    prev_area = None
    start_time = '00-00-00-00'
    end_time = '00-00-00-00'
    prev_img = None

    for ii in range(0, 2, 1):
        for img_path in glob.glob(sub_dir+os.sep+'*.jpg'):
            img_origin = cv2.imread(img_path)
            h, w = img_origin.shape[:2]
            if ii==0:
                img_origin = img_origin[:h/2, :, :]
            else:
                img_origin = img_origin[h/2:, :, :]

            hsv = cv2.cvtColor(img_origin, cv2.COLOR_BGR2HSV)
            text_mask = cv2.inRange(hsv, lower, upper)

            current_area = cv2.countNonZero(text_mask)

            if current_area >= 100 and prev_area is None:
                # can start
                print 'start ' + img_path
                prev_area = current_area
                prev_img = img_origin.copy()
                start_time = os.path.basename(img_path)[:-4]
                continue

            if current_area >= 100 and (prev_area-99 < current_area):
                # continue
                prev_area = current_area
                prev_img = img_origin.copy()
                continue

            if current_area < 100 and prev_area is not None:
                # stop
                print 'stop ' + img_path
                end_time = os.path.basename(img_path)[:-4]

                cv2.imwrite('out'+os.sep+start_time+'_'+end_time+'.jpg', prev_img)
                prev_area = None
                prev_img = None
                continue

            if current_area < 100 and prev_area is None:
                # do nothing
                continue

            print 'analize me ' + img_path + ' {} {} '.format(prev_area, current_area)

    hh.make_xlsx(os.path.basename(os.path.split(sub_dir)[0]))