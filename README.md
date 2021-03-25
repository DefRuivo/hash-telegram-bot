# hash-telegram-bot

Bot de telegram que pega um valor nos comandos guarda numa DB\
o valor transformado em hash e envia para o usuário, podendo fazer um novo valor de hash

## Requisitos

- [Python](https://www.python.org/): ^3.8

## Como instalar:

No terminal utilize os comandos:

```pip install -r requirements.txt```

## Como usar:

No terminal inicie o bot: ```python runner.py```\
No chat do telegram inicie a chamada do bot com /start\
O usuario vai receber uma mensagem para que envie ```/n Mensagem_Para_ser_Hasheada```\
Caso o usuário já tenha um hash na DB o bot vai enviar o hash assim que enviar ```/n```