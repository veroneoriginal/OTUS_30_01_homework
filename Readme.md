# Simple HTTP Server

Простой HTTP-сервер на Python, реализующий часть протокола HTTP
(GET и HEAD) без использования сторонних HTTP-библиотек.
Сервер написан на базе сокетов и предназначен для учебных целей —
разобраться, как реально работает HTTP «под капотом».

---

## Архитектура

**Thread-per-connection (threading)**

- Каждое входящее соединение обрабатывается в отдельном потоке
- Потоки создаются динамически (`threading.Thread`)
- Реализация без пула потоков


---

## Реализованный функционал

- Поддержка методов **GET** и **HEAD**
- Для неподдерживаемых методов возвращается **405 Method Not Allowed**
- Отдача статических файлов из `DOCUMENT_ROOT`
- Поддержка `index.html` для директорий
- Корректные HTTP-статусы:
  - `200 OK`
  - `403 Forbidden`
  - `404 Not Found`
  - `405 Method Not Allowed`
- Защита от directory traversal (`..`)
- Поддержка URL-encoded имён файлов (`%20`, `%XX`)
- Корректные `Content-Type` для:
  - `.html`
  - `.css`
  - `.js`
  - `.jpg`, `.jpeg`
  - `.png`
  - `.gif`
  - `.swf`
- Корректная работа метода **HEAD**
  - тело не возвращается
  - `Content-Length` соответствует GET
- Корректные HTTP-заголовки:
  - `Date`
  - `Server`
  - `Content-Length`
  - `Content-Type`
  - `Connection`

---

## Запуск сервера
python httpd.py

---
### Сайт данный в задании и главная корректно запускаются
http://localhost:8080/httptest/wikipedia_russia.html
http://localhost:8080/
