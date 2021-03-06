import glob
import os
import time

from flask import current_app


def initialize_modules():
    # load the kernel modules needed to handle the sensor
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')


def get_temp_sensor_file_location():
    try:
        # From an Adafruit tutorial:
        # https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
        # base path of a sensor directory that starts with 28, the preface for the ds18b20 serial name
        base_dir = '/sys/bus/w1/devices/'
        # glob does unix style pathname pattern matching. If multiple sensors exist, an array of folders would be found
        device_folder = glob.glob(base_dir + '28*')[0]
        # The file under the 28-[serial_number] folder where we can find the temperature readings in C*1000
        return device_folder + '/w1_slave'
    except Exception as e:
        # TODO: It would be nice to user the flask logger when logging errors from config
        print("Could not load temp sensor file location:", e)
        return ""


# open the file representing the sensor
def read_temp_raw():
    f = open(current_app.config["TEMP_SENSOR_FILE_LOCATION"], 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp_in_f():
    try:
        lines = read_temp_raw()
        # E.g.: ['4a 01 4b 46 7f ff 0c 10 10 : crc=10 YES\n', '4a 01 4b 46 7f ff 0c 10 10 t=20625\n']
        # If the DS sensor reads YES at the end of the first line, a temperature reading will exist on the second line
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_f
    except Exception as e:
        current_app.logger.error("Error getting temp", e)
        return 0.0
