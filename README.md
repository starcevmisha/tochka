Для запуска используйте **start.bat**

 http://127.0.0.1 - можно добавить тестового пользователя и узнать состояние всех пользователей

Пример использования

> GET http://127.0.0.1/api/status?uuid=ab1f7e4c73eb466db873a01cb667dd2

```
Ответ
{
  "addition": {
    "balance": 3900, 
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