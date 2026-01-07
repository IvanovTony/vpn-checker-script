# 🛡 VPN Checker & Aggregator (Raw/Beta Version)

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/IvanovTony/vpn-checker-script/run_check.yml?label=Auto-Check&style=for-the-badge)

**ПРЕДУПРЕЖДЕНИЕ:** Это ранняя (сырая) версия скрипта. Возможны ошибки при плохом соединении с GitHub и ложные срабатывания при проверке.

Скрипт для автоматического сбора, валидации и сортировки VLESS/VMess/Trojan конфигураций. Работает полностью на GitHub Actions (бесплатно, сервер не нужен).

---

## 🚀 Основные возможности

1.  **Smart Chunking (Умная разбивка):** Защита от слишком больших файлов подписки. Если рабочих ключей > 1000, скрипт автоматически делит их на `part1.txt`, `part2.txt`, чтобы клиенты (Hiddify, v2rayNG) не зависали.
2.  **Гео-Сортировка:**
    *   🇷🇺 **RU_Best** — Российские ключи (белые списки, гос. сервисы).
    *   🇪🇺 **My_Euro** — Чистая Европа (NL, DE, FI, FR...). Остальное отсеивается.
3.  **Генератор подписок:** Создает единый файл `subscriptions_list.txt` со всеми готовыми ссылками.
4.  **Валидация:** Реальная проверка соединения через сокеты (TCP/TLS) с замером пинга.
5.  **Фильтр мусора:** Автоматически удаляет дубликаты, Китай (CN), Иран (IR) и локальные IP.

---

## 📂 Результат работы

После запуска в папке `checked` появляются файлы.
В файле `subscriptions_list.txt` будут готовые ссылки такого вида:

**Если ключей мало:**
`https://raw.githubusercontent.com/USER/REPO/main/checked/RU_Best/ru_white.txt`

**Если ключей много (авто-разбивка):**
`https://raw.githubusercontent.com/USER/REPO/main/checked/RU_Best/ru_white.txt`
`https://raw.githubusercontent.com/USER/REPO/main/checked/RU_Best/ru_white_part2.txt`

*(Ссылки генерируются автоматически и всегда ведут на существующие файлы)*

---

## 🛠 ИНСТРУКЦИЯ: Установка и Запуск

Делайте строго по шагам, чтобы скрипт заработал в вашем репозитории.

### Шаг 1. Сделайте Fork
1.  Нажмите кнопку **Fork** (вверху справа).
2.  Назовите репозиторий (например, `vpn-checker`).
3.  Нажмите **Create fork**.

### Шаг 2. Включите права (Permissions) — ВАЖНО!
Скрипту нужно разрешение на запись файлов в репозиторий.
1.  В новом репозитории перейдите в **Settings**.
2.  Слева выберите **Actions** -> **General**.
3.  Прокрутите вниз до **Workflow permissions**.
4.  Выберите пункт: **Read and write permissions**.
5.  Нажмите **Save**.

### Шаг 3. Настройка скрипта (main.py)
Откройте файл `main.py` и отредактируйте 3 обязательных пункта под себя:

**1. Ваш канал/метка (Строка 33):**
MY_CHANNEL = "@your_channel_name"

Будет отображаться в названии каждого ключа
text

**2. Ваши источники (Строка 46):**
URLS_MY = [
"https://raw.githubusercontent.com/..."
]

Вставьте сюда ссылки на ваши RAW файлы с ключами.
text

**3. Ваш репозиторий (Строка 188) — КРИТИЧНО:**
GITHUB_USER_REPO = "ВАШ_НИК/НАЗВАНИЕ_РЕПОЗИТОРИЯ"

Например: "ivanov/vpn-checker". Без этого ссылки в файле подписок будут вести на чужой репо.
text

### Шаг 4. Запуск
1.  Перейдите во вкладку **Actions**.
2.  Нажмите зеленую кнопку **I understand my workflows...**.
3.  Выберите воркфлоу **Check VPN Keys** слева.
4.  Нажмите **Run workflow**.

---

## 🤖 Telegram Bot (24/7 Работа)

Проект включает Telegram бот для удобного доступа к ключам с круглосуточной работой!

### 📱 Команды бота
- `/start` - Приветствие
- `/help` - Помощь
- `/ru` - Ключи для России
- `/all` - Все ключи
- `/vless` - Топ-50 VLESS ключей России
- `/fast` - Самый быстрый VLESS ключ России
- `/random` - 5 случайных VLESS ключей России
- `/status` - Статус ключей

### 🚀 Запуск 24/7 Бота

1. **Получите токен** у [@BotFather](https://t.me/BotFather):
   - `/newbot`
   - Имя: `VPN Checker Script`
   - Юзернейм: `vpn_checker_script_bot`

2. **Настройте .env файл:**
   ```bash
   cp .env.example .env
   # Добавьте TELEGRAM_BOT_TOKEN в .env
   ```

3. **Выберите способ развертывания:**

   ### 🏆 Вариант 1 - Docker (Рекомендуется)
   ```bash
   # 1. Настройте .env файл
   cp .env.example .env
   echo "TELEGRAM_BOT_TOKEN=your_token_here" >> .env
   
   # 2. Запустите с автоперезапуском
   docker-compose up -d
   
   # 3. Проверьте статус
   docker-compose logs vpn-bot
   ```
   
   **✅ Преимущества Docker:**
   - 🔄 Автоматический перезапуск каждый час
   - 🏥 Health checks каждые 60 секунд  
   - 💾 Постоянное хранилище ключей
   - 🚀 Автовосстановление после ошибок
   - 📊 Логирование работы

   ### 🔧 Вариант 2 - VPS/Server
   ```bash
   # 1. Клонируйте репозиторий
   git clone https://github.com/IvanovTony/vpn-checker-script.git
   cd vpn-checker-script
   
   # 2. Настройте окружение
   cp .env.example .env
   echo "TELEGRAM_BOT_TOKEN=your_token_here" >> .env
   
   # 3. Установите зависимости
   pip3 install -r requirements.txt
   
   # 4. Запустите с менеджером процессов
   pm2 start run_bot.py --name vpn-bot --restart-delay 3000
   pm2 save
   pm2 startup
   ```
   
   ### 🌐 Вариант 3 - Авто-развертывание на сервер
   ```bash
   # 1. Добавьте секреты в GitHub:
   # Settings > Secrets and variables > Actions
   # DOCKER_USERNAME, DOCKER_PASSWORD
   # DEPLOY_SERVER_HOST, DEPLOY_SERVER_USER, DEPLOY_SERVER_KEY
   # TELEGRAM_BOT_TOKEN, CHAT_ID
   
   # 2. Запустите развертывание:
   # Actions > Deploy 24/7 Bot > Run workflow
   
   # 3. Бот автоматически развернется на вашем сервере
   ```

   ### 🧪 Вариант 4 - GitHub Actions (Только тестирование)
   ```bash
   # Добавьте TELEGRAM_BOT_TOKEN в GitHub Secrets
   # Actions > Run Telegram Bot > Run workflow
   # Работает 5 минут для проверки
   ```

### 📊 Мониторинг и обслуживание

**Docker команды:**
```bash
# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f vpn-bot

# Перезапустить
docker-compose restart vpn-bot

# Остановить
docker-compose down

# Обновить
docker-compose pull && docker-compose up -d
```

**PM2 команды:**
```bash
# Проверить статус
pm2 status

# Посмотреть логи
pm2 logs vpn-bot

# Перезапустить
pm2 restart vpn-bot

# Остановить
pm2 stop vpn-bot
```

### ⚡ Возможности 24/7 бота

- **🔄 Автоперезапуск:** Каждый час для стабильности
- **🏥 Health Checks:** Проверка работоспособности каждую минуту
- **💾 Persistent Storage:** Ключи сохраняются между перезапусками
- **🚀 Error Recovery:** Автовосстановление после сбоев
- **📱 Все команды:** Работают 24/7 без перерывов
- **📊 Логирование:** Детальные логи для диагностики
- **🔄 Auto-update:** Автоматическое обновление при пуше в main

---

## ⚙️ Технические настройки (Опции скрипта)

Описание переменных в начале файла `main.py` для тех, кто хочет изменить логику:

*   **TIMEOUT (5):** Время ожидания ответа от сервера в секундах.
*   **THREADS (40):** Количество потоков проверки. Больше 50 ставить не рекомендуется (GitHub может забанить).
*   **CACHE_HOURS (12):** Время хранения истории. Если сервер проверен менее 12 часов назад, он не проверяется повторно.
*   **CHUNK_LIMIT (1000):** Максимальное количество ключей в одном файле перед разбивкой на части.
*   **MAX_KEYS_TO_CHECK (15000):** Лимит входящих ключей. Если ссылок больше, лишние отбрасываются для экономии ресурсов.
*   **EURO_CODES:** Список кодов стран, которые считаются "Европой".
*   **BAD_MARKERS:** Стоп-слова (CN, IR, RELAY), при наличии которых ключ удаляется сразу.

---
