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