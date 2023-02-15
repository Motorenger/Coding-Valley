<div align="center">
<img width="500 "alt="logo" src="https://user-images.githubusercontent.com/88438873/217668930-e89ec310-afc0-4c0e-b358-01212ccbebac.png">
<b>
</b>
<h1>Welcome to the Coding Valley Api Repository</h1>

<a href="https://codingvalley.tech/login/"><img src="https://img.shields.io/badge/Coddng%20Valley-API-orange?style=for-the-badge?style=for-the-badge&logo=appveyor)" height="25px"></a>
<a href="https://igorkaruna.github.io/codingvalley/"><img src="https://img.shields.io/badge/Codng%20Valley-Documentation-green?style=for-the-badge?style=for-the-badge&logo=appveyor)" height="25px"></a>

**LIVE DEMO: https://codingvalley.tech/login/**
</div>


<br/>


## SQL Diagram

![drawSQL-coding-valley-export-2023-02-15](https://user-images.githubusercontent.com/88438873/219054988-00067110-5d1f-4af7-9ba5-ee90f712471c.png)


## Getting Started 

If you are trying to use this project for the first time, you can get up and running by following these steps.

## Requirements 
<div align="center">

|                          Technology                          |      Version       |
| :----------------------------------------------------------: | :----------------: |
|           [**django**](https://pypi.org/project/Django/)           |      **4.1.6**       |
|           [**djangorestframework**](https://pypi.org/project/djangorestframework/)           |      **3.14.0**       |
|           [**djangorestframework-simplejwt**](https://pypi.org/project/djangorestframework-simplejwt/)           |      **5.22**       |
|           [**django_debug_toolbar**](https://pypi.org/project/django-debug-toolbar/)           |      **3.8.1**       |
|           [**django-cors-headers**](https://pypi.org/project/django-cors-headers/)           |      **3.13.0**       |
|           [**requests**](https://pypi.org/project/requests/)           |      **2.28.2**       |
|           [**pytest-django**](https://pytest-django.readthedocs.io/en/latest/)           |      **4.5.2**       |
|           [**pytest-xdist**](https://pypi.org/project/pytest-xdist/)           |      **3.2.0**       |
|           [**pytest-mock**](https://pypi.org/project/pytest-mock/)           |      **3.10.0**       |
|           [**model-bakery**](https://pypi.org/project/model-bakery/)           |      **1.10.1**       |
|           [**flake8**](https://pypi.org/project/flake8/)           |      **6.0.0**       |
|           [**shortuuid**](https://docs.python.org/3/)           |      **1.10.11**       |
|           [**gunicorn**](https://pypi.org/project/gunicorn/)           |      **20.1.0**       |
|           [**redis**](https://pypi.org/project/redis/)           |      **4.4.2**       |
|           [**celery**](https://pypi.org/project/celery/)           |      **5.5.2**       |
|           [**django-redis**](https://pypi.org/project/django-redis/)           |      **5.2.0**       |
|           [**aiohttp**](https://pypi.org/project/aiohttp/)           |      **3.8.4**       |
|           [**asgiref**](https://pypi.org/project/asgiref/)           |      **3.6.0**       |


</div>

## Install and Run

Make sure you have **Python 3.x** & docker installed.

Clone the repository using the following command

```
git clone https://github.com/igorkaruna/codingvalley.git
or 
bash git clone git@github.com:igorkaruna/codingvalley.git

# After cloning, move into the directory having the project files using the change directory command
cd codingvalley
```

Run the development server
```
docker-compose -f docker-compose.dev.yml up --build
```

Run the production server
```
docker-compose -f docker-compose.prod.yml up --build
```
