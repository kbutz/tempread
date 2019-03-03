from app import celery, create_app
from app.models import TemperatureReading
from ds18b20 import read_temp_in_f

app = create_app()
app.app_context().push()

# Define celery beat schedule to run save_temperature task once every minute
celery.conf.beat_schedule = {
    'add-every-300-seconds': {
        'task': 'celery_worker.save_temperature',
        'schedule': 300.0
    },
}


# Define celery task to read temperature and save to DB
@celery.task
def save_temperature():
    current_temp = read_temp_in_f()
    temp_row = TemperatureReading()
    temp_row.temp_in_f = current_temp
    temp_row.add()
