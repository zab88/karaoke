import cv2
import numpy as np
import xlsxwriter, glob, os

def make_xlsx(movieName):
    # if not os.path.exists('xlsx'+os.sep+movieName):
    #     os.makedirs('xlsx'+os.sep+movieName)
    workbook = xlsxwriter.Workbook('xlsx'+os.sep+movieName+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 12)
    worksheet.set_column(1, 1, 12)
    worksheet.set_column(2, 2, 80)

    j = 0
    time_start_prev = None
    time_end_prev = None
    for f_test in glob.glob("out/*.jpg"):
        # time format
        time_start = os.path.basename(f_test).replace('.jpg', '').split('_')[0].replace('-', ':')
        time_end = os.path.basename(f_test).replace('.jpg', '').split('_')[1].replace('-', ':')
        time_start = time_start[::-1].replace(':', '.', 1)[::-1] + '0'
        time_end = time_end[::-1].replace(':', '.', 1)[::-1] + '0'

        worksheet.write('A'+str(j+1), time_start)
        worksheet.write('B'+str(j+1), time_end)
        worksheet.insert_image('C'+str(j+1), f_test)

        worksheet.set_row(j, 32)

        # quick fix time
        if time_end_prev is None:
            time_start_prev = time_start
            time_end_prev = time_end
            j += 1
            continue
        if time_end_prev > time_start:
            worksheet.write('B' + str(j), time_start)
        time_start_prev = time_start
        time_end_prev = time_end

        j += 1
    workbook.close()

def symmetry_clean(img_bin):
    h, w = img_bin.shape[:2]
    cols_sum = img_bin.sum(axis=0)
    cols_sum = [1 if s > 1 else 0 for s in cols_sum]
    mid = len(cols_sum)/2
    m_w = 25
    min_clean = None
    for i in xrange(0, len(cols_sum)/2, 1):
        if sum(cols_sum[mid-i-m_w:mid-i]) < 1:
            min_clean = i
            break
        if sum(cols_sum[mid+i:mid+i+m_w]) < 1:
            min_clean = i
            break
    if min_clean is not None:
        # clean
        res = img_bin.copy()
        cv2.rectangle(res, (0, 0), (mid-min_clean, h), color=(0), thickness=-1)
        cv2.rectangle(res, (mid+min_clean, 0), (w, h), color=(0), thickness=-1)
    return res