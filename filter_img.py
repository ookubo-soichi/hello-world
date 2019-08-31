import os, cv2, shutil
import numpy as np
from matplotlib import pyplot as plt

img_dir = os.listdir('./raw_img/')

for _d in img_dir:
    print (_d)
    os.mkdir('./fil_img/'+_d)
    imgs = os.listdir('./raw_img/'+_d)
    for _img in imgs:
        errcnt_sum = 0
        img = cv2.imread('./raw_img/'+_d+'/'+_img, 0)
        for x in np.arange(50,1920,100):
            errcnt = 0
            errcnt_list = []
            tmp = img[:,x]
            for i,p in enumerate(tmp[:-1]):
                if abs(float(tmp[i]) - float(tmp[i+1])) > 20:
                    errcnt = errcnt+1
                else:
                    if errcnt > 10:
                        errcnt_list.append(errcnt)
                    errcnt = 0
            errcnt_sum = errcnt_sum + sum(errcnt_list)
        if errcnt_sum > 1000:
            shutil.move('./raw_img/'+_d+'/'+_img, './fil_img/'+_d)
