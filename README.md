# PHPSupportBot
https://t.me/PHPSupportBot

Это телеграм бот для администрирования сотрудничества между заказчиками и прогаммистами.

## Запуск

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте БД командой `python manage.py migrate`
- Запустите бота `py main.py`

## Администрирование
- Запустите сервер для администрирования командой `python manage.py runserver`
- Перейдите по адресу http://127.0.0.1:8000/admin
- Используйте данные для авторизации (Username: "username", Password: "password")
- Далее следуйте указаниям бота

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и 
запишите туда данные в таком формате: `BOT_TG_TOKEN=значение`.

где `BOT_TG_TOKEN` — токен для доступа к боту.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
 