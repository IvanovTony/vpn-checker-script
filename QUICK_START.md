# 🚀 Быстрый запуск 24/7 VPN Бота

## 🎯 Самый простой способ (Docker)

### 1. Подготовка
```bash
# Клонируйте репозиторий
git clone https://github.com/IvanovTony/vpn-checker-script.git
cd vpn-checker-script

# Создайте .env файл с токеном
cp .env.example .env
echo "TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER" >> .env
```

### 2. Запуск 24/7 бота
```bash
# Запустите с автоматическим перезапуском
docker-compose up -d

# Проверьте статус
docker-compose logs vpn-bot
```

### 3. Проверка работы
Отправьте боту любую команду:
- `/start` - Приветствие
- `/help` - Помощь
- `/status` - Статус ключей

---

## 🔧 Альтернативный способ (VPS)

```bash
# Клонируйте и настройте
git clone https://github.com/IvanovTony/vpn-checker-script.git
cd vpn-checker-script
cp .env.example .env
echo "TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН" >> .env

# Установите и запустите
pip3 install -r requirements.txt
pm2 start run_bot.py --name vpn-bot
pm2 save
```

---

## ✅ Проверка работы

**Команды бота:**
- `/start` - ✅ Приветствие
- `/help` - ✅ Помощь
- `/ru` - ✅ Ключи для России
- `/all` - ✅ Все ключи
- `/vless` - ✅ Топ-50 VLESS России
- `/fast` - ✅ Самый быстрый VLESS России
- `/random` - ✅ 5 случайных VLESS России
- `/status` - ✅ Статус ключей

**Мониторинг:**
```bash
# Docker
docker-compose logs -f vpn-bot
docker-compose ps

# PM2
pm2 logs vpn-bot
pm2 status
```

---

## 🎉 Готово!

Ваш бот теперь работает 24/7 с:
- 🔄 Автоперезапуском каждый час
- 🏥 Health checks каждые 60 секунд
- 💾 Постоянным хранилищем ключей
- 🚀 Автовосстановлением после ошибок
- 📱 Полным набором команд

**Бот готов к круглосуточной работе!** 🚀
