#!/usr/bin/env python3
"""
Скрипт для отправки webhook и запуска бота по запросу
"""

import requests
import os
import sys
from datetime import datetime

def send_webhook():
    """Отправляет webhook для запуска бота"""
    
    # Проверяем переменные окружения
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN не найден в переменных окружения!")
        print("Создайте Personal Access Token и добавьте в GitHub Secrets")
        return False
    
    REPO_OWNER = os.getenv('REPO_OWNER', 'IvanovTony')
    REPO_NAME = os.getenv('REPO_NAME', 'vpn-checker-script')
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    data = {
        "event_type": "run_bot_command",
        "client_payload": {
            "command": "manual_trigger",
            "timestamp": datetime.now().isoformat(),
            "trigger_source": "manual_script"
        }
    }
    
    try:
        print(f"🚀 Отправка webhook в {REPO_OWNER}/{REPO_NAME}...")
        print(f"📝 Команда: {data['client_payload']['command']}")
        print(f"⏰ Время: {data['client_payload']['timestamp']}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 204:
            print("✅ Webhook отправлен успешно!")
            print("⏱️ Бот запустится через 30-90 секунд")
            print("🔄 Бот будет работать 10 минут")
            return True
        elif response.status_code == 401:
            print("❌ Ошибка аутентификации!")
            print("🔑 Проверьте GITHUB_TOKEN в GitHub Secrets")
            print("📝 Убедитесь что token имеет права repo:workflow")
            return False
        elif response.status_code == 404:
            print("❌ Репозиторий не найден!")
            print("🔍 Проверьте REPO_OWNER и REPO_NAME")
            return False
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Таймаут подключения!")
        print("🔄 Попробуйте еще раз")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения!")
        print("🌐 Проверьте интернет соединение")
        return False
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")
        return False

def main():
    """Главная функция"""
    print("🤖 VPN Bot Webhook Trigger")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("Использование:")
            print("  python3 trigger_webhook.py           # Запуск webhook")
            print("  python3 trigger_webhook.py --help     # Эта справка")
            print("\nПеременные окружения:")
            print("  GITHUB_TOKEN - Personal Access Token")
            print("  REPO_OWNER   - Владелец репозитория (default: IvanovTony)")
            print("  REPO_NAME     - Имя репозитория (default: vpn-checker-script)")
            return
    
    success = send_webhook()
    
    if success:
        print("\n🎯 Следующие шаги:")
        print("1. ⏳ Подождите 1-2 минуты")
        print("2. 📱 Отправьте команду боту в Telegram")
        print("3. ✅ Бот ответит на вашу команду")
        print("\n📊 Статус можно посмотреть:")
        print("   GitHub Actions > Webhook Bot Runner")
    else:
        print("\n🔧 Решение проблем:")
        print("1. Проверьте GITHUB_TOKEN в Secrets")
        print("2. Убедитесь что token имеет права repo:workflow")
        print("3. Проверьте название репозитория")
        sys.exit(1)

if __name__ == "__main__":
    main()
