#!/usr/bin/env python3
"""
Telegram Bot для Railway.app
Запускает VPN Checker Bot 24/7
"""

import os
import logging
from telegram_bot import VPNBot

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Главная функция для запуска бота на Railway"""
    
    # Получаем токен из переменных окружения
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
        logger.error("Пожалуйста, добавьте TELEGRAM_BOT_TOKEN в Railway Variables")
        return
    
    logger.info("🚀 Запуск VPN Checker Bot на Railway.app...")
    logger.info("✅ Бот будет работать 24/7")
    
    try:
        # Создаем и запускаем бота
        bot = VPNBot(bot_token)
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        # Railway автоматически перезапустит контейнер при ошибке

if __name__ == '__main__':
    main()