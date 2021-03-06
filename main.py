'''
<path_to_images>
<6 numbers, separated by comma>
<number of lines>
'''
import cv2
import numpy as np
import glob, os, sys
import helpers as hh

# cut_images2 30,115,115,65,255,255
# cut_images2\movie_02\\*.jpg 30,115,115,65,255,255
# K:\MyPrograms\python2\recipe\simon-crop\out_2017\0U0QnC5Zw-w/*.jpg 0,0,210,200,200,255
if len(sys.argv)<3:
    print(__doc__)
    sys.exit()
path_to_images = sys.argv[1]
numbers6 = sys.argv[2]
numbers6 = numbers6.split(',')
if len(numbers6) == 6:
    lower = np.array([int(numbers6[0]), int(numbers6[1]), int(numbers6[2])])
    upper = np.array([int(numbers6[3]), int(numbers6[4]), int(numbers6[5])])
else:
    lower = np.array([130, 100, 160])
    upper = np.array([210, 255, 255])
    # cut_images 130,100,160,210,255,255
    # cut_images2 30,115,115,65,255,255

# number of lines can be 1 or 2
karaoke_lines = 2
if len(sys.argv)==4:
    if str(sys.argv[3]) in ['1', '2']:
        karaoke_lines = int(sys.argv[3])

if len(glob.glob(path_to_images)) == 0:
    print('not found <path_to_images>')
    sys.exit()
# path_to_images = os.path.abspath(path_to_images) # for many

debug = False
# debug = True

# if directories does not exist, let's create them
dirs_mast = ['out', 'xlsx']
for d in dirs_mast:
    if not os.path.exists(d):
        os.makedirs(d)

#for sub_dir in glob.glob(path_to_images+os.sep+'*'+os.sep): # for many
sub_dir = path_to_images
for f_remove in glob.glob("out/*.jpg"):
    os.remove(f_remove)

current_area = 0
prev_area = None
start_time = '00-00-00-00'
end_time = '00-00-00-00'
prev_img = None

for ii in range(0, karaoke_lines, 1):
    frame_now = 0
    start_frame = 0
    frame_names = []
    # for img_path in glob.glob(sub_dir+os.sep+'*.jpg'): # for many
    for img_path in glob.glob(sub_dir):
        if img_path[-10:] == '000000.jpg':
            continue
        # just to add 0.2
        frame_names.append(os.path.basename(img_path)[:-4])
        frame_now += 1
        img_origin = cv2.imread(img_path)
        h, w = img_origin.shape[:2]
        # splitting if two lines
        if karaoke_lines == 2:
            if ii==0:
                img_origin = img_origin[:h/2, :, :]
            else:
                img_origin = img_origin[h/2:, :, :]

        hsv = cv2.cvtColor(img_origin, cv2.COLOR_BGR2HSV)
        text_mask = cv2.inRange(hsv, lower, upper)

        # let's apply symmetry
        text_mask = hh.symmetry_clean(text_mask)

        current_area = cv2.countNonZero(text_mask)

        if current_area >= 100 and prev_area is None:
            # can start
            if debug:
                print 'start ' + img_path
            prev_area = current_area
            prev_img = img_origin.copy()
            start_time = os.path.basename(img_path)[:-4]
            start_frame = frame_now
            if frame_now>2:
                start_time = frame_names[-2]
            continue

        if current_area >= 100 and (prev_area-99 < current_area):
            # continue
            prev_area = current_area
            prev_img = img_origin.copy()
            continue

        if current_area < 100 and prev_area is not None:
            # stop
            if debug:
                print 'stop ' + img_path
            end_time = os.path.basename(img_path)[:-4]

            # check length of sequence
            if frame_now - start_frame > 10:
                cv2.imwrite('out'+os.sep+start_time+'_'+end_time+'.jpg', prev_img)
            prev_area = None
            prev_img = None
            continue

        if current_area < 100 and prev_area is None:
            # do nothing
            continue
        if debug:
            print 'analize me ' + img_path + ' {} {} '.format(prev_area, current_area)

hh.make_xlsx(os.path.basename(os.path.split(sub_dir)[0]))