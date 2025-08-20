# EORA LLM QA Demo

## Описание
Сервис для ответов на вопросы потенциальных клиентов с использованием материалов EORA.

### Технологии
- Python 3.12
- LLM - mistralai/Mistral-7B-Instruct-v0.2
- LangChain
- FAISS
- telegram-бот
- pdm
## Входные данные
- data/urls.txt
## Хранилище
- data/faiss_index
### Использование
1.Склонируйте репозиторий
2. Настройте API ключ телеграм бота через @BotFather
3. Настройте API ключ для модели LLM https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
4. Иницализируйте в корне .env:
```
TELEGRAM_TOKEN=....
API_KEY=....
```
доп параметры:
```
DEBUG = True
BUILD_FAISS = True
TOP_K = 8
ANSWER_MAX_TOKENS = 700
ANSWER_TEMPERATURE = 0.3
PATH_FILE_URLS=/data/urls.txt
PATH_STORAGE_INDEX=/data/faiss_index
```
5. Запуск докер контейнера:
```docker compose up```
6. Запуск вне докер контейнера:
```pdm install
pdm run python src/main.py
```
### Примеры вопрос-ответ
Вопрос: "Что вы делаете для ритейла?"
Ответ:
> Мы реализовали HR-бота для Магнита[] и визуальный поиск для KazanExpress[].

## Трудности
UnstructuredURLLoader - с ним больше всего возилась так как функция в библиотеке не рабочая
а также с настройкой LLM
## Roadmap
- Если нужна расширяемость проекта то необходима реализация классов и di
- Если данных очень много - psql
- Есть логирование, но обработка ошибок может быть лучше
- Настройки модели нужно тонко подбирать
