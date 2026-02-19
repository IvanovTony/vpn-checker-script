# 🛡 VPN Checker & Aggregator

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/IvanovTony/vpn-checker-script/run_check.yml?label=Auto-Check&style=for-the-badge)

Автоматический сбор, проверка и сортировка VLESS/VMess/Trojan/Shadowsocks конфигураций. Работает на GitHub Actions — сервер не нужен.

---

## 🚀 Возможности

| Функция | Описание |
|---------|----------|
| **Smart Chunking** | Автоматическое разделение файлов при >1000 ключей (защита от зависания клиентов) |
| **Гео-сортировка** | 🇷🇺 RU_Best — Россия, 🇪🇺 My_Euro — Европа (NL, DE, FI, FR и др.) |
| **Валидация** | Реальная проверка соединения (TCP/TLS/WebSocket) с замером пинга |
| **Фильтрация** | Удаление дубликатов, CN, IR, KR, локальных IP |
| **Telegram бот** | Удобный доступ к ключам через бота |


---

## 🛠 Установка

### Шаг 1: Fork репозитория

1. Нажмите **Fork** в правом верхнем углу
2. Создайте репозиторий (например, `vpn-checker`)

### Шаг 2: Настройка прав (Workflow Permissions)

1. Перейдите в **Settings** → **Actions** → **General**
2. В разделе **Workflow permissions** выберите **Read and write permissions**
3. Нажмите **Save**

### Шаг 3: Конфигурация

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Или настройте переменные в GitHub Actions:

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `MY_CHANNEL` | Название канала/метка в ключах | `@vpnCheckerScript` |
| `GITHUB_USER_REPO` | Ваш репозиторий | `username/repo-name` |
| `GITHUB_BRANCH` | Ветка | `main` |
| `TIMEOUT` | Таймаут проверки (сек) | `5` |
| `THREADS` | Количество потоков | `40` |
| `CHUNK_LIMIT` | Макс. ключей в файле | `1000` |
| `MAX_KEYS_TO_CHECK` | Лимит входящих ключей | `15000` |
| `CACHE_HOURS` | Время кэширования (часы) | `12` |

### Шаг 4: Добавление источников

Отредактируйте `main.py`:

```python
# Ваши источники ключей (строка ~33)
URLS_MY = [
    "https://raw.githubusercontent.com/user/repo/main/keys.txt",
]

# Российские источники (строка ~26)
URLS_RU = [
    "https://example.com/ru_keys.txt",
]
```

### Шаг 5: Запуск

1. Перейдите во вкладку **Actions**
2. Нажмите **I understand my workflows...**
3. Выберите **Check VPN Keys**
4. Нажмите **Run workflow**

---

## 🤖 Telegram Бот

### Команды

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие |
| `/help` | Список команд |
| `/ru` | Все ключи для России |
| `/all` | Все ключи (RU + EU) |
| `/vless` | Топ-50 VLESS ключей России |
| `/fast` | Топ-5 самых быстрых VLESS |
| `/random` | 5 случайных VLESS из топ-1000 |
| `/status` | Статус и количество ключей |

### Деплой на Railway.app

1. Создайте бота через [@BotFather](https://t.me/BotFather) и получите токен
2. Зарегистрируйтесь на [Railway.app](https://railway.app)
3. Подключите GitHub репозиторий
4. Добавьте переменную окружения:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather
   ```
5. Деплой запустится автоматически

---

## ⚙️ Технические детали

### Поддерживаемые протоколы

- ✅ VLESS (TLS, Reality, WebSocket)
- ✅ VMess (TLS, WebSocket)
- ✅ Trojan
- ✅ Shadowsocks

### Фильтрация

Автоматически удаляются:
- Дубликаты
- Страны: CN (Китай), IR (Иран), KR (Корея)
- Локальные IP (127.0.0.1, localhost)
- RELAY и POOL соединения

### Европейские страны

```
NL, DE, FI, GB, FR, SE, PL, CZ, AT, CH, IT, ES, NO, DK, BE, IE, LU, EE, LV, LT
```

---

## 📋 Архитектура

```
┌─────────────────┐     Каждые 4 часа     ┌─────────────────┐
│  GitHub Actions │ ────────────────────► │     main.py     │
│  (автозапуск)   │                       │  (проверка)     │
└─────────────────┘                       └────────┬────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │    checked/     │
                                          │  (результаты)   │
                                          └────────┬────────┘
                                                   │
                                                   ▼
┌─────────────────┐    Читает файлы      ┌─────────────────┐
│  Telegram Bot   │ ◄─────────────────── │   Railway.app   │
│  (пользователи) │                      │   (хостинг)     │
└─────────────────┘                      └─────────────────┘
```

---

## 🔧 Локальный запуск

```bash
# Клонирование
git clone https://github.com/YOUR_USERNAME/vpn-checker-script.git
cd vpn-checker-script

# Установка зависимостей
pip install -r requirements.txt

# Настройка
cp .env.example .env
# Отредактируйте .env

# Запуск проверки
python main.py

# Запуск бота
python telegram_bot.py
```

---

## 📄 Лицензия

MIT License — используйте свободно.

---

## 🤝 Вклад

Pull requests приветствуются! Для крупных изменений сначала откройте issue.

---

> ⚠️ **Дисклеймер**: Проект предназначен только для образовательных целей. Используйте ответственно и в соответствии с законодательством вашей страны.