import os, cv2
import numpy as np

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

im_dir =  os.environ['HOME']+'/Desktop/caparr/src/'

im_names = sorted(os.listdir(im_dir))
im_files_raw = [cv2.imread(im_dir+x) for x in im_names]
im_files = [cv2.resize(x, None, fx = 0.4, fy = 0.4) for x in im_files_raw]

im_order1 = [[im_files[0],im_files[1],im_files[2]],
             [im_files[6],im_files[7],im_files[8]],
             [im_files[12],im_files[13],im_files[14]],
             [im_files[18],im_files[19],im_files[20]],
             [im_files[24],im_files[25],im_files[26]],
             [im_files[30],im_files[31],im_files[32]],
             [im_files[36],im_files[37],im_files[38]],]

im_order2 = [[im_files[3],im_files[4],im_files[5]],
             [im_files[9],im_files[10],im_files[11]],
             [im_files[15],im_files[16],im_files[17]],
             [im_files[21],im_files[22],im_files[23]],
             [im_files[27],im_files[28],im_files[29]],
             [im_files[33],im_files[34],im_files[35]],
             [im_files[39],im_files[40],im_files[41]],]

im_tile1 = concat_tile(im_order1)
cv2.imwrite(os.environ['HOME']+'/Desktop/caparr/output1.png', im_tile1)
im_tile2 = concat_tile(im_order2)
cv2.imwrite(os.environ['HOME']+'/Desktop/caparr/output2.png', im_tile2)
