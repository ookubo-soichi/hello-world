import time, serial
import threading
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports

def g_scale(val):
	val_a = abs(val)
	if val_a < 0.05:
		p = 0.0 + (0.2-0.0)/(0.05-0.0)*(val_a-0.0)
	elif val_a < 0.1:
		p = 0.2 + (0.4-0.2)/(0.1-0.05)*(val_a-0.05)
	elif val_a < 0.2:
		p = 0.4 + (0.6-0.4)/(0.2-0.1)*(val_a-0.1)
	elif val_a < 0.3:
		p = 0.6 + (0.8-0.6)/(0.3-0.2)*(val_a-0.2)
	else:
		p = 0.8 + (1.0-0.8)/(0.4-0.3)*(val_a-0.3)
	if val < 0:
		p *= -1.0
	return max(min(p, 1.0), -1.0)

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
	ax1 = plt.subplot2grid((1, 1), (0, 0))
	ax1.patch.set_facecolor('black')
	xmin = -8.0
	ax1.set_xlim((xmin, 0.0))
	ax1.set_ylim((-1.05 ,1.05))
	ax1.axes.get_xaxis().set_visible(False)
	ax1.axes.get_yaxis().set_visible(False)
	ax1.hlines(y=0.0, xmin=xmin, xmax=0, linewidth=2, color='#FFFFFF')
	ax1.hlines(y=0.2, xmin=xmin, xmax=0, linewidth=2, color='#89F336')
	ax1.hlines(y=-0.2, xmin=xmin, xmax=0, linewidth=2, color='#89F336')
	ax1.hlines(y=0.4, xmin=xmin, xmax=0, linewidth=2, color='#0000FF')
	ax1.hlines(y=-0.4, xmin=xmin, xmax=0, linewidth=2, color='#0000FF')
	ax1.hlines(y=0.6, xmin=xmin, xmax=0, linewidth=2, color='#FF69B4')
	ax1.hlines(y=-0.6, xmin=xmin, xmax=0, linewidth=2, color='#FF69B4')
	ax1.hlines(y=0.8, xmin=xmin, xmax=0, linewidth=2, color='#FF0000')
	ax1.hlines(y=-0.8, xmin=xmin, xmax=0, linewidth=2, color='#FF0000')
	ax1.hlines(y=1.0, xmin=xmin, xmax=0, linewidth=2, color='#FFFFFF')
	ax1.hlines(y=-1.0, xmin=xmin, xmax=0, linewidth=2, color='#FFFFFF')
	x_t = np.arange(xmin+0.5, 0.05, 0.05)
	y_x = np.zeros(len(x_t)).astype(float)
	y_y = np.zeros(len(x_t)).astype(float)
	y_a = np.zeros(len(x_t)).astype(float)
	lines_x, = ax1.plot(x_t, y_x, '#ffff00', linewidth=5.0)
	lines_y, = ax1.plot(x_t, y_y, '#ff4500', linewidth=5.0)
	x_txt = xmin; s_txt = 15
	ax1.text(x_txt, 0.21, '0.05G', color='#89F336', size=s_txt)
	ax1.text(x_txt, 0.41, '0.1G', color='#0000FF', size=s_txt)
	ax1.text(x_txt, 0.61, '0.2G', color='#FF69B4', size=s_txt)
	ax1.text(x_txt, 0.81, '0.3G', color='#FF0000', size=s_txt)
	ax1.text(x_txt, -0.19, '-0.05G', color='#89F336', size=s_txt)
	ax1.text(x_txt, -0.39, '-0.1G', color='#0000FF', size=s_txt)
	ax1.text(x_txt, -0.59, '-0.2G', color='#FF69B4', size=s_txt)
	ax1.text(x_txt, -0.79, '-0.3G', color='#FF0000', size=s_txt)

	ports = serial.tools.list_ports.comports()
	for p in ports:
		if p.device in ['COM3', 'COM4']:
			pass
		else:
			com = p.device
	imu = IMUCaptureThreading(com)
	imu.start()
	
	while True:
		Ax, Ay = imu.read()
		y_x = np.hstack((y_x[1:], np.array([g_scale(Ax)])))
		y_y = np.hstack((y_y[1:], np.array([g_scale(Ay)])))
		lines_x.set_data(x_t, y_x)
		lines_y.set_data(x_t, y_y)
		plt.pause(0.01)
