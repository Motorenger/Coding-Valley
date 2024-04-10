<div align="center">
<img width="500 "alt="logo" src="https://user-images.githubusercontent.com/88438873/217668930-e89ec310-afc0-4c0e-b358-01212ccbebac.png">
<b>
</b>
<h1>Welcome to the Coding Valley Api Repository</h1>


<a href="https://nvkuntsevych.github.io/codingvalley-documentation/"><img src="https://img.shields.io/badge/Codng%20Valley-Documentation-green?style=for-the-badge?style=for-the-badge&logo=appveyor)" height="25px"></a>

</div>


## Requirements 
<div align="left">

|                          Technology                          |      Version       |
| :----------------------------------------------------------: | :----------------: |
|           [**django**](https://pypi.org/project/Django/)           |      **4.1.6**       |
|           [**redis**](https://pypi.org/project/redis/)           |      **4.4.2**       |
|           [**celery**](https://pypi.org/project/celery/)           |      **5.5.2**       |
|           [**aiohttp**](https://pypi.org/project/aiohttp/)           |      **3.8.4**       |
|           [**pytest**](https://pytest.readthedocs.io/en/latest/)           |      **4.5.2**       |


</div>

Check out the `requirements.txt` for the whole list of requirements.

## Installation

Simply clone the repo.

```
git clone https://github.com/igorkaruna/codingvalley.git
```

## Running

The project have multi-service architecture. Use `docker-compose` to 
spin up all containers.

```
docker-compose -f docker-compose.prod.yml up --build
```
