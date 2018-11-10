import os
import glob
import time

from flask import Flask
app = Flask(__name__)

@app.route('/')
def temperature():
    return "{\"rawTemp\":\"" + read_temp() + "\"}"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

try:
    # load the kernel modules needed to handle the sensor
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    #find the path of a sensor directory that starts with 28, the preface for the ds18b20 serial name
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
except Exception:
    print("Could not load temp sensor")

# open the file representing the sensor
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    try:
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return str(temp_f)
    except Exception as e:
        print("Error getting temp", e)
        return str(0)
