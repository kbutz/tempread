# from app.models import TemperatureReading
from ds18b20 import read_temp_in_f
from . import api


@api.route('/temp')
def temperature():
    # TODO: We don't really want to save the temp everytime it is read - this will be done by a cron/celery job
    # current_temp = read_temp()
    # temp_row = TemperatureReading()
    # temp_row.temp_in_f = float(current_temp)
    # temp_row.add()
    return "{\"rawTemp\":\"" + read_temp_in_f() + "\"}"
