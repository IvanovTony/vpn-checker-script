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

# Создаем директорию для ключей, если ее нет
RUN mkdir -p checked logs

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Создаем скрипт для запуска с мониторингом
COPY <<EOF /app/start_bot.sh
#!/bin/bash
echo "🚀 Starting VPN Bot with auto-restart..."

while true; do
    echo "🤖 Starting bot at \$(date)"
    python run_bot.py &
    BOT_PID=\$!
    
    # Ждем 10 минут работы бота
    sleep 600
    
    # Проверяем если бот еще работает
    if kill -0 \$BOT_PID 2>/dev/null; then
        echo "⏹️ Terminating bot after 10 minutes..."
        kill \$BOT_PID
        sleep 5
    else
        echo "📋 Bot stopped naturally"
    fi
    
    # Пауза перед перезапуском
    echo "💤 Sleeping for 60 seconds before restart..."
    sleep 60
done
EOF

RUN chmod +x /app/start_bot.sh

# Запускаем скрипт мониторинга
CMD ["/bin/bash", "/app/start_bot.sh"]
