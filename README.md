ADRSIR-API
==========

ADRSIR-API is the API to control [ADRSIR](https://bit-trade-one.co.jp/product/module/adrsir/) (universal remote board for Raspberry Pi).

## Requirements
- python >= 3.7
- fastapi >= 0.63.0
- pydantic >= 1.8.1
- SQLAlchemy >= 1.3.23
- uvicorn >= 0.13.4
- smbus >= 1.1

## Usage

### Simplest way to run the app
Run the app with
```
$ uvicorn adrsir.main:app --host 0.0.0.0
```
and visit `<your raspberry pi IP>:8000/docs/` in your web browser.
You will see the interactive API documentation.

### Deploy with gunicorn and nginx
1. Edit `adrsir-api.service` to suite your environment.
```systemd
[Service]
# Modify to suit your environment
Type=notify
User=<user>
Group=<user_group>
WorkingDirectory=</path/to/this_app_directory>
ExecStart=</path/to/gunicorn> adrsir.main:app
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
```

2. Move `adrsir-api.service` and `adrsir-api.sock` to `/etc/systemd/system/`.
Then enable service and socket.
```
$ systemctl enable --now adrsir-api.socket
$ systemctl enable --now adrsir-api.service
```

3. Edit `adrsir-api.conf` to suite your environments.
It will be necessary to change `server_name`.
```nginx
# This is the Nginx configulation file
# Place this file /etc/nginx/conf.d
upstream api_server{
    server unix:/run/adrsir-api.sock fail_timeout=0;
}

server {
    listen 8000;
    listen [::]:8000;
    client_max_body_size 4G;
    # your Raspberry Pi's IP
    server_name raspberrypi.local;
    keepalive_timeout 5;
    location / {
      try_files $uri @proxy_to_api;
    }
    location @proxy_to_api {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_pass http://api_server;
    }
}
```

4. Move `adrsir-api.conf` to `/etc/nginx/conf.d` and restart nginx.
```
$ systemctl restart nginx
```
Visit `<your raspberry pi IP>:8000/docs/` in your web browser.
You will see the interactive API documentation.

## License
Copyright (c) 2021 Takayuki YANO

The source code is licensed under the MIT License, see LICENSE.
