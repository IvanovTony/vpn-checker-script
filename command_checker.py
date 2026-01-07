#!/usr/bin/env python3
"""
Система проверки очереди команд Telegram
Запускает бота при появлении новых команд
"""

import os
import requests
import time
import logging
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramCommandChecker:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_owner = os.getenv('REPO_OWNER', 'IvanovTony')
        self.repo_name = os.getenv('REPO_NAME', 'vpn-checker-script')
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN не найден!")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN не найден!")
    
    def get_bot_info(self):
        """Получает информацию о боте"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json().get('result')
            return None
        except Exception as e:
            logger.error(f"Ошибка получения info: {e}")
            return None
    
    def get_updates(self, offset=None, limit=1):
        """Получает последние обновления"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            params = {
                'limit': limit,
                'timeout': 5
            }
            if offset:
                params['offset'] = offset
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get('result', [])
            return []
        except Exception as e:
            logger.error(f"Ошибка получения updates: {e}")
            return []
    
    def trigger_webhook(self, reason="auto_trigger"):
        """Запускает webhook для бота"""
        try:
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/dispatches"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            
            data = {
                "event_type": "run_bot_command",
                "client_payload": {
                    "command": "auto_trigger",
                    "timestamp": datetime.now().isoformat(),
                    "trigger_source": reason
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 204:
                logger.info(f"✅ Webhook отправлен (причина: {reason})")
                return True
            else:
                logger.error(f"❌ Ошибка webhook: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка отправки webhook: {e}")
            return False
    
    def check_for_commands(self):
        """Проверяет наличие команд в очереди"""
        try:
            # Получаем последние обновления
            updates = self.get_updates(limit=10)
            
            if not updates:
                logger.info("📭 Нет новых сообщений")
                return False
            
            # Ищем команды
            commands_found = []
            for update in updates:
                message = update.get('message', {})
                if message and message.get('text'):
                    text = message['text']
                    if text.startswith('/'):
                        command = text.split()[0]
                        commands_found.append({
                            'command': command,
                            'user': message.get('from', {}).get('first_name', 'Unknown'),
                            'time': datetime.fromtimestamp(update.get('message', {}).get('date', 0))
                        })
            
            if commands_found:
                logger.info(f"📝 Найдены команды: {[c['command'] for c in commands_found]}")
                
                # Проверяем что бот не запущен
                if self.is_bot_already_running():
                    logger.info("🤖 Бот уже работает, пропускаем запуск")
                    return False
                
                # Отправляем webhook для запуска бота
                return self.trigger_webhook(f"commands_detected: {[c['command'] for c in commands_found]}")
            
            logger.info("📭 Команд не найдено")
            return False
            
        except Exception as e:
            logger.error(f"❌ Ошибка проверки команд: {e}")
            return False
    
    def is_bot_already_running(self):
        """Проверяет запущен ли уже бот"""
        try:
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers, params={"status": "in_progress"}, timeout=10)
            
            if response.status_code == 200:
                runs = response.json().get('workflow_runs', [])
                bot_runs = [run for run in runs if 'Webhook Bot Runner' in run.get('name', '')]
                
                if bot_runs:
                    # Проверяем время запуска (не старше 5 минут)
                    for run in bot_runs:
                        created_at = run.get('created_at', '')
                        if created_at:
                            run_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            if (datetime.now(timezone.utc) - run_time).total_seconds() < 300:
                                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Ошибка проверки запущенных ботов: {e}")
            return False
    
    def run_checker(self, check_interval=60):
        """Запускает постоянную проверку"""
        logger.info("🚀 Запуск системы проверки команд...")
        
        # Проверяем информацию о боте
        bot_info = self.get_bot_info()
        if bot_info:
            logger.info(f"🤖 Бот: @{bot_info.get('username')}")
        else:
            logger.error("❌ Не удалось получить информацию о боте")
            return
        
        last_check = datetime.now()
        consecutive_empty_checks = 0
        
        try:
            while True:
                current_time = datetime.now()
                
                # Проверяем каждые check_interval секунд
                if (current_time - last_check).total_seconds() >= check_interval:
                    logger.info(f"🔍 Проверка команд в {current_time.strftime('%H:%M:%S')}")
                    
                    if self.check_for_commands():
                        consecutive_empty_checks = 0
                        # Ждем 5 минут после запуска бота
                        logger.info("⏳ Бот запущен, ждем 5 минут...")
                        time.sleep(300)  # 5 минут
                    else:
                        consecutive_empty_checks += 1
                        if consecutive_empty_checks > 0:
                            logger.info(f"📊 {consecutive_empty_checks} проверок без команд")
                    
                    last_check = current_time
                
                # Короткая пауза
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("👋 Проверка остановлена пользователем")
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}")

def main():
    """Главная функция"""
    try:
        checker = TelegramCommandChecker()
        
        print("🤖 Telegram Command Checker")
        print("=" * 40)
        print("🔍 Проверка очереди команд Telegram")
        print("🚀 Автоматический запуск бота")
        print("⏰ Проверка каждые 60 секунд")
        print("=" * 40)
        
        # Запускаем проверку
        checker.run_checker(check_interval=60)
        
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}")
        print("🔧 Убедитесь что все переменные окружения установлены:")
        print("  - TELEGRAM_BOT_TOKEN")
        print("  - GITHUB_TOKEN")
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")

if __name__ == "__main__":
    main()
