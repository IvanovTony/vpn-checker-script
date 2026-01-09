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
        # Устанавливаем timeout для предотвращения зависаний
        while True:
            try:
                bot.application.run_polling(
                    drop_pending_updates=True,
                    timeout=30  # 30 секунд timeout
                )
            except Exception as e:
                print(f"❌ Bot polling error: {e}")
                print("🔄 Перезапуск бота через 10 секунд...")
                time.sleep(10)
                continue
    except Exception as e:
        print(f"❌ Bot error: {e}")
        # Пытаемся перезапустить бота через 30 секунд
        print("🔄 Перезапуск бота через 30 секунд...")
        time.sleep(30)
        run_bot()  # Рекурсивный перезапуск

def run_auto_update():
    """Запуск автообновления ключей"""
    while True:  # Бесконечный цикл для перезапуска при ошибках
        try:
            import schedule
            
            def update_keys():
                print(f"🚀 Starting key update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                try:
                    result = os.system("python main.py")
                    if result == 0:
                        print(f"✅ Key update completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        print(f"⚠️ Key update completed with warnings at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
            
            # Основной цикл планировщика
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(60)
                except Exception as e:
                    print(f"⚠️ Schedule error: {e}")
                    time.sleep(60)  # Продолжаем работать даже с ошибками
                    
        except Exception as e:
            print(f"❌ Auto-update service crashed: {e}")
            print("🔄 Restarting auto-update service in 30 seconds...")
            time.sleep(30)
            # Продолжаем внешний цикл для перезапуска

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
