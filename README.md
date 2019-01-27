# tempread
Basic functionality for rest api serving up the current temperature using a RaspberryPi 3, DS18B20 temp sensor, Flask, gunicorn and nginx.

#### Hardware setup:
* Raspberry-pi
* DS18B20 one-wire temp sensor
* Breadboard and jumper wires

A good place to get started is Adafruit's walkthrough: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware


#### Running the tempread app locally with Gunicorn application server and nginx and/or Pipenv:

install/update python3, nginx

pip3 install pipenv

To run in pipenv:

* ```pipenv shell```
* ```pipenv install --ignore-pipfile```
* ```gunicorn --bind 0.0.0.0:8000 wsgi```

To exit app and pipenv:

* ```ctrl + c to quit gunicorn```
* ```exit``` to leave pipenv

To run outside of the pipenv, you'll just need to pip install flask and gunicorn, clone this repo, and:
```gunicorn --bind 0.0.0.0:8000 wsgi```


####Running Celery with RabbitMQ
To run a basic RabbitMQ instance from docker w/ management plugin:
* ```docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management```
* You can manage your RabbitMQ instance at `http://localhost:15672`

For Celery config:
* In config.py, set your celery broke url (our rabbit mq instance) and optionally a celery backend for handling or persisting celery responses
* Run your celery work: `celery worker -A celery_worker.celery --loglevel=info`

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

