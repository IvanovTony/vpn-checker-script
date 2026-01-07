#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="/opt/vpn-bot"
LOG_FILE="/var/log/vpn-bot-health.log"
TELEGRAM_BOT_TOKEN=""
CHAT_ID=""

# Загружаем переменные окружения
if [ -f "$PROJECT_DIR/.env" ]; then
    source "$PROJECT_DIR/.env"
    TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
    CHAT_ID=$CHAT_ID
fi

# Функция логирования
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
    echo -e "$1"
}

# Функция отправки алерта в Telegram
send_telegram_alert() {
    local message="$1"
    
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
        local escaped_message=$(echo "$message" | sed 's/[_*[\]()~`>#+-=|{}.!]/\\&/g')
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
             -d "chat_id=$CHAT_ID" \
             -d "text=$escaped_message" \
             -d "parse_mode=MarkdownV2" > /dev/null 2>&1
    fi
}

# Проверка Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_message "${RED}❌ Docker не установлен!${NC}"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        log_message "${RED}❌ Docker daemon не работает!${NC}"
        return 1
    fi
    
    return 0
}

# Проверка контейнера
check_container() {
    cd "$PROJECT_DIR"
    
    # Проверяем что контейнер существует
    if ! docker-compose ps | grep -q "vpn-checker-bot"; then
        log_message "${YELLOW}⚠️ Контейнер не найден, запускаю...${NC}"
        docker-compose up -d
        sleep 10
        return 1
    fi
    
    # Проверяем что контейнер запущен
    if ! docker-compose ps | grep -q "Up"; then
        log_message "${YELLOW}⚠️ Контейнер не запущен, запускаю...${NC}"
        docker-compose up -d
        sleep 10
        
        # Повторная проверка
        if ! docker-compose ps | grep -q "Up"; then
            log_message "${RED}❌ Не удалось запустить контейнер!${NC}"
            return 1
        fi
    fi
    
    return 0
}

# Проверка здоровья бота
check_bot_health() {
    cd "$PROJECT_DIR"
    
    # Проверяем что бот отвечает на команды
    local bot_response=$(docker-compose exec -T vpn-bot python -c "
import os
import sys
sys.path.append('/app')
try:
    from telegram_bot import VPNBot
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token:
        bot = VPNBot(token)
        print('OK')
    else:
        print('NO_TOKEN')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null || echo "EXEC_ERROR")
    
    if [ "$bot_response" == "OK" ]; then
        return 0
    elif [ "$bot_response" == "NO_TOKEN" ]; then
        log_message "${RED}❌ TELEGRAM_BOT_TOKEN не настроен!${NC}"
        return 1
    else
        log_message "${RED}❌ Ошибка инициализации бота: $bot_response${NC}"
        return 1
    fi
}

# Проверка доступа к файлам
check_files() {
    cd "$PROJECT_DIR"
    
    # Проверяем что .env файл существует и доступен
    if [ ! -f ".env" ]; then
        log_message "${RED}❌ Файл .env не найден!${NC}"
        return 1
    fi
    
    # Проверяем что директория с ключами существует
    if [ ! -d "checked" ]; then
        log_message "${YELLOW}⚠️ Директория checked не найдена, создаю...${NC}"
        mkdir -p checked/{RU_Best,My_Euro}
    fi
    
    # Проверяем права доступа
    if [ ! -r "checked" ]; then
        log_message "${RED}❌ Нет доступа к директории checked!${NC}"
        return 1
    fi
    
    return 0
}

# Проверка использования ресурсов
check_resources() {
    cd "$PROJECT_DIR"
    
    # Получаем статистику контейнера
    local stats=$(docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" vpn-checker-bot 2>/dev/null || echo "")
    
    if [ -n "$stats" ]; then
        local cpu_usage=$(echo "$stats" | tail -n1 | awk '{print $2}' | sed 's/%//')
        local mem_usage=$(echo "$stats" | tail -n1 | awk '{print $3}')
        
        # Проверяем CPU > 80%
        if (( $(echo "$cpu_usage > 80" | bc -l) )); then
            log_message "${YELLOW}⚠️ Высокая загрузка CPU: ${cpu_usage}%${NC}"
        fi
        
        # Проверяем память
        if [[ "$mem_usage" == *"GiB"* ]]; then
            local mem_gib=$(echo "$mem_usage" | sed 's/GiB//' | awk '{print $1}')
            if (( $(echo "$mem_gib > 1" | bc -l) )); then
                log_message "${YELLOW}⚠️ Высокое использование памяти: ${mem_usage}${NC}"
            fi
        fi
    fi
    
    return 0
}

# Функция восстановления
fix_issues() {
    cd "$PROJECT_DIR"
    
    log_message "${BLUE}🔧 Попытка восстановления...${NC}"
    
    # Перезапускаем контейнер
    docker-compose down
    sleep 5
    docker-compose up -d
    sleep 15
    
    # Проверяем результат
    if check_container && check_bot_health; then
        log_message "${GREEN}✅ Восстановление успешно!${NC}"
        send_telegram_alert "✅ VPN Bot восстановлен и работает нормально"
        return 0
    else
        log_message "${RED}❌ Восстановление не удалось!${NC}"
        send_telegram_alert "🚨 VPN Bot не удалось восстановить! Требуется ручное вмешательство"
        return 1
    fi
}

# Основная проверка
main_health_check() {
    log_message "${BLUE}🔍 Начало health check...${NC}"
    
    local issues=0
    
    # Проверка Docker
    if ! check_docker; then
        issues=$((issues + 1))
    fi
    
    # Проверка файлов
    if ! check_files; then
        issues=$((issues + 1))
    fi
    
    # Проверка контейнера
    if ! check_container; then
        issues=$((issues + 1))
    fi
    
    # Проверка здоровья бота
    if ! check_bot_health; then
        issues=$((issues + 1))
    fi
    
    # Проверка ресурсов
    check_resources
    
    # Если есть проблемы, пробуем восстановить
    if [ $issues -gt 0 ]; then
        log_message "${YELLOW}⚠️ Обнаружено $issues проблем, начинаю восстановление...${NC}"
        
        if fix_issues; then
            log_message "${GREEN}✅ Все проблемы устранены${NC}"
        else
            log_message "${RED}❌ Проблемы не устранены${NC}"
            return 1
        fi
    else
        log_message "${GREEN}✅ Все проверки пройдены успешно${NC}"
    fi
    
    return 0
}

# Обработка аргументов
case "$1" in
    --help|-h)
        echo "Использование: $0 [опции]"
        echo "  --help, -h      Показать эту справку"
        echo "  --verbose       Подробный вывод"
        echo "  --test          Тестовый режим без восстановления"
        echo "  --logs          Показать последние логи"
        ;;
    --verbose)
        log_message "${BLUE}🔍 Подробная проверка...${NC}"
        check_docker
        check_files
        check_container
        check_bot_health
        check_resources
        ;;
    --test)
        log_message "${BLUE}🧪 Тестовый режим...${NC}"
        main_health_check
        ;;
    --logs)
        if [ -f "$LOG_FILE" ]; then
            tail -n 50 "$LOG_FILE"
        else
            echo "Лог файл не найден: $LOG_FILE"
        fi
        ;;
    "")
        main_health_check
        ;;
    *)
        echo "Неизвестная опция: $1"
        echo "Используйте --help для помощи"
        exit 1
        ;;
esac
