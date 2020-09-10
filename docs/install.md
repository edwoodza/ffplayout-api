# Manuel Installation Guide

**We are assuming that the system user `www-data` will run all processes!**

### API Setup

##### Preparation
- clone repo to `/var/www/ffplayout`
- cd in root folder from repo
- add virtual environment: `virtualenv -p python3 venv`
- run `source ./venv/bin/activate`
- install dependencies: `pip install -r requirements-base.txt`
- cd in `ffplayout`
- generate and copy secret: `python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'`
- open **ffplayout/settings/production.py**
- past secret key in variable `SECRET_KEY`
- set `ALLOWED_HOSTS` with correct URL
- set URL in `CORS_ORIGIN_WHITELIST`
- migrate database: `python manage.py makemigrations && python manage.py migrate`
- collect static files: `python manage.py collectstatic`
- add super user to db: `python manage.py createsuperuser`
- populate some data to db: `python manage.py loaddata ../docs/db_data.json`
- run: `chown www-data. -R /var/www/ffplayout`

##### System Setup
- copy **docs/ffplayout-api.service** from root folder to **/etc/systemd/system/**
- enable service and start it: `systemctl enable ffplayout-api.service && systemctl start ffplayout-api.service`
- install **nginx**
- edit **docs/ffplayout.conf**
    - set correct IP and `server_name`
    - add domain `http_origin` test value
    - add https redirection and SSL if is necessary
- copy **docs/ffplayout.conf** to **/etc/nginx/sites-available/**
- symlink config: `ln -s /etc/nginx/sites-available/ffplayout.conf /etc/nginx/sites-enabled/`
- restart nginx
- run `visudo` and add:
    ```
    www-data ALL = NOPASSWD: /bin/systemctl start ffplayout-engine.service, /bin/systemctl stop ffplayout-engine.service, /bin/systemctl reload ffplayout-engine.service, /bin/systemctl restart ffplayout-engine.service, /bin/systemctl status ffplayout-engine.service, /bin/systemctl is-active ffplayout-engine.service, /bin/journalctl -n 1000 -u ffplayout-engine.service
    ```

### Frontend

**We need a recent version of npm**

- go to folder **/var/www/ffplayout/ffplayout/frontend**
- install dependencies: `npm install`
- create **.env** file:
    ```
    BASE_URL='http://localhost:3000'
    API_URL='/'
    ```
    - in dev mode `API_URL` should be: `http://localhost:8000`
    - for deactivating progress animation: `DEV=true`
- create symlink for the media folder
    - when your media folder is a subfolder (for example `/opt/ffplayout/media`) create the same folder structure under **static**:
        - `mkdir -p /var/www/ffplayout/ffplayout/frontend/static/opt/ffplayout`
    - `ln -s /opt/ffplayout/media /var/www/ffplayout/ffplayout/frontend/static/opt/ffplayout/`
- build app: `npm run build`

Your frontend should be now in **/var/www/ffplayout/ffplayout/frontend/dist** folder, which we are included already in the nginx config. You can serve now the GUI under your domain URL.

### OS Specific
On debian 10 you need to install:

```
apt install -y curl
```

```
curl -sL https://deb.nodesource.com/setup_12.x | bash -
```

**For full installation (with ffmpeg/srs):**
```
apt install -y sudo net-tools git python3-dev build-essential python3-virtualenv nodejs nginx autoconf automake libtool pkg-config yasm cmake curl mercurial git wget gperf mediainfo
```
