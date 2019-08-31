import os, cv2
import shutil

img_dir = './raw_img/'
img_dirs = os.listdir(img_dir)
detector = cv2.ORB_create()

for d in img_dirs:
    print (d)
    last_copyed_i = 0
    os.mkdir('./rmdup_img/'+d[:-3])
    img_files = sorted(os.listdir(img_dir+d))
    rlt = []
    for i in range(len(img_files)-1):
        img1 = cv2.imread(img_dir+d+'/'+img_files[i],0)
        img2 = cv2.imread(img_dir+d+'/'+img_files[i+1],0)
        kp1, des1 = detector.detectAndCompute(img1, None)
        kp2, des2 = detector.detectAndCompute(img2, None)
        if des1 is None or des2 is None:
            continue
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        if len(matches[0]) != 2:
            continue
        good = []
        match_param = 0.6
        for m,n in matches:
            if m.distance < match_param*n.distance:
                good.append([m])
        #print (img_files[i], len(good))
        rlt.append([img_files[i], len(good)])
        if len(good) <= 20 or i >= last_copyed_i+4:
            shutil.copy(img_dir+d+'/'+img_files[i], './rmdup_img/'+d[:-3]+'/'+img_files[i])
            last_copyed_i = i

img_dir = './rmdup_img/'
img_dirs = os.listdir(img_dir)
for d in img_dirs:
    print (d)
    last_copyed_i = 0
    os.mkdir('./rmdup_img2/'+d)
    img_files = sorted(os.listdir(img_dir+d))
    rlt = []
    for i in range(len(img_files)-1):
        img1 = cv2.imread(img_dir+d+'/'+img_files[i],0)
        img2 = cv2.imread(img_dir+d+'/'+img_files[i+1],0)
        kp1, des1 = detector.detectAndCompute(img1, None)
        kp2, des2 = detector.detectAndCompute(img2, None)
        if des1 is None or des2 is None:
            continue
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        if len(matches[0]) != 2:
            continue
        good = []
        match_param = 0.6
        for m,n in matches:
            if m.distance < match_param*n.distance:
                good.append([m])
        #print (img_files[i], len(good))
        rlt.append([img_files[i], len(good)])
        if len(good) == 0 or i >= last_copyed_i+4:
            shutil.copy(img_dir+d+'/'+img_files[i], './rmdup_img2/'+d+'/'+img_files[i])
            last_copyed_i = i
