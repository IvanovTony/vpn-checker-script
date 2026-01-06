# 🔐 Настройка Secrets в GitHub

Эта инструкция покажет как правильно засекретить `TELEGRAM_BOT_TOKEN` и `CHAT_ID` для безопасной работы бота.

## 📋 Что нужно засекретить

### 1. TELEGRAM_BOT_TOKEN
- **Назначение**: Токен для управления Telegram ботом
- **Где взять**: @BotFather в Telegram
- **Риск**: У кого есть токен - может управлять ботом

### 2. CHAT_ID (опционально)
- **Назначение**: ID чата для уведомлений
- **Где взять**: @userinfobot в Telegram
- **Риск**: Могут отправлять спам в ваш чат

## 🛡️ Пошаговая инструкция

### Шаг 1: Получение TELEGRAM_BOT_TOKEN

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду: `/newbot`
3. Ответьте на вопросы:
   - Имя бота: `VPN Checker Script`
   - Юзернейм: `vpn_checker_script_bot` (или уникальный)
4. Сохраните полученный токен (пример: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Шаг 2: Получение CHAT_ID (если нужно)

1. Откройте Telegram и найдите **@userinfobot**
2. Отправьте ему любое сообщение
3. В ответ получите свой ID (пример: `123456789`)

### Шаг 3: Настройка Secrets в GitHub

1. Откройте репозиторий: https://github.com/IvanovTony/vpn-checker-script
2. Перейдите: **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**

#### Для TELEGRAM_BOT_TOKEN:
- **Name**: `TELEGRAM_BOT_TOKEN`
- **Value**: `ваш_токен_от_BotFather`
- Нажмите **Add secret**

#### Для CHAT_ID (если нужно):
- **Name**: `CHAT_ID`
- **Value**: `ваш_chat_id`
- Нажмите **Add secret**

## ✅ Проверка настроек

### В GitHub Actions
После добавления секретов, workflow будут иметь доступ к ним:
```yaml
env:
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  CHAT_ID: ${{ secrets.CHAT_ID }}
```

### В локальной разработке
Создайте файл `.env` (не добавляйте в Git!):
```env
TELEGRAM_BOT_TOKEN=ваш_токен_для_тестов
CHAT_ID=ваш_chat_id
```

## 🔄 Использование в коде

### Python код
```python
import os
from dotenv import load_dotenv

# Загрузка .env для локальной разработки
load_dotenv()

# Работает и локально, и в GitHub Actions
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

if not TELEGRAM_BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN не найден")
    exit(1)

print("✅ Секреты загружены успешно")
```

### GitHub Actions
```yaml
- name: Send Telegram Message
  env:
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    CHAT_ID: ${{ secrets.CHAT_ID }}
  run: |
    curl -X POST \
      "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d "chat_id=${CHAT_ID}" \
      -d "text=✅ Бот успешно развернут!"
```

## 🛡️ Правила безопасности

### ✅ Что делать:
- Используйте разные токены для разработки и продакшена
- Регулярно обновляйте токены (раз в месяц)
- Ограничьте доступ к репозиторию
- Используйте двухфакторную аутентификацию в GitHub

### ❌ Чего нельзя делать:
- Никогда не пишите токены в коде
- Не добавляйте .env файл в Git
- Не передавайте токены в открытом виде
- Не используйте один токен для нескольких проектов

## 🔍 Проверка работы

После настройки секретов:

1. **Запустите GitHub Actions**:
   - Перейдите в Actions → Deploy Telegram Bot
   - Нажмите "Run workflow"

2. **Проверьте логи**:
   - Должно быть "✅ Токен найден"
   - Ошибки "TELEGRAM_BOT_TOKEN не найден" быть не должно

3. **Протестируйте бота**:
   - Найдите бота в Telegram
   - Отправьте `/start`
   - Проверьте ответ

## 🚞 Проблемы и решения

### ❌ "TELEGRAM_BOT_TOKEN не найден"
**Решение**:
- Проверьте название секрета (должно быть точно `TELEGRAM_BOT_TOKEN`)
- Убедитесь что secret добавлен в правильный репозиторий
- Проверьте права доступа к Actions

### ❌ "Invalid token"
**Решение**:
- Проверьте правильность токена
- Получите новый токен у @BotFather
- Убедитесь что токен скопирован полностью

### ❌ "Bot was blocked by user"
**Решение**:
- Найдите бота в Telegram
- Отправьте `/start`
- Разблокируйте если нужно

## 📞 Поддержка

Если возникли проблемы с секретами:
1. Проверьте эту инструкцию еще раз
2. Убедитесь что все шаги выполнены правильно
3. Создайте Issue в репозитории с деталями ошибки

---

**🎉 Готово! Теперь ваш бот безопасно работает с зашифрованными секретами!**
