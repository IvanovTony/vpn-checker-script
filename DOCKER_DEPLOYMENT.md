# 🐳 Развертывание VPN Bot на удаленном сервере через Docker

## 🎯 Цель:

Запустить бота на удаленном сервере (VPS) через Docker для постоянной работы 24/7.

## 🏗️ Архитектура решения:

```
┌─────────────────────────────────────────────────┐
│           VPS/Удаленный сервер          │
│  ┌─────────────────────────────────┐    │
│  │        Docker Container        │    │
│  │  ┌─────────────────────┐  │    │
│  │  │   VPN Bot       │  │    │
│  │  │ (run_bot.py)     │  │    │
│  │  └─────────────────────┘  │    │
│  │  Auto-restart script       │    │
│  └─────────────────────────┘    │
│  │  Мониторинг          │    │
│  │  Логи               │    │
│  └─────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## 🚀 Пошаговая инструкция:

### Шаг 1: Подготовка сервера

#### Вариант А: Аренда VPS (рекомендуется)
```bash
# Подключитесь к серверу по SSH
ssh root@your_server_ip

# Обновите систему
apt update && apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установите Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверьте установку
docker --version
docker-compose --version
```

#### Вариант Б: Использование существующего сервера
```bash
# Проверьте что Docker установлен
docker --version

# Если нет - установите
apt install docker.io docker-compose -y
```

### Шаг 2: Клонирование репозитория

```bash
# Создайте директорию для проекта
mkdir -p /opt/vpn-bot
cd /opt/vpn-bot

# Клонируйте репозиторий
git clone https://github.com/IvanovTony/vpn-checker-script.git .

# Или используйте вашу fork
git clone https://github.com/your_username/vpn-checker-script.git .
```

### Шаг 3: Настройка переменных окружения

```bash
# Создайте .env файл из шаблона
cp .env.example .env

# Отредактируйте .env файл
nano .env
```

Содержимое `.env`:
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFghijklmnopqrstuvwxyz
CHAT_ID=123456789
ADMIN_USERNAME=admin
KEYS_DIR=./checked
HISTORY_DIR=./checked
HISTORY_FILE=history.json
BATCH_LIMIT=10
KEY_CHECK_DELAY=1
BATCH_INTERVAL=300
```

### Шаг 4: Запуск через Docker Compose

```bash
# Запустите бота в фоне
docker-compose up -d

# Проверьте статус
docker-compose ps

# Посмотрите логи
docker-compose logs -f vpn-bot
```

### Шаг 5: Проверка работы

```bash
# Проверьте что контейнер работает
docker ps | grep vpn-checker-bot

# Проверьте логи на ошибки
docker-compose logs vpn-bot | tail -20

# Проверьте что бот отвечает в Telegram
# Отправьте команду /start
```

## 🔧 Управление сервисом

### Основные команды:

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart vpn-bot

# Просмотр логов
docker-compose logs -f vpn-bot

# Вход в контейнер
docker-compose exec vpn-bot bash

# Обновление кода
git pull origin main
docker-compose up -d --build
```

### Мониторинг:

```bash
# Статус контейнера
docker-compose ps

# Использование ресурсов
docker stats vpn-checker-bot

# Свободное место
df -h

# Загрузка CPU
top -p $(docker-compose exec -T vpn-bot pgrep python)
```

## 📊 Структура файлов на сервере:

```
/opt/vpn-bot/
├── .env                    # Конфигурация (секреты)
├── .git/                   # Git репозиторий
├── checked/                 # Файлы с ключами
│   ├── RU_Best/
│   └── My_Euro/
├── logs/                    # Логи бота
│   ├── app.log
│   └── error.log
├── docker-compose.yml        # Docker конфигурация
├── Dockerfile              # Docker образ
└── *.py                    # Код бота
```

## 🔄 Автоматизация развертывания:

### Создайте скрипт развертывания:

```bash
# Создайте файл deploy.sh
nano deploy.sh
```

Содержимое `deploy.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 Начинаю развертывание VPN Bot..."

# Переход в директорию проекта
cd /opt/vpn-bot

# Получение обновлений
echo "📥 Получение обновлений..."
git pull origin main

# Остановка старого контейнера
echo "🛑 Остановка старого контейнера..."
docker-compose down

# Сборка и запуск нового образа
echo "🔨 Сборка нового образа..."
docker-compose build

echo "🚀 Запуск нового контейнера..."
docker-compose up -d

echo "✅ Развертывание завершено!"

# Проверка статуса
sleep 10
if docker-compose ps | grep -q "Up"; then
    echo "✅ Контейнер работает!"
    docker-compose ps
else
    echo "❌ Ошибка запуска контейнера!"
    docker-compose logs vpn-bot
    exit 1
fi
```

Сделайте скрипт исполняемым:
```bash
chmod +x deploy.sh
```

### Настройте cron для автоматических обновлений:

```bash
# Откройте crontab
crontab -e

# Добавьте строку для ежедневного обновления в 3:00
0 3 * * * /opt/vpn-bot/deploy.sh >> /var/log/vpn-bot-deploy.log 2>&1
```

## 🔒 Безопасность

### Защита .env файла:

```bash
# Установите правильные права
chmod 600 .env
chown root:root .env

# Проверьте что .env в .gitignore
cat .gitignore | grep .env
```

### Firewall настройки:

```bash
# Откройте только необходимые порты (если нужен nginx)
ufw allow 22/tcp    # SSH
ufw allow 8080/tcp   # Мониторинг (опционально)
ufw enable
```

### SSH ключи:

```bash
# Сгенерируйте SSH ключи
ssh-keygen -t rsa -b 4096 -C "vpn-bot@server"

# Добавьте публичный ключ на сервер
ssh-copy-id root@your_server_ip
```

## 📈 Мониторинг и алерты

### Настройка логирования:

```bash
# Создайте директорию для логов
mkdir -p /var/log/vpn-bot

# Настройте ротацию логов
echo "0 0 * * * /usr/sbin/logrotate /etc/logrotate.d/vpn-bot" | crontab -
```

### Мониторинг состояния:

```bash
# Создайте health check скрипт
cat > /opt/vpn-bot/health_check.sh << 'EOF'
#!/bin/bash
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ VPN Bot контейнер не работает!"
    # Отправьте алерт (опционально)
    curl -X POST "https://api.telegram.org/bot\$TELEGRAM_BOT_TOKEN/sendMessage" \
         -d "chat_id=\$CHAT_ID&text=🚨 Бот упал! Перезапускаю..."
    /opt/vpn-bot/deploy.sh
fi
EOF

chmod +x /opt/vpn-bot/health_check.sh

# Добавьте в cron для проверки каждые 5 минут
echo "*/5 * * * * /opt/vpn-bot/health_check.sh" | crontab -
```

## 🚨 Устранение проблем

### Проблема: Контейнер не запускается

```bash
# Проверьте логи
docker-compose logs vpn-bot

# Проверьте .env файл
cat .env

# Проверьте права на файлы
ls -la checked/

# Пересоберите образ
docker-compose build --no-cache
docker-compose up -d
```

### Проблема: Бот не отвечает в Telegram

```bash
# Проверьте токен
curl -s https://api.telegram.org/bot\$TELEGRAM_BOT_TOKEN/getMe

# Проверьте логи на ошибки
docker-compose logs vpn-bot | grep ERROR

# Перезапустите контейнер
docker-compose restart vpn-bot
```

### Проблема: Нет доступа к файлам с ключами

```bash
# Проверьте структуру папок
ls -la checked/

# Создайте недостающие папки
mkdir -p checked/RU_Best checked/My_Euro

# Установите правильные права
chown -R 1000:1000 checked/
chmod -R 755 checked/
```

## 💰 Стоимость решения

### VPS провайдеры:
- **DigitalOcean:** $5/месяц (1GB RAM, 25GB SSD)
- **Vultr:** $3.5/месяц (512MB RAM, 10GB SSD)
- **Hetzner:** €3.49/месяц (2GB RAM, 20GB SSD)

### Расходы:
- **VPS:** $3-6/месяц
- **Домен (опционально):** $10/год
- **SSL (опционально):** бесплатно (Let's Encrypt)
- **Итого:** $36-72/год

## ✅ Проверка работоспособности

### Тестовый чек-лист:

- [ ] Контейнер запускается без ошибок
- [ ] Бот отвечает на команду /start
- [ ] Бот отвечает на команду /status
- [ ] Бот отправляет ключи по /ru
- [ ] Логи пишутся в logs/
- [ ] Автоперезапуск работает
- [ ] Мониторинг работает
- [ ] Обновления через git pull работают

### Команды для проверки:

```bash
# Полная проверка статуса
docker-compose ps && echo "---" && docker-compose logs --tail=20 vpn-bot

# Тест команд бота
docker-compose exec vpn-bot python -c "
import telegram
from telegram_bot import VPNBot
bot = VPNBot('\$TELEGRAM_BOT_TOKEN')
print('✅ Bot initialization successful')
"
```

---

## 🎉 Итог

**После выполнения этой инструкции у вас будет:**
- ✅ **Постоянно работающий бот** 24/7
- ✅ **Автоматические обновления** кода
- ✅ **Мониторинг состояния** и алерты
- ✅ **Резервное копирование** логов
- ✅ **Безопасное хранение** секретов
- ✅ **Масштабируемое решение**

**Ваш VPN бот будет работать надежно на удаленном сервере!** 🚀
