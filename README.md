# Foodgram — социальная сеть для обмена рецептами. (Яндекс.Практикум)

## Основные функции проекта
- регистрация пользователей, подписка на пользователей
- создание записей рецептов, с тегами и ингредиентами
- редактирование и удаление записей, просмотр чужих, фильтрация по тегам

## Стек
### Frontend
  - React
### Backend
  - Python
  - Django
  - DRF
  - Nginx
  - gunicorn

## Развертывание проекта и виртуального окружения
- создание локальной копии: 'git clone <SSH-ссылка>'
- создание виртуального окружения: 'python3 -m venv env'
- активация окружения: 'source env/bin/activate'
- установка необходимых пакетов 'pip install -r requirements.txt`

## Прописывание переменных окружения
- в корне проекта создать файл .env
- в файле .env прописать:
DEBUG=False
SECRET_KEY='(o*sf68hb$hray@(6jrdz)jh#x^3&k)74+85$uw85!ja=3#n95'
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432

## Автор
[TheHeroWorld](https://github.com/TheHeroWorld)

## Сервер
http://51.250.103.42/
Логин admin
Пароль admin
