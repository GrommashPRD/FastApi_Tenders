# Перед началом работы:

Cоздайте свой **SECRET_KEY** для файла _.env.prod_

**_Windows:_**
```
from secrets import token_bytes
from base64 import b64encode
print(b64encode(token_bytes(32)).decode())
```
**_Linux/MacOs:_**
```
openssl rand -base64 32
```

# FastAPI проект - Сервис проведения тендеров

[Ссылка на адание](https://github.com/avito-tech/tech-internship/blob/main/Tech%20Internships/Backend/Backend-trainee-assignment-autumn-2024/Backend-trainee-assignment-autumn-2024.md)

1. `make start` - Формирование Docker - образа + запуск.
2. `make stop` - Остановка.
3. `make venv` - Создание виртуального окружения
4. `source venv/bin/activate` - Активация виртуального окружения
5. `make install` - Установка зависимостей проекта.
6. `make test` - Тестирование проекта.


# Регистрация и Авторизация
1. Создать пользователя. (Лучше создать два пользователя). \
Скопируйте user_id второго пользователя чтобы работать с ним по функционалу.

```
curl -X 'POST' \
  'http://localhost:8000/auth/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "testuser",
  "password": "testuser",
  "first_name": "test",
  "last_name": "test"
}'

curl -X 'POST' \
  'http://localhost:8000/auth/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "testuser2",
  "password": "testuser2",
  "first_name": "test2",
  "last_name": "test2"
}'
```

2. Авторизуйтесь в системе.

```
curl -X 'POST' \
  'http://localhost:8000/auth/login/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "testuser",
  "password": "testuser"
}'
```
# Организации и управление.

1. Создайте организацию. \
Вынесите для себя "organization_id" для дальнейшей работы.
Доступный тип организации `"IE", "LLC", "JSC"`
```
curl -X 'POST' \
  'http://127.0.0.1:8000/organisation/new/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Organization - 1",
  "description": "Description about org",
  "org_type": "IE"
}'
```


2. Тут вы можете добавить пользователя в вашу организацию, чтобы сделать его ответственным.

```
curl -X 'POST' \
  'http://localhost:8000/organisation/<ВАШ ORGANIZATION_ID>/add_users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  "<USER_ID ВТОРОГО СОЗДАННОГО ПОЛЬЗОВАТЕЛЯ>"
]'
```

# Тендеры.

1. Создание тендера. \
Только есть у вас есть организация. \
Тендер получает статус "CREATED", никто кроме Вас, его не видит, до тех пор, пока не опубликуете. 
```
curl -X 'POST' \
  'http://localhost:8000/tenders/new/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "testtenser",
  "description": "testtender",
  "service_type": "CONSTRUCTION"
}'
```

2. Получить список всех тендеров системы. \
Отображаются только опубликованные тендеры.
```
curl -X 'GET' \
  'http://localhost:8000/tenders/' \
  -H 'accept: application/json'
```

3. Отображает тендеры текущего пользователя(с любым статусом).
```
curl -X 'GET' \
  'http://localhost:8000/tenders/my/' \
  -H 'accept: application/json'
```

4. Получить информацию о статусе тендера. TENDER_ID можно получить из пункта 7. \
Если вы создатель тендера, вы увидите его любой статус, если вы не создатель то вы увидите статус тендера только после его публикации.
```
curl -X 'GET' \
  'http://localhost:8000/tenders/<ВАШ TENDER_ID>/status/' \
  -H 'accept: application/json'
```
5. Изменить статус тендера. \
Доступные варианты "PUBLISHED", "CLOSED".
```
curl -X 'PUT' \
  'http://localhost:8000/tenders/<ВАШ TENDER_ID>/status/?status=PUBLISHED' \
  -H 'accept: application/json'
```

6. Изменить информацию по тендеру.

```
curl -X 'PATCH' \
  'http://localhost:8000/tenders/<ВАШ TENDER_ID>/edit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "new description"
}'
```
7. Откатить тендер по версии. \
Тендер создается с версией 1, после внесения изменений, версия увеличивается на 1. \
После отката версия так же увеличивается на 1. 

```
curl -X 'PUT' \
  'http://localhost:8000/tenders/<ВАШ TENDER_ID>/rollback/<ВЕРСИЯ>' \
  -H 'accept: application/json'
```

# Предложения.

1. Создание предложения для тендера. \
Только для опубликованных тендеров.

```
curl -X 'POST' \
  'http://localhost:8000/bids/new/?tender_id=<TENDER_ID К КОТОРОМУ ДЕЛАЕТЕ ПРЕДЛОЖЕНИЕ>&is_from_organization=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "test",
  "description": "test"
}'
```

2. Все предложения текущего пользователя.
```
curl -X 'GET' \
  'http://localhost:8000/bids/my/' \
  -H 'accept: application/json'
```

3. Узнать статус для предложения. \
Доступно владельцам тендера и владельцу предложения.

```
curl -X 'GET' \
  'http://localhost:8000/bids/<TENDER_ID>/status/' \
  -H 'accept: application/json'
```
4. Изменение статуса для предложения. \
Только владелец предложения
```
curl -X 'PUT' \
  'http://localhost:8000/bids/<ID ВАШЕГО ПРЕДЛОЖЕНИЯ>/status/?status=PUBLISHED' \
  -H 'accept: application/json'
```
5. Показать все предложения для тендера. Для владельца тендера.
```
curl -X 'GET' \
  'http://localhost:8000/bids/<TENDER_ID ВАШЕГО ТЕНДЕРА>/list/' \
  -H 'accept: application/json'
```
6. Изменить параметры предложения. \
Только для владельца предложения.
```
curl -X 'PATCH' \
  'http://localhost:8000/bids/<BID_ID ВАШЕГО ПРЕДЛОЖЕНИЯ>/edit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "test1",
  "description": "test1"
}'
```
7. Откатить предложение по версии. \
Только для создателя предложения.\
Предложение создается с версией 1, после внесения изменений, версия увеличивается на 1. \
После отката версия так же увеличивается на 1. 
```
curl -X 'PUT' \
  'http://localhost:8000/bids/<BID_ID ВАШЕГО ПРЕДЛОЖЕНИЯ>/rollback/<ВЕРСИЯ>' \
  -H 'accept: application/json'
```
8. Написать отзыв о предложении. \
Только для владельца тендера \
к которому создавалось предложение.

```
curl -X 'PUT' \
  'http://127.0.0.1:8000/bids/<BID_ID ПРЕДЛОЖЕНИЯ>/feedback/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "feedback": "string"
}'
```

9. Вынесение решения по предложению. \
Только ответственные за организацию.
Доступные ответы "ACCEPTED", "REJECTED".
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/bids/<BID_ID ПРЕДЛОЖЕНИЯ>/submit_decision?status=<СТАТУС>' \
  -H 'accept: application/json'
```
_Если хотя бы один голос будет "REJECTED", предложение автоматически отклоняется и получает системный статус "CANCELED"_ \
**Для согласования предложения нужно получить решения больше или равно кворуму. \
Кворум = min(3, количество ответственных за организацию).** \
_Если предложение набирает нужное кол-во голосов, ТЕНЕДЕР автоматически закрывается, предложение победило._