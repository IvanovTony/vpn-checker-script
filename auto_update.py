#!/usr/bin/env python3
"""
Автоматическое обновление VPN ключей для работы в Replit
Запускается периодически для обновления ключей
"""

import os
import time
import schedule
from datetime import datetime
from main import *

def update_keys():
    """Обновить VPN ключи"""
    print(f"🚀 Starting key update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Запускаем основной скрипт проверки
        os.system("python main.py")
        
        print(f"✅ Key update completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    except Exception as e:
        print(f"❌ Error updating keys: {e}")
        return False

def main():
    """Главная функция автообновления"""
    print("🤖 Auto-update service started for Replit")
    print("⏰ Keys will be updated every 4 hours")
    print("🔄 First update starting now...")
    
    # Первое обновление сразу
    update_keys()
    
    # Планируем обновления каждые 4 часа
    schedule.every(4).hours.do(update_keys)
    
    print("⏰ Next updates scheduled every 4 hours")
    print("🔄 Press Ctrl+C to stop")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем каждую минуту

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Auto-update service stopped")
