# tempread
Basic functionality for rest api serving up the current temperature using a RaspberryPi 3, DS18B20 temp sensor, Flask, gunicorn and nginx.

#Hardware setup:(Coming soon)

#Running the tempread Flask app with Gunicorn application server and nginx:
install python, nginx
pip install virtualenv
in virtualenv, pip install gunicorn, flask

#create virtualenv
mkdir projectname #where virtualenv will be created
virtualenv projectname
#activate virtualenv for development
source projectname/bin/activate
#to deactivate virtualenv
deactivate

#run gunicorn
gunicorn --bind 0.0.0.0:8000 wsgi

#configure nginx to proxy requests in a new sites-available
server {
  listen 80;
  server_name 0.0.0.0:8000; #I think this can be anything

  location / {
    proxy_pass http://0.0.0.0:8000;
  }
}

#create link to sites-enabled
sudo ln -s /etc/nginx/sites-available/tempread /etc/nginx/sites-enabled

sudo service nginx start/restart

notes*
var/log/nginx/access.log

