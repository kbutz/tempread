# tempread
REST api  and periodic task to record the temperature using Celery's heartbeat, serving up the current temperature using a RaspberryPi 3, DS18B20 temp sensor, Flask, gunicorn and optionally nginx.

#### Hardware setup:
* Raspberry-pi
* DS18B20 one-wire temp sensor
* Breadboard and jumper wires

V1 still in the breadboard:
![V1 Raspberry Pi # + DS18B20](https://i.imgur.com/dPu16Uy.jpg)

A good place to get started is Adafruit's walkthrough: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware


#### Running the tempread app locally with Gunicorn application server and nginx and/or from Pipenv:
Install/update python3, Flask, flask-sqlalchemy, PyMYSQL, Celery, gunicorn, nginx

pip3 install pipenv

To run in pipenv:

* ```pipenv shell```
* ```pipenv install --ignore-pipfile```
* ```gunicorn --bind 0.0.0.0:8000 wsgi```

To exit app and pipenv:

* ```ctrl + c to quit gunicorn```
* ```exit``` to leave pipenv

One liner to run a mysql server with docker for local testing:
* ```docker run --name mysql_container_name -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=example_db -p 3306:3306 -d mysql:5.7```

To run outside of the pipenv, you'll just need to pip install flask and gunicorn, clone this repo, and:
```gunicorn --bind 0.0.0.0:8000 wsgi```

Then you should be able to get a temperature reading on the /api/v1/temp endpoint:
```curl http://localhost:8000/api/v1/temp```


#### Running a Celery worker and beat with RabbitMQ
The intent here is to set up a periodic task leveraging Celery's heart-beat. If you only want to run the periodic task
and do not care about getting the temp over a rest endpoint, you only need to spin up the DB, RabbitMQ server and run the last command
to spin up a celery work and beat.

To run a basic RabbitMQ instance from docker w/ management plugin:
* ```docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management```
* You can manage your RabbitMQ instance at `http://localhost:15672`

For Celery config:
* In config.py, set your celery broke url (our rabbit mq instance) and optionally a celery backend for handling or persisting celery responses
* NOTE: Not needed, but useful if you want to call any other async tasks from Flask - Run your celery worker to pick up async tasks from Flask: `celery worker -A celery_worker.celery --loglevel=info`
* Run a celery worker and celery beat to pick up async tasks from Flask and the celery beat to periodically save temperature readings 
```celery -A celery_worker.celery worker -B --loglevel=info```

#### Optional nginx configuration
Configure nginx to proxy requests in a new sites-available<br/>
<pre>
server {
    listen 5000; # exposed port
    server_name localhost;

    location / {
        include proxy_params;
        proxy_pass http://0.0.0.0:8000; # gunicorn port
    }
}
</pre>

Create link to sites-enabled

```sudo ln -s /etc/nginx/sites-available/tempread /etc/nginx/sites-enabled```

```sudo service nginx start/restart```

