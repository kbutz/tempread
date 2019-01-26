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

