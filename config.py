import os

from ds18b20 import initialize_modules, get_temp_sensor_file_location


class Config(object):
    initialize_modules()

    TEMP_SENSOR_FILE_LOCATION = get_temp_sensor_file_location()

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "mysql+pymysql" + "://" + "root" + ":" + "password" + "@" + "192.168.1.3" + ":" + "3307" + "/" + "tempread"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

