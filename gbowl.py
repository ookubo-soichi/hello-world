# nano /lib/udev/rules.d/50-udev-default.rules
# KERNEL=="tty[A-Z]*[0-9]|pppox[0-9]*|ircomm[0-9]*|noz[0-9]*|rfcomm[0-9]*", GROUP="dialout", MODE="0666"

import time, serial
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for p in ports:
	if p.device in ['COM3', 'COM4']:
		pass
	else:
		com = p.device

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

img = plt.imread("C:/car/bg_orig_200.png")
fig = plt.figure(figsize = (12.65, 3))
plt.get_current_fig_manager().window.wm_geometry("+0+0")
fig.tight_layout()
fig.patch.set_facecolor('black')
fig.canvas.toolbar.pack_forget()

ax1 = plt.subplot2grid((1, 20), (0, 0), colspan=7)
ax2 = plt.subplot2grid((1, 20), (0, 7), colspan=13)
ax1.patch.set_facecolor('black')
ax2.patch.set_facecolor('black')

im = ax1.imshow(img)
pos1, = ax1.plot([100.0], [100.0], 'o', ms=35, color='#FFBF00')
ax2.hlines(y=0.0, xmin=-10, xmax=0, linewidth=2, color='#FFFFFF')
ax2.hlines(y=0.2, xmin=-10, xmax=0, linewidth=2, color='#89F336')
ax2.hlines(y=-0.2, xmin=-10, xmax=0, linewidth=2, color='#89F336')
ax2.hlines(y=0.4, xmin=-10, xmax=0, linewidth=2, color='#67DA0D')
ax2.hlines(y=-0.4, xmin=-10, xmax=0, linewidth=2, color='#67DA0D')
ax2.hlines(y=0.6, xmin=-10, xmax=0, linewidth=2, color='#58BB0B')
ax2.hlines(y=-0.6, xmin=-10, xmax=0, linewidth=2, color='#58BB0B')
ax2.hlines(y=0.8, xmin=-10, xmax=0, linewidth=2, color='#4A9C09')
ax2.hlines(y=-0.8, xmin=-10, xmax=0, linewidth=2, color='#4A9C09')
ax2.hlines(y=1.0, xmin=-10, xmax=0, linewidth=2, color='#3B7D07')
ax2.hlines(y=-1.0, xmin=-10, xmax=0, linewidth=2, color='#3B7D07')
x_t = np.arange(-8.0, 0.05, 0.05)
y_x = np.zeros(len(x_t)).astype(float)
y_y = np.zeros(len(x_t)).astype(float)
y_a = np.zeros(len(x_t)).astype(float)
lines_x, = ax2.plot(x_t, y_x, '#ffff00', linewidth=5.0)
lines_y, = ax2.plot(x_t, y_y, '#00ffff', linewidth=5.0)
ax2.text(-10.0, 0.21, '0.1G', color='#89F336', size=15)
ax2.text(-10.0, 0.41, '0.25G', color='#89F336', size=15)
ax2.text(-10.0, 0.61, '0.4G', color='#89F336', size=15)
ax2.text(-10.0, 0.81, '0.6G', color='#89F336', size=15)
ax2.text(-10.0, -0.21, '-0.1G', color='#89F336', size=15)
ax2.text(-10.0, -0.41, '-0.25G', color='#89F336', size=15)
ax2.text(-10.0, -0.61, '-0.4G', color='#89F336', size=15)
ax2.text(-10.0, -0.81, '-0.6G', color='#89F336', size=15)
ax1.set_aspect('equal', adjustable='box')
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)
ax2.set_xlim((-10.0, 0.0))
ax2.set_ylim((-1.05 ,1.05))
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)

ser = serial.Serial()
ser.port = com
ser.baudrate = 19200
ser.parity = 'N'
ser.bytesize = 8
ser.timeout = 1
ser.open()
print('Starting...', ser.name)
time.sleep(1)
ser.reset_input_buffer()
while True:
	readData = ser.read(size=11).hex()
	AxL = int(readData[4:6], 16)
	AxH = int(readData[6:8], 16)
	AyL = int(readData[8:10], 16)
	AyH = int(readData[10:12], 16)
	AzL = int(readData[12:14], 16)
	AzH = int(readData[14:16], 16)
	Ax = float(np.array((AxH<<8)|AxL).astype(np.int16)) *16.0 / 32768.0
	Ay = float(np.array((AyH<<8)|AyL).astype(np.int16)) *16.0 / 32768.0
	Az = float(np.array((AzH<<8)|AzL).astype(np.int16)) *16.0 / 32768.0
	A = np.sqrt(Ax*Ax + Ay*Ay)
	theta = np.arctan2(Ax, Ay)
	y_x = np.hstack((y_x[1:], np.array([g_scale(Ax)])))
	y_y = np.hstack((y_y[1:], np.array([g_scale(Ay)])))
	lines_x.set_data(x_t, y_x)
	lines_y.set_data(x_t, y_y)
	A_pos = ball_pos(A)
	pos1.set_data([A_pos*np.cos(theta) + 100.0], [A_pos*np.sin(theta) + 100.0])
	plt.pause(0.01)
