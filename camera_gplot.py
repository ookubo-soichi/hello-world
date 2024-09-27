import time, serial
import threading
import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports

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
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
		print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
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
	def __init__(self, com):
		self.ser = serial.Serial()
		self.ser.port = com
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
	fig = plt.figure(figsize = (12.6, 7), tight_layout=True)
	plt.get_current_fig_manager().window.wm_geometry("+0+0")
	fig.patch.set_facecolor('black')
	fig.canvas.toolbar.pack_forget()
	fig.canvas.manager.full_screen_toggle()
	ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=2)
	ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=2)
	ax3 = plt.subplot2grid((3, 2), (2, 0), colspan=2)
	ax1.patch.set_facecolor('black')
	ax2.patch.set_facecolor('black')
	ax3.patch.set_facecolor('black')
	xmin = -15.0
	ax3.set_xlim((xmin, 0.0))
	ax3.set_ylim((-1.05 ,1.05))
	ax1.axes.get_xaxis().set_visible(False)
	ax1.axes.get_yaxis().set_visible(False)
	ax2.axes.get_xaxis().set_visible(False)
	ax2.axes.get_yaxis().set_visible(False)
	ax3.axes.get_xaxis().set_visible(False)
	ax3.axes.get_yaxis().set_visible(False)
	ax3.hlines(y=0.0, xmin=xmin, xmax=0, linewidth=2, color='#FFFFFF')
	ax3.hlines(y=0.2, xmin=xmin, xmax=0, linewidth=2, color='#89F336')
	ax3.hlines(y=-0.2, xmin=xmin, xmax=0, linewidth=2, color='#89F336')
	ax3.hlines(y=0.4, xmin=xmin, xmax=0, linewidth=2, color='#67DA0D')
	ax3.hlines(y=-0.4, xmin=xmin, xmax=0, linewidth=2, color='#67DA0D')
	ax3.hlines(y=0.6, xmin=xmin, xmax=0, linewidth=2, color='#58BB0B')
	ax3.hlines(y=-0.6, xmin=xmin, xmax=0, linewidth=2, color='#58BB0B')
	ax3.hlines(y=0.8, xmin=xmin, xmax=0, linewidth=2, color='#4A9C09')
	ax3.hlines(y=-0.8, xmin=xmin, xmax=0, linewidth=2, color='#4A9C09')
	ax3.hlines(y=1.0, xmin=xmin, xmax=0, linewidth=2, color='#3B7D07')
	ax3.hlines(y=-1.0, xmin=xmin, xmax=0, linewidth=2, color='#3B7D07')
	x_t = np.arange(-14.0, 0.05, 0.05)
	y_x = np.zeros(len(x_t)).astype(float)
	y_y = np.zeros(len(x_t)).astype(float)
	y_a = np.zeros(len(x_t)).astype(float)
	lines_x, = ax3.plot(x_t, y_x, '#ffff00', linewidth=5.0)
	lines_y, = ax3.plot(x_t, y_y, '#00ffff', linewidth=5.0)
	x_txt = xmin; s_txt = 15
	ax3.text(x_txt, 0.21, '0.1G', color='#89F336', size=s_txt)
	ax3.text(x_txt, 0.41, '0.25G', color='#89F336', size=s_txt)
	ax3.text(x_txt, 0.61, '0.4G', color='#89F336', size=s_txt)
	ax3.text(x_txt, 0.81, '0.6G', color='#89F336', size=s_txt)
	ax3.text(x_txt, -0.19, '-0.1G', color='#89F336', size=s_txt)
	ax3.text(x_txt, -0.39, '-0.25G', color='#89F336', size=s_txt)
	ax3.text(x_txt, -0.59, '-0.4G', color='#89F336', size=s_txt)
	ax3.text(x_txt, -0.79, '-0.6G', color='#89F336', size=s_txt)
	
	cap1 = VideoCaptureThreading(2)
	cap1.start()
	ret, frame = cap1.read()
	im1 = ax1.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

	cap2 = VideoCaptureThreading(3)
	cap2.start()
	ret, frame = cap2.read()
	im2 = ax2.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

	ports = serial.tools.list_ports.comports()
	for p in ports:
		if p.device in ['COM3', 'COM4']:
			pass
		else:
			com = p.device
	imu = IMUCaptureThreading(com)
	imu.start()
	
	while True:
		im1.set_data(grab_frame(cap1))
		im2.set_data(grab_frame(cap2))
		Ax, Ay = imu.read()
		y_x = np.hstack((y_x[1:], np.array([g_scale(Ax)])))
		y_y = np.hstack((y_y[1:], np.array([g_scale(Ay)])))
		lines_x.set_data(x_t, y_x)
		lines_y.set_data(x_t, y_y)
		plt.pause(0.001)
