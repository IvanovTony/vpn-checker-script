#!/usr/bin/env python3
"""
Вебхук бот для работы с GitHub Actions
Запускается на короткое время, обрабатывает команды и завершается
"""

import os
import asyncio
import logging
import time
import threading
import requests
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import the original bot class
from telegram_bot import VPNBot

class WebhookBot(VPNBot):
    def __init__(self, token: str, max_runtime: int = 600):
        """Bot that runs for a limited time"""
        super().__init__(token)
        self.max_runtime = max_runtime  # Максимальное время работы в секундах
        self.start_time = time.time()
        self.commands_processed = 0
        self.should_stop = False
        
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop command"""
        if update.message:
            await update.message.reply_text(
                "🛑 Бот остановлен. Для перезапуска используйте /start или отправьте любую команду.",
                parse_mode='Markdown'
            )
        self.should_stop = True
        
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command with webhook info"""
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, self.max_runtime - elapsed)
        
        # Get original status
        await super().status_command(update, context)
        
        # Add webhook status
        webhook_status = (
            f"\n\n🤖 *Webhook Status:*\n"
            f"⏱️ Работает: {elapsed} сек\n"
            f"⏰ Осталось: {remaining} сек\n"
            f"📝 Команд обработано: {self.commands_processed}\n"
            f"🔄 Перезапуск через webhook"
        )
        
        if update.message:
            await update.message.reply_text(webhook_status, parse_mode='Markdown')
        
    def setup_handlers(self):
        """Setup bot command handlers"""
        super().setup_handlers()
        self.application.add_handler(CommandHandler("stop", self.stop_command))
        # Заменяем status_command на наш
        self.application.remove_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        
    async def handle_update(self, update: Update, context):
        """Handle update with tracking"""
        try:
            self.commands_processed += 1
            
            # Log command
            if update.message and update.message.text:
                command = update.message.text.split()[0]
                logger.info(f"Processing command: {command} (total: {self.commands_processed})")
            
            # Process update normally
            await self.application.process_update(update)
            
            # Check if we should stop
            elapsed = time.time() - self.start_time
            if elapsed >= self.max_runtime or self.should_stop:
                logger.info(f"Bot stopping after {elapsed} seconds")
                await self.application.stop()
                return
                
        except Exception as e:
            logger.error(f"Error handling update: {e}")
    
    def run_with_timeout(self):
        """Run bot with timeout and continuous operation"""
        logger.info(f"Starting webhook bot (max runtime: {self.max_runtime}s)")
        
        try:
            # Run the polling with timeout
            self.application.run_polling(
                drop_pending_updates=True,
                timeout=self.max_runtime,
                close_loop=True
            )
        except Exception as e:
            logger.error(f"Bot error: {e}")
        finally:
            logger.info(f"Bot stopped after {time.time() - self.start_time:.1f} seconds")

def send_webhook_trigger():
    """Send webhook to trigger bot"""
    try:
        token = os.getenv('GITHUB_TOKEN')
        repo_owner = os.getenv('REPO_OWNER', 'IvanovTony')
        repo_name = os.getenv('REPO_NAME', 'vpn-checker-script')
        
        if not token:
            logger.warning("No GITHUB_TOKEN found")
            return False
            
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "event_type": "run_bot_command",
            "client_payload": {
                "command": "webhook_trigger",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 204:
            logger.info("Webhook sent successfully")
            return True
        else:
            logger.error(f"Webhook failed: {response.status_code} {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return False

def main():
    """Main function"""
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден!")
        return
    
    # Check if we're in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print("🤖 Running in GitHub Actions mode")
        
        # Create webhook bot
        bot = WebhookBot(bot_token, max_runtime=280)  # 5 минут - 20 секунд на остановку
        
        try:
            bot.run_with_timeout()
        except KeyboardInterrupt:
            print("\n👋 Бот остановлен пользователем")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            
        print(f"✅ Бот завершил работу. Обработано команд: {bot.commands_processed}")
        
        # Send notification to admin with restart instructions
        try:
            chat_id = os.getenv('CHAT_ID')
            if chat_id:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                
                if bot.commands_processed > 0:
                    data = {
                        'chat_id': chat_id,
                        'text': f"✅ Вебхук бот завершил работу\n📝 Обработано команд: {bot.commands_processed}\n🔄 Для перезапуска отправьте любую команду\n\n💡 Или запустите вручную:\n1. Actions > Webhook Bot Runner\n2. Нажмите 'Run workflow'",
                        'parse_mode': 'Markdown'
                    }
                else:
                    data = {
                        'chat_id': chat_id,
                        'text': f"🤖 Бот завершил работу (нет команд)\n📅 Время: {datetime.now().strftime('%H:%M:%S')}\n🔄 Для перезапуска отправьте любую команду\n\n💡 Бот работает по запросу!\nКаждые 15 минут проверяется очередь команд.",
                        'parse_mode': 'Markdown'
                    }
                
                requests.post(url, json=data)
        except:
            pass
    else:
        print("🚀 Local mode - running standard bot")
        # Run standard bot for local testing
        bot = VPNBot(bot_token)
        bot.run()

if __name__ == '__main__':
    main()
