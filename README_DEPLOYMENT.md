# 🚀 Развертывание Telegram Bot

## 📋 Требования

- Python 3.9+
- Токен Telegram Bot от @BotFather
- Сервер для постоянной работы бота

## 🔧 Настройка

### 1. Получение токена бота

1. Найдите в Telegram **@BotFather**
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Имя бота: `VPN Checker Script`
   - Юзернейм: `vpn_checker_script_bot`
4. Сохраните полученный токен

### 2. Настройка GitHub Secrets

1. Перейдите в ваш репозиторий: https://github.com/IvanovTony/vpn-checker-script
2. Настройки → Secrets and variables → Actions
3. Нажмите "New repository secret"
4. Создайте секрет:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: ваш токен от @BotFather

### 3. Установка команд бота

Откройте @BotFather и отправьте:
```
/setcommands
```

Выберите вашего бота и вставьте команды:
```
start - 🎉 Запустить бота
help - 📖 Показать помощь
ru - 🇷🇺 Получить ключи для России
all - 🌍 Получить все ключи
vless - ⚡ Топ-50 VLESS ключей России
fast - 🚀 Самый быстрый VLESS ключ России
random - 🎲 5 случайных VLESS ключей России
status - 📊 Статус ключей
```

## 🖥️ Запуск на сервере

### Вариант 1: Прямой запуск

```bash
# Клонируйте репозиторий
git clone https://github.com/IvanovTony/vpn-checker-script.git
cd vpn-checker-script

# Установите зависимости
pip3 install -r requirements.txt

# Создайте .env файл
cp .env.example .env
nano .env  # Вставьте ваш TELEGRAM_BOT_TOKEN

# Запустите бота
python3 run_bot.py
```

### Вариант 2: Docker (рекомендуется)

Создайте `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "run_bot.py"]
```

Создайте `docker-compose.yml`:
```yaml
version: '3.8'

services:
  vpn-bot:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./checked:/app/checked
```

Запуск:
```bash
docker-compose up -d
```

### Вариант 3: Systemd Service

Создайте сервис файл:
```bash
sudo nano /etc/systemd/system/vpn-bot.service
```

Вставьте содержимое:
```ini
[Unit]
Description=VPN Checker Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/vpn-checker-script
ExecStart=/usr/bin/python3 /path/to/vpn-checker-script/run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Включите и запустите:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vpn-bot
sudo systemctl start vpn-bot
```

## 🔄 GitHub Actions

### Автоматическая проверка ключей

Workflow `checker.yml` запускается каждые 4 часа и:
1. Проверяет VPN ключи
2. Обновляет файлы в папке `checked/`
3. Коммитит изменения в репозиторий

### Развертывание бота

Workflow `deploy-bot.yml` запускается при изменении файлов бота и:
1. Тестирует конфигурацию бота
2. Проверяет токен
3. Показывает инструкции по развертыванию

## 📱 Доступные команды

- `/start` - Приветствие
- `/help` - Помощь
- `/ru` - Ключи для России
- `/all` - Все ключи
- `/vless` - Топ-50 VLESS ключей России
- `/fast` - Самый быстрый VLESS ключ России
- `/random` - 5 случайных VLESS ключей России
- `/status` - Статус ключей

## 🛠️ Отладка

### Проверка логов

```bash
# Для прямого запуска
python3 run_bot.py

# Для Docker
docker-compose logs -f vpn-bot

# Для Systemd
sudo journalctl -u vpn-bot -f
```

### Распространенные проблемы

1. **Бот не отвечает**
   - Проверьте токен в `.env`
   - Убедитесь что бот запущен
   - Проверьте логи на ошибки

2. **Нет ключей**
   - Проверьте папку `checked/`
   - Запустите проверку ключей: `python3 main.py`
   - Убедитесь что файлы ключей существуют

3. **Ошибки GitHub Actions**
   - Проверьте `TELEGRAM_BOT_TOKEN` в Secrets
   - Убедитесь что токен правильный
   - Проверьте логи workflow

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи
2. Убедитесь что все файлы на месте
3. Проверьте токен и права доступа
4. Создайте Issue в репозитории
