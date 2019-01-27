import os

from ds18b20 import initialize_modules, get_temp_sensor_file_location


class Config(object):
    initialize_modules()

    TEMP_SENSOR_FILE_LOCATION = get_temp_sensor_file_location()

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "mysql+pymysql" + "://" + "root" + ":" + "password" + "@" + "localhost" + ":" + "3306" + "/" + "tempread"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER') or 'amqp://localhost' # use env var or default rabbit mq uri
    # TODO: optionally add CELERY_BACKEND for celery result consumer

