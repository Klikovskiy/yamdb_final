# Учебный проект 16 спринта Яндекс Практикум. CI/CD API YAMDB.
## Описание проекта

Проект для публикаций отзывов пользователей на произведения. Категории произведений: «Книги», «Фильмы», «Музыка». Список категорий расширяемый.

Читатели оставляют к произведениям текстовые отзывы (Review) и выставляют рейтинг (оценку в диапазоне от 1 до 10).

Полная документация к API находится по эндпоинту: /redoc

## Как запустить проект
         
1. Клонируйте репозиторий и перейдите в него в командной строке:
```      
git clone https://github.com/klikovskiy/yamdb_final
cd yamdb_final
```      
2. Создайте в клонированной директории файл .env. Ниже приведен пример его наполнения:
```
DB_ENGINE=django.db.backends.postgresql # Указываем что работаем с Postgresql.
DB_NAME=postgres # Имя базы данных.
POSTGRES_USER=set_your_username # Логин для подключения к базе данных.
POSTGRES_PASSWORD=set_your_pwd # Пароль для подключения к базе данных.
DB_HOST=db # Название контейнера.
DB_PORT=5432 # Порт для подключения к Базе данных.
```
3. Запустите docker-compose. Для этого необходимо перейти в папку infra и выполнить команду:
```
docker-compose up -d
```
4. Проверьте, что контейнеры запустились:
```
docker container ls
```
5. Выполните миграции:
```
docker-compose exec web python manage.py migrate
```
6. Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
7. Подгрузите статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
8. Заполните базу данными:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Остановить работу контейнеров можно командой ```docker-compose down```.

Документация после запуска доступна по адресу [localhost/redoc](http://localhost/redoc/).

## Технологии
### API
- Python 3.7-slim
- Django 2.2.28
- Django Rest Framework 5.2.2
- PostgreSQL 13.0
- Gunicorn 20.0.4
- Nginx 1.21.3

### Контейнер
- Docker 20.10.22
- Docker Compose 2.15.1
