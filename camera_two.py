import time
import threading
import cv2
import numpy as np
import matplotlib.pyplot as plt

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

class VideoCaptureThreading:
	def __init__(self, src):
		self.cap = cv2.VideoCapture(src)
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
		self.grabbed, self.frame = self.cap.read()
		self.started = False
		self.read_lock = threading.Lock()
	def set(self, var1, var2):
		self.cap.set(var1, var2)
	def start(self):
		if self.started:
			print('[!] Threaded video capturing has already been started.')
			return None
		self.started = True
		self.thread = threading.Thread(target=self.update, args=())
		self.thread.start()
		return self
	def update(self):
		while self.started:
			grabbed, frame = self.cap.read()
			with self.read_lock:
				self.grabbed = grabbed
				self.frame = cv2.flip(frame, 1)
	def read(self):
		with self.read_lock:
			frame = self.frame.copy()
			grabbed = self.grabbed
		return grabbed, frame
	def stop(self):
		self.started = False
		self.thread.join()
	def __exit__(self, exec_type, exc_value, traceback):
		self.cap.release()

if __name__ == "__main__":
	fig = plt.figure(figsize = (12.6, 7), tight_layout=True)
	plt.get_current_fig_manager().window.wm_geometry("+0+0")
	fig.patch.set_facecolor('black')
	fig.canvas.toolbar.pack_forget()
	fig.canvas.manager.full_screen_toggle()
	ax1 = plt.subplot2grid((1, 2), (0, 0))
	ax2 = plt.subplot2grid((1, 2), (0, 1))
	ax1.patch.set_facecolor('black')
	ax2.patch.set_facecolor('black')
	ax1.axes.get_xaxis().set_visible(False)
	ax1.axes.get_yaxis().set_visible(False)
	ax2.axes.get_xaxis().set_visible(False)
	ax2.axes.get_yaxis().set_visible(False)

	cap1 = VideoCaptureThreading(2)
	cap1.start()
	ret, frame = cap1.read()
	im1 = ax1.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

	cap2 = VideoCaptureThreading(3)
	cap2.start()
	ret, frame = cap2.read()
	im2 = ax2.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
	
	while True:
		im1.set_data(grab_frame(cap1))
		im2.set_data(grab_frame(cap2))
		plt.pause(0.001)
