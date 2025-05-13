Robby Sitanala Python Job Test
May 13 2025


# Installation
For docker
```shell
docker compose up -d
docker compose up run --rm python manage.py makemigrations
docker compose up run --rm python manage.py migrate
docker compose up run --rm python manage.py loaddata fixtures/superuser.yaml
```

For non-docker
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/superuser.yaml
```