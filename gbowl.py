import time, serial
import threading
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports

def ball_pos(val):
	val_a = abs(val)
	if val_a < 0.2:
		p = 200 + (272-200)/(0.2-0.0) * (val_a-0.0)
	elif val_a < 0.3:
		p = 272 + (308-272)/(0.3-0.2)*(val_a-0.2)
	elif val_a < 0.4:
		p = 308 + (346-308)/(0.4-0.3)*(val_a-0.3)
	else:
		p = 346 + (400-346)/(1.0-0.4)*(val_a-0.4)
	return max(min(p-200, 200), 0)

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
	ax1.set_aspect('equal', adjustable='box')
	ax1.axes.get_xaxis().set_visible(False)
	ax1.axes.get_yaxis().set_visible(False)

	img = plt.imread("C:/Users/user/bg_orig_400.png")
	im = ax1.imshow(img)
	pos1, = ax1.plot([200.0], [200.0], 'o', ms=100, color='#FFBF00')

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
		A = np.sqrt(Ax*Ax + Ay*Ay)
		theta = np.arctan2(Ax, Ay)
		A_pos = ball_pos(A)
		pos1.set_data([A_pos*np.cos(theta) + 200.0], [A_pos*np.sin(theta) + 200.0])
		plt.pause(0.001)
