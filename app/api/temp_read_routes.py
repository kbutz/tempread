# from app.models import TemperatureReading
from app import celery
from ds18b20 import read_temp_in_f
from . import api


@api.route('/temp')
def temperature():
    # Example logging to DB on each read
    # current_temp = read_temp()
    # temp_row = TemperatureReading()
    # temp_row.temp_in_f = float(current_temp)
    # temp_row.add()

    # Example kicking off an async celery task
    # async_task.delay()
    return "{\"rawTemp\":\"" + str(read_temp_in_f()) + "\"}"

@celery.task
def async_task():
    print("Example async task task")
