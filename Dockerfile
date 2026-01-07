FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Создаем директорию для ключей
RUN mkdir -p checked

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Создаем скрипт для запуска с автоперезапуском
COPY <<EOF /app/start_bot.sh
#!/bin/bash

echo "🚀 Starting VPN Bot with auto-restart..."

while true; do
    echo "🤖 Starting bot at \$(date '+%Y-%m-%d %H:%M:%S')"
    
    # Запускаем бота в фоновом режиме
    python run_bot.py &
    BOT_PID=\$!
    
    # Ждем 1 час работы бота
    sleep 3600
    
    # Проверяем если бот еще работает
    if kill -0 \$BOT_PID 2>/dev/null; then
        echo "⏹️ Restarting bot after 1 hour for stability..."
        kill \$BOT_PID 2>/dev/null
        sleep 5
    else
        echo "📋 Bot stopped, checking for errors..."
        # Проверяем логи ошибок если нужно
        sleep 10
    fi
    
    # Короткая пауза перед перезапуском
    echo "💤 Waiting 30 seconds before restart..."
    sleep 30
done
EOF

RUN chmod +x /app/start_bot.sh

# Запускаем скрипт с автоперезапуском
CMD ["/bin/bash", "/app/start_bot.sh"]
