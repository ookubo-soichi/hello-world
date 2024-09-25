import time, serial
import threading
import cv2
import numpy as np
import matplotlib.pyplot as plt

def ball_pos(val):
	val_a = abs(val)
	if val_a < 0.2:
		p = 100 + (136-100)/(0.2-0.0) * (val_a-0.0)
	elif val_a < 0.3:
		p = 136 + (154-136)/(0.3-0.2)*(val_a-0.2)
	elif val_a < 0.4:
		p = 154 + (173-154)/(0.4-0.3)*(val_a-0.3)
	else:
		p = 173 + (200-173)/(1.0-0.4)*(val_a-0.4)
	return max(min(p-100, 100), 0)

def g_scale(val):
	val_a = abs(val)
	if val_a < 0.1:
		p = 0.0 + (0.2-0.0)/(0.1-0.0)*(val_a-0.0)
	elif val_a < 0.25:
		p = 0.2 + (0.4-0.2)/(0.25-0.1)*(val_a-0.1)
	elif val_a < 0.4:
		p = 0.4 + (0.6-0.4)/(0.4-0.25)*(val_a-0.25)
	elif val_a < 0.6:
		p = 0.6 + (0.8-0.6)/(0.6-0.4)*(val_a-0.4)
	else:
		p = 0.8 + (1.0-0.8)/(1.0-0.6)*(val_a-0.6)
	if val < 0:
		p *= -1.0
	return max(min(p, 1.0), -1.0)

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

class VideoCaptureThreading:
	def __init__(self, src):
		self.cap = cv2.VideoCapture(src)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
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
				self.frame = frame
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

class IMUCaptureThreading:
	def __init__(self):
		self.ser = serial.Serial()
		self.ser.port = '/dev/ttyUSB0'
		self.ser.baudrate = 19200
		self.ser.parity = 'N'
		self.ser.bytesize = 8
		self.ser.timeout = 1
		self.ser.open()
		print('Starting...', self.ser.name)
		time.sleep(1)
		self.ser.reset_input_buffer()
		self.started = False
		self.read_lock = threading.Lock()
		self.Ax = 0.0
		self.Ay = 0.0
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
			readData = self.ser.read(size=11).hex()
			AxL = int(readData[4:6], 16)
			AxH = int(readData[6:8], 16)
			AyL = int(readData[8:10], 16)
			AyH = int(readData[10:12], 16)
			Ax = float(np.array((AxH<<8)|AxL).astype(np.int16)) *16.0 / 32768.0
			Ay = float(np.array((AyH<<8)|AyL).astype(np.int16)) *16.0 / 32768.0
			with self.read_lock:
				self.Ax = Ax
				self.Ay = Ay
	def read(self):
		with self.read_lock:
			Ax = self.Ax
			Ay = self.Ay
		return Ax, Ay
	def stop(self):
		self.started = False
		self.thread.join()
		
if __name__ == "__main__":
	fig = plt.figure(figsize = (16, 9), tight_layout=True)
	# plt.get_current_fig_manager().window.wm_geometry("+0+0")
	# fig.tight_layout()
	fig.patch.set_facecolor('black')
	#fig.canvas.toolbar.pack_forget()
	ax1 = plt.subplot2grid((2, 6), (0, 0), colspan=2)
	ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=4)
	ax3 = plt.subplot2grid((2, 6), (1, 0), colspan=3)
	ax4 = plt.subplot2grid((2, 6), (1, 3), colspan=3)
	ax1.patch.set_facecolor('black')
	ax2.patch.set_facecolor('black')
	ax3.patch.set_facecolor('black')
	ax4.patch.set_facecolor('black')
	ax1.set_aspect('equal', adjustable='box')
	ax2.set_xlim((-10.0, 0.0))
	ax2.set_ylim((-1.05 ,1.05))
	ax1.axes.get_xaxis().set_visible(False)
	ax1.axes.get_yaxis().set_visible(False)
	ax2.axes.get_xaxis().set_visible(False)
	ax2.axes.get_yaxis().set_visible(False)
	ax3.axes.get_xaxis().set_visible(False)
	ax3.axes.get_yaxis().set_visible(False)
	ax4.axes.get_xaxis().set_visible(False)
	ax4.axes.get_yaxis().set_visible(False)

	img = plt.imread("bg_orig_200.png")
	im = ax1.imshow(img)
	pos1, = ax1.plot([100.0], [100.0], 'o', ms=75, color='#FFBF00')

	xmin = -10.0
	ax2.hlines(y=0.0, xmin=xmin, xmax=0, linewidth=2, color='#FFFFFF')
	ax2.hlines(y=0.2, xmin=xmin, xmax=0, linewidth=2, color='#89F336')
	ax2.hlines(y=-0.2, xmin=xmin, xmax=0, linewidth=2, color='#89F336')
	ax2.hlines(y=0.4, xmin=xmin, xmax=0, linewidth=2, color='#67DA0D')
	ax2.hlines(y=-0.4, xmin=xmin, xmax=0, linewidth=2, color='#67DA0D')
	ax2.hlines(y=0.6, xmin=xmin, xmax=0, linewidth=2, color='#58BB0B')
	ax2.hlines(y=-0.6, xmin=xmin, xmax=0, linewidth=2, color='#58BB0B')
	ax2.hlines(y=0.8, xmin=xmin, xmax=0, linewidth=2, color='#4A9C09')
	ax2.hlines(y=-0.8, xmin=xmin, xmax=0, linewidth=2, color='#4A9C09')
	ax2.hlines(y=1.0, xmin=xmin, xmax=0, linewidth=2, color='#3B7D07')
	ax2.hlines(y=-1.0, xmin=xmin, xmax=0, linewidth=2, color='#3B7D07')
	x_t = np.arange(-9.0, 0.05, 0.05)
	y_x = np.zeros(len(x_t)).astype(float)
	y_y = np.zeros(len(x_t)).astype(float)
	y_a = np.zeros(len(x_t)).astype(float)
	lines_x, = ax2.plot(x_t, y_x, '#ffff00', linewidth=5.0)
	lines_y, = ax2.plot(x_t, y_y, '#00ffff', linewidth=5.0)
	x_txt = -10.0; s_txt = 15
	ax2.text(x_txt, 0.21, '0.1G', color='#89F336', size=s_txt)
	ax2.text(x_txt, 0.41, '0.25G', color='#89F336', size=s_txt)
	ax2.text(x_txt, 0.61, '0.4G', color='#89F336', size=s_txt)
	ax2.text(x_txt, 0.81, '0.6G', color='#89F336', size=s_txt)
	ax2.text(x_txt, -0.21, '-0.1G', color='#89F336', size=s_txt)
	ax2.text(x_txt, -0.41, '-0.25G', color='#89F336', size=s_txt)
	ax2.text(x_txt, -0.61, '-0.4G', color='#89F336', size=s_txt)
	ax2.text(x_txt, -0.81, '-0.6G', color='#89F336', size=s_txt)
	
	cap1 = VideoCaptureThreading(0)
	cap1.start()
	ret, frame = cap1.read()
	im1 = ax3.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

	cap2 = VideoCaptureThreading(2)
	cap2.start()
	ret, frame = cap2.read()
	im2 = ax4.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

	imu = IMUCaptureThreading()
	imu.start()
	
	while True:
		im1.set_data(grab_frame(cap1))
		im2.set_data(grab_frame(cap2))
		Ax, Ay = imu.read()
		A = np.sqrt(Ax*Ax + Ay*Ay)
		theta = np.arctan2(Ax, Ay)
		A_pos = ball_pos(A)
		pos1.set_data([A_pos*np.cos(theta) + 100.0], [A_pos*np.sin(theta) + 100.0])
		y_x = np.hstack((y_x[1:], np.array([g_scale(Ax)])))
		y_y = np.hstack((y_y[1:], np.array([g_scale(Ay)])))
		lines_x.set_data(x_t, y_x)
		lines_y.set_data(x_t, y_y)
		plt.pause(0.01)
