from app import celery, create_app
from app.models import TemperatureReading
from ds18b20 import read_temp_in_f

app = create_app()
app.app_context().push()

celery.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'celery_worker.save_temperature',
        'schedule': 60.0
    },
}


@celery.task
def save_temperature():
    current_temp = read_temp_in_f()
    temp_row = TemperatureReading()
    temp_row.temp_in_f = current_temp
    temp_row.add()
