# Base Project

## Development environment
* Backend: Django + Postgresql
* Frontend: VueJS + Quasar

## To start the development environment
In the terminal write the following command:

```bash
docker-compose -f docker-compose-develop.yml up
```

If you want to rebuild the docker image run:

```bash
docker-compose -f docker-compose-develop.yml up --build
```

Now the application should be working when visiting the urls:
* Backend: http://127.0.0.1:8000/api/
* Frontend: http://127.0.0.1:8080/

The connection data to the database are the following:
* User: base-project
* Base de datos: base-project
* Password: base-project
* host: 127.0.0.1
* puerto: 5435

## To run django commands in the develop environment
The command must be executed as follows:
```bash
docker exec -it dev-base-project-backend python manage.py <commando>
```
Examples
```bash
docker exec -it dev-base-project-backend python manage.py makemigrations
docker exec -it dev-base-project-backend python manage.py migrate
docker exec -it dev-base-project-backend python manage.py createsuperuser
```
