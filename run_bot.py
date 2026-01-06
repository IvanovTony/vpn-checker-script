#!/usr/bin/env python3
"""
Simple startup script for VPN Checker Telegram Bot
"""

import os
import sys
from telegram_bot import main

if __name__ == "__main__":
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Ошибка: файл .env не найден!")
        print("\nСоздайте файл .env со следующим содержимым:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here\n")
        print("\nИли скопируйте шаблон:")
        print("cp .env.example .env\n")
        sys.exit(1)
    
    # Load and check token
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token or token == 'your_bot_token_here':
        print("❌ Ошибка: укажите реальный токен в файле .env!")
        print("Получите токен у @BotFather в Telegram")
        sys.exit(1)
    
    print("🚀 Запуск VPN Checker Telegram Bot...")
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
