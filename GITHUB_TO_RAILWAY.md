# 🚀 Развертывание VPN бота: GitHub → Railway

## 📋 **Что уже готово (все файлы созданы):**

✅ **Railway файлы:**
- `railway.toml` - конфигурация Railway
- `Procfile` - команда запуска
- `runtime.txt` - Python 3.12
- `webhook_bot.py` - webhook бот для 24/7
- `requirements.txt` - все зависимости

---

## 🎯 **Развертывание из GitHub в Railway (3 шага):**

### Шаг 1: Создание Telegram бота
1. Найдите [@BotFather](https://t.me/BotFather)
2. Отправьте: `/newbot`
3. Имя: `VPN Checker Bot`
4. Username: `vpn_checker_script_bot`
5. **Скопируйте токен** - понадобится для Railway

### Шаг 2: Развертывание на Railway
1. Перейдите на [Railway.app](https://railway.app)
2. Войдите через GitHub (бесплатно)
3. Нажмите **"New Project"** → **"Deploy from GitHub repo"**
4. Найдите репозиторий `vpn-checker-script`
5. Нажмите **"Deploy"**

### Шаг 3: Настройка переменных окружения
1. После развертывания откройте проект в Railway
2. Перейдите в **Settings** → **Variables**
3. Добавьте переменные:

```
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
PORT=8080
```

4. Railway автоматически определит URL и создаст webhook
5. **Готово!** Бот работает 24/7

---

## 🔧 **Автоматическая работа:**

### Что происходит автоматически:
- ✅ Railway устанавливает зависимости из `requirements.txt`
- ✅ Запускает `webhook_bot.py` из `Procfile`
- ✅ Определяет Railway окружение
- ✅ Настраивает webhook автоматически
- ✅ Бот отвечает на команды 24/7

### Проверка работы:
- Откройте Railway Dashboard → Logs
- Найдите ваш бот в Telegram
- Отправьте `/start`

---

## 📱 **Команды бота:**

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие |
| `/help` | Помощь |
| `/ru` | Ключи для России |
| `/all` | Все ключи |
| `/vless` | Топ-50 VLESS России |
| `/fast` | Самый быстрый VLESS России |
| `/random` | 5 случайных VLESS России |
| `/status` | Статус ключей |

---

## 🔄 **Обновления:**

**Автоматические обновления при push в main:**
```bash
git add .
git commit -m "Update bot"
git push origin main
```

Railway автоматически:
- 🔍 Обнаружит изменения
- 🔄 Пересоберет проект
- 🚀 Перезапустит бота

---

## 📊 **Мониторинг:**

### Railway Dashboard:
- **Logs** - логи работы бота
- **Metrics** - статистика
- **Settings** - переменные окружения
- **Deployments** - история развертываний

### Health checks:
```bash
# Проверить статус
curl https://your-app.railway.app/health

# Домашняя страница
curl https://your-app.railway.app/
```

---

## 🚨 **Если что-то не работает:**

### Бот не отвечает:
1. Проверьте `TELEGRAM_BOT_TOKEN` в Variables
2. Посмотрите логи в Railway Dashboard
3. Перезапустите: Settings → General → Restart

### Ошибки в логах:
1. Убедитесь что все файлы в репозитории
2. Проверьте версию Python в `runtime.txt`
3. Посмотрите раздел "Deployments"

---

## 💰 **Стоимость:**

| План | Цена | Что включено |
|------|------|-------------|
| **Hobby** | **$0/месяц** | ✅ 24/7 uptime<br>✅ 750 часов/месяц<br>✅ 100MB RAM<br>✅ 1GB storage |

**🎉 Для VPN бота достаточно бесплатного плана!**

---

## 🎯 **Результат:**

**🚀 Ваш VPN Checker Bot работает 24/7 на Railway!**

### Что получено:
- ✅ **Бесплатно** - $0/месяц
- ✅ **24/7 работа** - всегда онлайн
- ✅ **Автообновления** - из GitHub
- ✅ **HTTPS** - автоматический SSL
- ✅ **Мониторинг** - логи и метрики
- ✅ **Масштабирование** - при необходимости

### Дальнейшие шаги:
1. **Пользуйтесь ботом** - все команды доступны
2. **Следите за логами** - Railway Dashboard
3. **Обновляйте код** - git push origin main
4. **Наслаждайтесь** - ваш бот всегда онлайн!

---

## 🔗 **Полезные ссылки:**

- [Railway.app](https://railway.app)
- [Railway Dashboard](https://railway.app/dashboard)
- [BotFather](https://t.me/BotFather)
- [Репозиторий](https://github.com/IvanovTony/vpn-checker-script)

**🎉 Готово! Ваш бот работает на Railway.app!**
