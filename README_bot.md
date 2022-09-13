# Документация API v1 для бота

## Создание пользователя
### authtoken/users/
#### POST
Создаёт пользователя.
- Запрос:
```json
{
  "username": "john_the_best",
  "first_name": "John",
  "last_name": "Doe",
  "vkontakte_id": 1,
  "telegram_id": 0
}
```

- Ответ:
```json
{
  "username": "john_the_best",
  "first_name": "John",
  "last_name": "Doe",
  "vkontakte_id": 1,
  "telegram_id": 0,
  "server_uuid": "3f2ce827-d276-417c-a29a-b34b90a4bb94"
}
```

## Деактивация пользователя
### users/is_active/`uuid:user`
#### PUT, PATCH
Деактивирует пользователя.
- Запрос:
```json
{
  "is_active": false
}
```

- Ответ:
```json
{
  "id": "27d3a710-ddbb-4aed-8c49-bb5084053b8f",
  "is_active": false
}
```
