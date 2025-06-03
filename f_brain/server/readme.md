

```sh
cd f_brain/server

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# start new django project called server_config
django-admin startproject server_config .

# start new django app called weather
python manage.py startapp weather
```

```python
# add weather to INSTALLED_APPS in server_config/settings.py
INSTALLED_APPS = [
     ...
     'weather',
]
```

```sh
# make migrations
python manage.py makemigrations
# migrate
python manage.py migrate

# create superuser
python manage.py createsuperuser
# Username (leave blank to use 'awf'): admin
# Email address: admin@example.com
# Password: admin
# Password (again): admin
```

```sh
# build docker server image
docker build -t f_brain/server .
# or 

cd f_brain/server
docker build -t .