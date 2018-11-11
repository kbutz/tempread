import glob
import os


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


class Config(object):
    initialize_modules()

    TEMP_SENSOR_FILE_LOCATION = get_temp_sensor_file_location()

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "mysql+pymysql" + "://" + "root" + ":" + "password" + "@" + "192.168.1.3" + ":" + "3307" + "/" + "tempread"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

