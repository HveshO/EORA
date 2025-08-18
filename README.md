# EORA LLM QA Demo

## Описание
Сервис для ответов на вопросы потенциальных клиентов с использованием материалов EORA.

### Технологии
- Python 3.x
- OpenAI GPT-4 / GigaChat
- FastAPI для HTTP API
- Парсер архивных страниц/файлов с eora.ru
- CLI и Telegram-бот

### Использование

1. Склонируйте репозиторий
2. Запустите парсер для предзагрузки материалов:  
    `python core/crawler.py`
3. Запустите API:  
    `python core/api.py`
4. (По желанию) используйте CLI или Telegram-бота

### Примеры вопрос-ответ
Вопрос: "Что вы делаете для ритейла?"
Ответ:
> Мы реализовали HR-бота для Магнита[] и визуальный поиск для KazanExpress[].

### Ссылки на материалы
-  https://eora.ru/cases/chat-boty/hr-bot-dlya-magnit-kotoriy-priglashaet-na-sobesedovanie
-  https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto

## Оценка качества

Описание метрик, ограничения.

## Roadmap
...
