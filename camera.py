import cv2
import matplotlib.pyplot as plt

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

#Initiate the two cameras
cap1 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap1.set(3,160)
cap1.set(4,120)

cap2 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap2.set(3,160)
cap2.set(4,120)

#create two subplots
fig = plt.figure(figsize = (12.65, 3.8))
fig.patch.set_facecolor('black')
fig.canvas.toolbar.pack_forget()
plt.get_current_fig_manager().window.wm_geometry("+0+335")
ax1 = plt.subplot2grid((1, 2), (0, 0))
ax2 = plt.subplot2grid((1, 2), (0, 1))
plt.tight_layout()
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)

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
