# Bot Majestic

Модульный Discord-бот с асинхронными обработчиками событий, командами в cogs и централизованным журналированием ошибок.

## Возможности

- загрузка команд как расширений;
- обработка событий Discord;
- JSON-конфигурация префикса и параметров команд;
- HTTP-запросы через aiohttp;
- журналирование команд и ошибок.

## Технологии

Python, discord.py, asyncio, aiohttp, JSON.

## Структура

```text
bot.py                 запуск бота и загрузка расширений
cogs/main_commands.py  команды и прикладная логика
```

## Запуск

```bash
pip install discord.py aiohttp
```

Задайте `DISCORD_BOT_TOKEN`, создайте локальный `config.json` с полем `prefix` и запустите:

```bash
python bot.py
```
