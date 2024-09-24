import cv2
import matplotlib.pyplot as plt

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

#Initiate the two cameras
cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap1.set(3,160)
cap1.set(4,120)
cap2 = cv2.VideoCapture(2)
cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap2.set(3,160)
cap2.set(4,120)

#create two subplots
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
plt.tight_layout()

#create two image plots
im1 = ax1.imshow(grab_frame(cap1))
im2 = ax2.imshow(grab_frame(cap2))

plt.ion()

while True:
    im1.set_data(grab_frame(cap1))
    im2.set_data(grab_frame(cap2))
    plt.pause(0.001)

plt.ioff()
plt.show()
