#!/usr/bin/env python3
"""
Основной скрипт для работы в Replit
Запускает Telegram бота и автообновление ключей одновременно
"""

import os
import threading
import time
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def run_bot():
    """Запуск Telegram бота"""
    try:
        from telegram_bot import VPNBot
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            print("❌ TELEGRAM_BOT_TOKEN не найден!")
            print("Пожалуйста, добавьте токен в .env файл или в Secrets Replit")
            return
        
        print("🤖 Starting Telegram Bot...")
        bot = VPNBot(token)
        bot.run()
    except Exception as e:
        print(f"❌ Bot error: {e}")

def run_auto_update():
    """Запуск автообновления ключей"""
    try:
        import schedule
        
        def update_keys():
            print(f"🚀 Starting key update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            try:
                os.system("python main.py")
                print(f"✅ Key update completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception as e:
                print(f"❌ Error updating keys: {e}")
        
        print("⏰ Auto-update service started")
        print("🔄 Keys will be updated every 4 hours")
        
        # Планируем обновления каждые 4 часа
        schedule.every(4).hours.do(update_keys)
        
        # Запускаем первое обновление через 5 минут
        print("⏳ First update in 5 minutes...")
        time.sleep(300)
        update_keys()
        
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except Exception as e:
        print(f"❌ Auto-update error: {e}")

def main():
    """Главная функция"""
    print("🚀 VPN Checker Bot starting in Replit")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Проверяем наличие токена
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ ОШИБКА: TELEGRAM_BOT_TOKEN не найден!")
        print("\n📝 Как добавить токен в Replit:")
        print("1. Нажмите на иконку 'Secrets' (🔑) слева")
        print("2. Добавьте новый секрет:")
        print("   - Key: TELEGRAM_BOT_TOKEN")
        print("   - Value: ваш_токен_от_BotFather")
        print("3. Перезапустите Replit")
        return
    
    # Создаем потоки для одновременной работы
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    update_thread = threading.Thread(target=run_auto_update, daemon=True)
    
    print("🤖 Starting Telegram Bot...")
    bot_thread.start()
    
    print("⏰ Starting Auto-update service...")
    update_thread.start()
    
    print("✅ All services started!")
    print("🔄 Bot is running and keys will auto-update every 4 hours")
    print("=" * 50)
    
    # Основной цикл
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 VPN Checker Bot stopped")

if __name__ == "__main__":
    main()
