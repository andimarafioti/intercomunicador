import os, glob, time, sys, lcddriver

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'

def read_temp_raw():
    f_1 = open(device_file, 'r')
    lines_1 = f_1.readlines()
    f_1.close()
    return lines_1

def read_temp():
    lines = read_temp_raw()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')
    temp = float(lines[1][equals_pos+2:])/1000

    return temp
 
lcd = lcddriver.lcd()

lcd.lcd_display_string("Temperature", 1)

while True: #infinite loop
    temp = read_temp() #get the temp
    lcd.lcd_display_string('{0:.2f}'.format(temp) + " C", 2)
    time.sleep(5) 