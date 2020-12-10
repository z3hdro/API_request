# API_request

Приложение для проверки списка URL-Адресов и внесения их в базу данных

стек: Django, Postgresql, Redis, Celery, Docker

## Установка
Для установки необходимо и использования необходимо иметь установленный docker и PyPI.

1. Клонируем данный репозиторий на устройство:
  ### `git clone https://github.com/z3hdro/API_request.git`

2. Переходим в папку проекта (cd API_request) и устанавливаем виртуальное окружение:
### ` python -m venv env`
   Активируем виртуальное окружение

3. Переходим в корень проекта (cd api) и устанавливаем все зависимости из requirements.txt:
### `pip install -r requirements.txt`
  !!!Для Ubuntu/Linux возможно возникновение ошибки, решение: 
  в файле requirements.txt
```python
psycopg2==2.8.6
#заменить вручную на 
psycopg2-binary==2.8.6
```
  После сохранения изменений снова вызвать:
  ### `pip install -r requirements.txt`
   
4. Далее, необходимо запустить docker и запустить контейнеры postgresql и redis:
## Redis
### `docker run --name {container name} -p {preferable port redis}:6379 -v {path to store backup}:/data redis`
## Docker
### `docker run --name {container name} -p {preferable port postgresql}:5432 -v {path to store data}:/var/lib/postgresql/data -e POSTGRES_PASSWORD={preferable password} postgres`

5. Открываем settings.py и записываем необходмые настройки:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'preferable password',
        'HOST': 'localhost',
        'PORT': 'preferable port postgresql',
    }
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://localhost:{preferable port redis}/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://localhost:{preferable port redis}/0")
```

6. Из корня проекта (в терминале) делаем миграцию:
  ### `python manage.py makemigrations`
  
  ### `python manage.py migrate`
  
7. Поднимаем отдельно в терминале из корня проекта celery:
  ### `celery -A api worker`
  
8. Запускаем из корня проекта(в терминале) сам проект:
  ### `python manage.py runserver`
 
## Использование
  В данном API есть:
  1. localhost:8000/ - запускает импорт всех данных из файла data.xlsx в базу данных postgres через Django ORM (data.xlsx должна лежать в корне проекта!).
  Возвращает id-task задачи Celery, которая будет импортировать данные в фоновом режиме.
  
  2. localhost:8000/tasks/id-task - возвращает статус задачи Celery (статус несуществующего id-task = PENDING).
  
  3. localhost:8000/api/check - запускает проверку доступности всех URL-адресов, которые лежат в базе данных.
  Если результаты не обновлялись в течение 30 секунд или отсутствуют, то для таких URL-адресов будет выполнена проверка.
  (Используем через Celery-tasks)
  
  4. localhost:8000/site_check?url=example.com - проверка статуса url-адрес (Пример: example.com).
  
  5. localhost:8000/admin - панель для админов. Необходимо создать superuser или использовать уже готового superuser-а:
  В терминале
   ### `python manage.py createsuperuser`
