# verifySender.py

Служит для отправки кода подтверждения на почту.

## class Message

```python
def __init__(self,
    from_mail: str,
    from_password: str,
    to_mail: str,
    subject: str,
    text: str,
    to_name: str = ''
):
...
```

from_email - email адрес отправителя  
from_password - пароль email отправителя  
to_mail - email адрес получателя  
subject - тема сообщения  
text - текст сообщения, под форматирование  
(пример: `'Здравствуйте, {}! {} Это Ваш код подтверждения!'`,  
вывод: `Здравствуйте, имя! 111111 Это Ваш код подтверждения!`)  
to_name - имя отправителя (необязательно)  

***

```python
def send_verify_message(
    self,
    smtp_host: str,
    smtp_port: int
): # возвращает код подтверждения (str)
```

smtp_host - адрес SMTP сервера  
smtp_port - порт SMTP сервера

## function getSMTPServer (в разработке)

```python
def getSMTPServer(mail_service: str): # возвращает два параметра - адрес и порт SMTP сервера
```

mail_service - название почтового клиента
