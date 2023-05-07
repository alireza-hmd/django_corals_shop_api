# Corals 
 
## Settings
clone the project first:
```
git clone https://github.com/alireza-hmd/django_corals_shop_api.git
```
after this you need to configure some settings. create environment variable file in `core/.env` path and configure it for your own project.
there is a env.example file in the `core` directory that you can copy in your `.env` file and change it for your project. 
you can run this commands and get the same result but dont forget to change .env file (specially your Secret Key):
```
cd django_corals_shop_api
cp core/env.example core/.env
```

you can change package and author name in the `pyproject.toml` file but its not necessary.

## Docker
You should have docker installed on your machine. use this command to build the docker container:
```
docker-compose up --build
```
you can set database name anything you want but it should be the same name you set in the `core/.env` file.

## Run Project

now you are ready to develop your django project. visit this link and you will see api schema generated with swagger-ui:
```
http://localhost:8000/#/
```
## Schema
![api schema](https://github.com/alireza-hmd/django_corals_shop_api/blob/master/api_schema.jpg?raw=true)
