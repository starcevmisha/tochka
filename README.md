Для запуска используйте **start.bat**
##### 0. Ping
``http://127.0.0.1/api/ping``

Ответ:

`pong`
____
##### 1. Посмотреть все аккаунты

`http://localhost` - информация обо всех акаунтах в удобочитаемом виде + создать новый аккаунт для тестовых целей
________________________________
##### 2. Добавить денег на счёт
`http://127.0.0.1/api/add?uuid=<uuid-счёта>&amount=<сумма>`

Пример ответа:
```
{
    "addition": {
        "balance": 3000,
        "created": "Sat, 19 Oct 2019 09:53:49 GMT",
        "fio": "oooo",
        "hold": 0,
        "last_update": "Sat, 19 Oct 2019 09:53:49 GMT",
        "status": "Active"
    },
    "description": "OK",
    "result": true,
    "status": 200
}
```

_________________________
#### 3. Заблокировать сумму на счёте с последующим вычетом этой суммы
`http://127.0.0.1/api/substract?uuid=<uuid-счёта>&amount=<сумма>`

Пример ответа:
```
{
    "addition": {
        "balance": 3000,
        "created": "Sat, 19 Oct 2019 09:53:49 GMT",
        "fio": "oooo",
        "hold": 300,
        "last_update": "Sat, 19 Oct 2019 09:53:49 GMT",
        "status": "Active"
    },
    "description": "OK",
    "result": true,
    "status": 200
}
```
____
#### 4.Статус счёта
`http://127.0.0.1/api/status?uuid=<uuid-счёта>` 

Пример ответа:
```
{
    "addition": {
        "balance": 3000,
        "created": "Sat, 19 Oct 2019 09:53:49 GMT",
        "fio": "oooo",
        "hold": 300,
        "last_update": "Sat, 19 Oct 2019 09:53:49 GMT",
        "status": "Active"
    },
    "description": "OK",
    "result": true,
    "status": 200
}
```

___
* Так как в условии тестового задания не было ничего сказана про тип метода, то все поддерживают и Get и Post
____
Очевидный минус - в воркере дублируется код моделей для подключения к базе, но к сожалению я так и 
не понял, как обойти это