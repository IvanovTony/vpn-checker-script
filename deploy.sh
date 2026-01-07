#!/bin/bash
set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Начинаю развертывание VPN Bot...${NC}"

# Проверяем аргументы
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo -e "${GREEN}Использование:${NC}"
    echo "  ./deploy.sh              # Полное развертывание"
    echo "  ./deploy.sh --update      # Только обновление кода"
    echo "  ./deploy.sh --restart     # Только перезапуск"
    echo "  ./deploy.sh --logs        # Просмотр логов"
    echo "  ./deploy.sh --status      # Проверка статуса"
    exit 0
fi

# Переход в директорию проекта
PROJECT_DIR="/opt/vpn-bot"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Директория $PROJECT_DIR не найдена!${NC}"
    echo "Сначала выполните первичную установку:"
    echo "  sudo mkdir -p $PROJECT_DIR"
    echo "  sudo cd $PROJECT_DIR"
    echo "  sudo git clone https://github.com/IvanovTony/vpn-checker-script.git ."
    exit 1
fi

cd "$PROJECT_DIR"

# Функции
update_code() {
    echo -e "${BLUE}📥 Получение обновлений...${NC}"
    git pull origin main
    echo -e "${GREEN}✅ Код обновлен${NC}"
}

stop_container() {
    echo -e "${YELLOW}🛑 Остановка контейнера...${NC}"
    docker-compose down 2>/dev/null || true
    echo -e "${GREEN}✅ Контейнер остановлен${NC}"
}

build_image() {
    echo -e "${BLUE}🔨 Сборка образа...${NC}"
    docker-compose build --no-cache
    echo -e "${GREEN}✅ Образ собран${NC}"
}

start_container() {
    echo -e "${BLUE}🚀 Запуск контейнера...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ Контейнер запущен${NC}"
}

check_status() {
    echo -e "${BLUE}📊 Проверка статуса...${NC}"
    
    if docker-compose ps | grep -q "Up"; then
        echo -e "${GREEN}✅ Контейнер работает!${NC}"
        docker-compose ps
        echo ""
        echo -e "${BLUE}📋 Последние логи:${NC}"
        docker-compose logs --tail=10 vpn-bot
    else
        echo -e "${RED}❌ Контейнер не работает!${NC}"
        echo ""
        echo -e "${YELLOW}📋 Последние логи:${NC}"
        docker-compose logs --tail=20 vpn-bot
        return 1
    fi
}

show_logs() {
    echo -e "${BLUE}📋 Просмотр логов (Ctrl+C для выхода):${NC}"
    docker-compose logs -f vpn-bot
}

# Основная логика
case "$1" in
    --update)
        update_code
        ;;
    --restart)
        stop_container
        start_container
        ;;
    --logs)
        show_logs
        ;;
    --status)
        check_status
        ;;
    "")
        # Полное развертывание
        update_code
        stop_container
        build_image
        start_container
        
        echo ""
        echo -e "${GREEN}🎉 Развертывание завершено!${NC}"
        echo -e "${BLUE}⏱️ Ожидаю 10 секунд для проверки...${NC}"
        
        sleep 10
        
        # Проверяем статус
        if check_status; then
            echo ""
            echo -e "${GREEN}✅ Бот готов к работе!${NC}"
            echo -e "${YELLOW}💡 Команды управления:${NC}"
            echo "  ./deploy.sh --status    # Проверка статуса"
            echo "  ./deploy.sh --restart   # Перезапуск"
            echo "  ./deploy.sh --logs      # Просмотр логов"
            echo "  ./deploy.sh --update    # Обновление кода"
        else
            echo -e "${RED}❌ Проверьте логи выше для устранения проблем${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}❌ Неизвестная опция: $1${NC}"
        echo "Используйте ./deploy.sh --help для помощи"
        exit 1
        ;;
esac
