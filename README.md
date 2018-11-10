# tempread
Basic functionality for rest api serving up the current temperature using a RaspberryPi 3, DS18B20 temp sensor, Flask, gunicorn and nginx.

Hardware setup:(Coming soon)

Running the tempread Flask app with Gunicorn application server and nginx:<br/>
install/update python3, nginx<br/>

pip3 install pipenv

To run in pipenv:

* ```pipenv shell```
* ```pipenv install --ignore-pipfile```
* ```gunicorn --bind 0.0.0.0:8000 wsgi```

To exist app and pipenv:

* ```ctrl + c to quit gunicorn```
* ```exit``` to leave pipenv

To run outside of the pipenv, you'll need to pip install flask and gunicorn:<br/>
gunicorn --bind 0.0.0.0:8000 wsgi

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

Create link to sites-enabled<br/>
sudo ln -s /etc/nginx/sites-available/tempread /etc/nginx/sites-enabled

sudo service nginx start/restart

notes*<br/>
var/log/nginx/access.log

