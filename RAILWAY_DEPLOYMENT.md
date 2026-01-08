# 🚀 Развертывание VPN бота на Railway.app

## 📋 **Готовность проекта к Railway**

✅ **Все необходимые файлы созданы:**
- `railway.toml` - Конфигурация Railway
- `Procfile` - Команда запуска
- `runtime.txt` - Версия Python
- `webhook_bot.py` - Webhook бот для 24/7 работы
- `requirements.txt` - Все зависимости включая Flask
- `.env.example` - Пример конфигурации

---

## 🚀 **Быстрое развертывание (5 минут)**

### Шаг 1: Создание аккаунта Railway
1. Перейдите на [Railway.app](https://railway.app)
2. Войдите через GitHub (бесплатно)
3. Нажмите "Start New Project"

### Шаг 2: Подключение репозитория
1. Выберите "Deploy from GitHub repo"
2. Найдите репозиторий `vpn-checker-script`
3. Нажмите "Deploy"

### Шаг 3: Настройка переменных окружения
1. После развертывания перейдите в проект
2. Settings → Variables → New Variable
3. Добавьте переменные:

```
TELEGRAM_BOT_TOKEN=your_bot_token_from_BotFather
PORT=8080
WEBHOOK_URL=https://your-app-name.railway.app/webhook
```

### Шаг 4: Получение токена бота
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте: `/newbot`
3. Введите имя: `VPN Checker Bot`
4. Введите username: `vpn_checker_script_bot`
5. Скопируйте полученный токен

---

## 🔧 **Автоматическая настройка webhook**

Railway автоматически определит URL вашего приложения:

1. Перейдите в Settings → Domains
2. Скопируйте ваш Railway URL
3. Установите `WEBHOOK_URL`:
   ```
   WEBHOOK_URL=https://your-app-name.railway.app/webhook
   ```

---

## 🤖 **Запуск бота**

### Автоматический запуск:
- Railway автоматически запустит `webhook_bot.py`
- Бот определит Railway окружение
- Настроит webhook автоматически
- Начнет работу на порту 8080

### Проверка работы:
```bash
# Health check
curl https://your-app-name.railway.app/health

# Индекс
curl https://your-app-name.railway.app/
```

---

## 📱 **Команды бота (24/7 доступны)**

- `/start` - Приветствие
- `/help` - Помощь
- `/ru` - Ключи для России
- `/all` - Все ключи
- `/vless` - Топ-50 VLESS ключей России
- `/fast` - Самый быстрый VLESS ключ России
- `/random` - 5 случайных VLESS ключей России
- `/status` - Статус ключей

---

## ✅ **Преимущества Railway**

| Преимущество | Описание |
|---------------|-------------|
| 🆓 **БЕСПЛАТНО** | $0/месяц |
| ⏰ **24/7 uptime** | Бот работает постоянно |
| 🔒 **HTTPS** | Автоматический SSL сертификат |
| 🔄 **GitHub** | Автоматические обновления |
| 📊 **Monitoring** | Health checks и логи |
| 🚀 **Быстрый старт** | 2-3 минуты до работы |
| 🌍 **Global** | Доступен worldwide |

---

## 🛠️ **Мониторинг и управление**

### Railway Dashboard:
- **Logs:** Просмотр логов бота
- **Metrics:** Статистика использования
- **Settings:** Управление переменными
- **Deployments:** История развертываний

### Команды управления:
```bash
# Перезапустить сервис
railway restart

# Посмотреть логи
railway logs

# Обновить код
git push origin main  # автоматический redeploy
```

---

## 🚨 **Устранение проблем**

### Проблема: Бот не запускается
1. Проверьте `TELEGRAM_BOT_TOKEN` в переменных
2. Убедитесь что `PORT=8080`
3. Посмотрите логи в Railway Dashboard

### Проблема: Webhook не работает
1. Проверьте `WEBHOOK_URL` формат
2. Убедитесь что URL доступен извне
3. Перезапустите сервис: `railway restart`

### Проблема: Ошибки в логах
1. Проверьте версию Python в `runtime.txt`
2. Убедитесь что все зависимости в `requirements.txt`
3. Проверьте код на синтаксические ошибки

---

## 📊 **Статусы развертывания**

### ✅ **Успешное развертывание:**
```
🚀 Starting bot in webhook mode for Railway...
🌐 Port: 8080
🔗 Webhook URL: https://your-app.railway.app/webhook
🤖 Webhook bot is ready!
```

### 📱 **Тестирование бота:**
1. Найдите ваш бот в Telegram
2. Отправьте `/start`
3. Проверьте команды: `/help`, `/status`, `/ru`

---

## 🎯 **Результат**

**🎉 Поздравляем! Ваш VPN Checker Bot работает 24/7 на Railway!**

### Что получено:
- ✅ **Бот работает постоянно** - 24/7 uptime
- ✅ **Все команды доступны** - мгновенный ответ
- ✅ **Автоматическое обновление** - при push в main
- ✅ **Мониторинг** - health checks и логи
- ✅ **БЕСПЛАТНО** - $0/месяц
- ✅ **Масштабирование** - можно добавить больше ботов

### Дальнейшие шаги:
1. **Пользуйтесь ботом** - все команды доступны 24/7
2. **Следите за логами** - Railway Dashboard
3. **Обновляйте код** - автоматические деплои
4. **Наслаждайтесь** - ваш VPN бот всегда онлайн!

---

## 🔗 **Полезные ссылки**

- [Railway Dashboard](https://railway.app/dashboard)
- [Railway Documentation](https://docs.railway.app)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Telegram Bot](https://python-telegram-bot.org)

**🚀 Ваш бот готов к работе на Railway.app!**
