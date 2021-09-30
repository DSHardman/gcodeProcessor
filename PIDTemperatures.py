import time
import serial
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

com = "COM4"

if 'ser' in globals() and ser.isOpen() == False: ## checks if ser is defined already and if connection is open
    ## configures the serial connection:
    ser = serial.Serial(
        port=com,
        baudrate=38400,
    )
elif 'ser' in globals() and ser.isOpen() == True:
    ser.flushInput()
    ser.flushOutput()
else:
    ser = serial.Serial(
        port=com,
        baudrate=38400,
    )

m = 0
nozzle_data = np.array([0])         ## Creates a numpy array to store the nozzel temperature to
t = np.array([0])                   ## Creates a numpty array to store times to
targets = np.array([0])
timestep = 0.5
max = 420

ser.write(b'\r\n\r\n')
time.sleep(2)
ser.flushInput()

ser.write(b'M42 P9 S255\r\n')       ## Write G-code over serial command, turns on RAMPS fan
ser.write(b'M42 P4 S255\r\n')       ## turns on horizontal extruder fan
ser.write(b'M106 S200\r\n')         ## turns on small nozzle fan

# Define initial parameters
init_target = 100
init_kp = 15
init_ki = 0.1
init_kd = 6.0

ser.write(b'M104 S' + str(init_target).encode() + b'\r\n')
time.sleep(2)
ser.write(b'M301 P' + str(init_kp).encode() + b' I' + str(init_ki).encode() + b' D' + str(init_kd).encode() + b'\r\n')
time.sleep(2)

fig, ax = plt.subplots()
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
# adjust the main plot to make room for the sliders
plt.subplots_adjust(bottom=0.6)

axtarget = plt.axes([0.25, 0.4, 0.65, 0.03])
target_slider = Slider(
    ax=axtarget,
    label='Target',
    valmin=0,
    valmax=200,
    valinit=init_target,
)

axkp = plt.axes([0.25, 0.3, 0.65, 0.03])
kp_slider = Slider(
    ax=axkp,
    label='Kp',
    valmin=0,
    valmax=30,
    valinit=init_kp,
)

axki = plt.axes([0.25, 0.2, 0.65, 0.03])
ki_slider = Slider(
    ax=axki,
    label='Ki',
    valmin=0,
    valmax=0.5,
    valinit=init_ki,
)

axkd = plt.axes([0.25, 0.1, 0.65, 0.03])
kd_slider = Slider(
    ax=axkd,
    label='Kd',
    valmin=0,
    valmax=10,
    valinit=init_kd,
)


# The function to be called anytime a slider's value changes
def update(val):
    ser.write(b'M301 P' + str(kp_slider.val).encode() + b' I' + str(ki_slider.val).encode() + b' D' + str(kd_slider.val).encode() + b'\r\n')
    ser.write(b'M104 S' + str(target_slider.val).encode() + b'\r\n')
    plt.draw()


# register the update function with each slider
target_slider.on_changed(update)
kp_slider.on_changed(update)
ki_slider.on_changed(update)
kd_slider.on_changed(update)

ax = fig.add_subplot()
plt.ion()
for m in range(1,max):              ## For loop to read obtaining temperature values for max time limit
    ser.write(b'M105\r\n')
    out = ''
    ## waits amount set by timestep before reading output
    time.sleep(timestep)
    out = ser.read(ser.inWaiting()) ## Wait for serial data incoming from 3D printer
    s = str(out)
    if out != '' and ':' in s and 'S' not in s:         ## makes sure only to use temperature reading lines
        colon = s.find(':')                             ## finds the first colon in string
        nozzle_temp = s[(colon + 1):(colon + 6)]        ## nozzle temp in this range after first colon
        nozzle_data = np.append(nozzle_data, [float(nozzle_temp)])
        targets = np.append(targets, [target_slider.val])
        tim = str(m*timestep)
        t = np.append(t, [float(tim)])

        plt.cla()
        plt.plot(t, nozzle_data, 'r-')
        plt.plot(t, targets)
        plt.ylabel('Nozzle Temperature')
        plt.xlabel('Time')
        plt.draw()
        plt.pause(0.0001)


ser.write(b'M104 S0\r\n')               ## turns off nozzle heater
time.sleep(1)
ser.write(b'M106 S255\r\n')             #Start cooling down the nozzel for future PID tests

print('Please enter a filename for the nozzle graph and the data (.txt) document (no punctuation except \'-\' and \'_\'):')
figname= input(">>")

plt.savefig(figname + '.pdf', bbox_inches='tight')
np.save(figname + 'temp', nozzle_data)
np.save(figname + 'targets', targets)
np.save(figname + 'times', t)

ser.close()
print('done')

##


