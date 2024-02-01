# Planetarium API service 🪐
API service for managing Planetarium.  
Uses DRF under the hood.

## Installation using GitHub ⌨️

Install Postgres and create database.

Clone repo and create virtual environment:

```bash
git clone https://github.com/nsdNite/Planetarium-API-Service.git
cd Planetarium-API-Service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

set DJANGO_SECRET_KEY=<your django secret key>
set POSTGRES_HOST=<your database hostname>
set POSTGRES_DB=<your database name>
set POSTGRES_PASSWORD=<your database password>

python manage.py migrate
python manage.py runserver
```

## Run with docker 🐳

Docker should be installed first.

Run docker and, then run next:

```bash
docker-compose build
docker-compose up
```

API has management command to wait for Postgres roll out, so don't worry.

## Accessing API 🔓 

Creating user:  
/api/user/register/  

Get access token:  
/api/user/token/  

## Features ⭐

- JWT authentication
- Admin panel via /admin/
- Documentation via /api/doc/swagger/
- Managing Reservations and Tickets
- Creating instances of Astronomy Shows, Planetarium Domes, Show Themes
- Adding Show Sessions
- Filtering of Astronomy Shows and Planetarium Domes
- API test included
- Managing script to wait for database creation when using Docker

## Notes on JWT authentication 🪙

To access API with JWT token please install ModHeader extension:  
[ModHeader for Chrome](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj)  
[ModHeader for Firefox](https://addons.mozilla.org/uk/firefox/addon/modheader-firefox/)

Click on extension, paste your JWT auth token with prefix word "bearer", e.g. on picture below.  
Select Authorization request header and check the box.
You can now access other parts of API.



## DB structure 🗄️
![img.png](readme_media%2Fimg.png)

