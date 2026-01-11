import os
import asyncio
import logging
import random
import io
from datetime import datetime, timedelta
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

# Configuration
BASE_DIR = "checked"
FOLDER_RU = os.path.join(BASE_DIR, "RU_Best")
FOLDER_EURO = os.path.join(BASE_DIR, "My_Euro")
CHANNEL_NAME = "@vpnCheckerScript"

EURO_CODES = {"NL", "DE", "FI", "GB", "FR", "SE", "PL", "CZ", "AT", "CH", "IT", "ES", "NO", "DK", "BE", "IE", "LU", "EE", "LV", "LT"}

def get_country_from_key(key: str) -> str:
    """Извлечь код страны из ключа (из тега в конце)"""
    try:
        # Код страны в теге: #100ms_NO или #519ms_RU
        if "#" in key:
            parts = key.split("#")[-1]
            # Формат: 100ms_NO_country или 100ms_RU
            country_parts = parts.split("_")
            if len(country_parts) >= 2:
                country = country_parts[1]
                # Проверяем что это код страны (2-3 символа)
                if len(country) >= 2:
                    return country.upper()
    except:
        pass
    return None

# Функция для получения московского времени
def get_moscow_time():
    """Получить текущее время в часовом поясе Москва (UTC+3)"""
    return datetime.now() + timedelta(hours=3)

def get_last_update_time(folder: str, prefix: str) -> str:
    """Получить время последнего обновления ключей из папки"""
    try:
        if not os.path.exists(folder):
            return "Нет данных"
        
        latest_time = None
        for filename in os.listdir(folder):
            if filename.endswith('.txt'):
                filepath = os.path.join(folder, filename)
                file_time = os.path.getmtime(filepath)
                if latest_time is None or file_time > latest_time:
                    latest_time = file_time
        
        if latest_time:
            # Конвертируем в московское время
            moscow_time = datetime.fromtimestamp(latest_time) + timedelta(hours=3)
            return moscow_time.strftime('%d.%m.%Y %H:%M')
        else:
            return "Нет данных"
    except Exception as e:
        logger.error(f"Error getting last update time: {e}")
        return "Ошибка"


class VPNBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("ru", self.ru_command))
        self.application.add_handler(CommandHandler("all", self.all_command))
        self.application.add_handler(CommandHandler("vless", self.vless_command))
        self.application.add_handler(CommandHandler("fast", self.fast_command))
        self.application.add_handler(CommandHandler("random", self.random_command))
        self.application.add_handler(CommandHandler("youtube", self.youtube_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("update", self.update_command))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            "🎉 *Добро пожаловать в VPN Checker Bot!*\n\n"
            "📋 *Доступные команды:*\n"
            "/ru - Получить рабочие ключи для России\n"
            "/all - Получить все рабочие ключи\n"
            "/vless - Получить топ-50 самых быстрых VLESS ключей России\n"
            "/fast - Получить топ-5 самых быстрых VLESS ключей России\n"
            "/random - Получить 5 случайных VLESS ключей России\n"
            "/youtube - Получить VLESS ключи для разблокировки YouTube в России\n"
            "/update - 🔄 Обновить ключи (занимает 5-10 минут)\n"
            "/status - Проверить статус ключей\n"
            "/help - Показать это сообщение\n\n"
            f"📺 *Наш канал:* {CHANNEL_NAME}\n"
            "⚡ *Ключи обновляются автоматически!*"
        )
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = (
            "🤖 *Помощь по командам:*\n\n"
            "*/ru* - 🔹 Отправляет актуальные VPN ключи для России\n"
            "*/all* - 🔹 Отправляет все доступные ключи\n"
            "*/vless* - 🔹 Отправляет топ-50 самых быстрых VLESS ключей России\n"
            "*/fast* - 🔹 Отправляет топ-5 самых быстрых VLESS ключей России\n"
            "*/random* - 🔹 Отправляет 5 случайных VLESS ключей России (из топ-1000)\n"
            "*/youtube* - 🔹 Отправляет VLESS ключи для разблокировки YouTube в России\n"
            "*/update* - 🔹 🔄 Запускает обновление ключей (занимает 5-10 минут)\n"
            "*/status* - 🔹 Показывает статус и количество ключей\n"
            "*/help* - 🔹 Показывает это сообщение\n\n"
            f"📺 *Канал:* {CHANNEL_NAME}\n"
            "⚠️ *Ключи регулярно проверяются на работоспособность*"
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    def get_keys_from_file(self, filepath: str) -> list:
        """Read keys from file and return as list"""
        try:
            if not os.path.exists(filepath):
                return []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                keys = [line.strip() for line in f.readlines() if line.strip()]
            return keys
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            return []
    
    def get_all_keys_from_folder(self, folder: str, prefix: str) -> list:
        """Get all keys from all files in folder"""
        all_keys = []
        if not os.path.exists(folder):
            return all_keys
        
        # Сортируем файлы по имени для правильного порядка (part1, part2, part3...)
        sorted_files = sorted(os.listdir(folder))
        
        for filename in sorted_files:
            if filename.endswith('.txt'):
                filepath = os.path.join(folder, filename)
                keys = self.get_keys_from_file(filepath)
                all_keys.extend(keys)
        
        return all_keys
    
    async def send_keys_message(self, update: Update, keys: list, title: str, emoji: str = "🔑", folder: str = None, prefix: str = None):
        """Send keys to user with proper formatting"""
        if not keys:
            await update.message.reply_text(
                f"❌ *{title}*\n\nК сожалению, в данный момент нет доступных ключей. "
                "Попробуйте позже или проверьте наш канал.",
                parse_mode='Markdown'
            )
            return
        
        # Count keys by protocol
        vless_keys = [k for k in keys if k.startswith('vless://')]
        vmess_keys = [k for k in keys if k.startswith('vmess://')]
        trojan_keys = [k for k in keys if k.startswith('trojan://')]
        ss_keys = [k for k in keys if k.startswith('ss://')]
        
        # Get last update time
        if folder and prefix:
            last_update = get_last_update_time(folder, prefix)
        else:
            last_update = "Нет данных"
        
        # Create message
        message_parts = [
            f"{emoji} *{title}*",
            f"📊 *Всего ключей:* {len(keys)}",
            f"🔹 VLESS: {len(vless_keys)}",
            f"🔹 VMess: {len(vmess_keys)}",
            f"🔹 Trojan: {len(trojan_keys)}",
            f"🔹 Shadowsocks: {len(ss_keys)}",
            f"📅 *Обновлено:* {last_update}",
            f"📺 *Канал:* {CHANNEL_NAME}"
        ]
        
        # Send summary message
        await update.message.reply_text('\n'.join(message_parts), parse_mode='Markdown')
        
        # Send keys in chunks if there are many
        if len(keys) > 50:
            # Send first 50 keys
            first_chunk = keys[:50]
            await self.send_keys_chunk(update, first_chunk, f"{title} (часть 1/2)")
            
            # Send remaining keys
            second_chunk = keys[50:]
            await self.send_keys_chunk(update, second_chunk, f"{title} (часть 2/2)")
        else:
            # Send all keys at once
            await self.send_keys_chunk(update, keys, title)
    
    async def send_keys_chunk(self, update: Update, keys: list, title: str):
        """Send a chunk of keys as a file"""
        if not keys:
            return
        
        # Create content
        content = '\n'.join(keys)
        
        # Create file
        filename = f"{title.replace(' ', '_').lower()}_{get_moscow_time().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            # Send as text message if content is short
            if len(content) < 4000:
                await update.message.reply_text(
                    f"📄 *{title}*\n\n```\n{content[:2000]}\n```",
                    parse_mode='Markdown'
                )
                if len(content) > 2000:
                    await update.message.reply_text(
                        f"📄 *{title} (продолжение)*\n\n```\n{content[2000:]}\n```",
                        parse_mode='Markdown'
                    )
            else:
                # Send as file for large content
                file = io.BytesIO(content.encode('utf-8'))
                file.name = filename
                await update.message.reply_document(
                    document=file,
                    filename=filename,
                    caption=f"📄 {title} ({len(keys)} ключей)"
                )
        except Exception as e:
            logger.error(f"Error sending keys chunk: {e}")
            await update.message.reply_text(
                "❌ Произошла ошибка при отправке ключей. Попробуйте позже.",
                parse_mode='Markdown'
            )
    
    async def ru_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ru command"""
        keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        await self.send_keys_message(update, keys, "🇷🇺 Ключи для России", "🇷🇺", FOLDER_RU, "ru_white")
    
    
    async def all_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /all command"""
        ru_keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        euro_keys = self.get_all_keys_from_folder(FOLDER_EURO, "my_euro")
        all_keys = ru_keys + euro_keys
        
        # Get the latest update time from both folders
        ru_update = get_last_update_time(FOLDER_RU, "ru_white")
        euro_update = get_last_update_time(FOLDER_EURO, "my_euro")
        
        # Use the most recent time
        if ru_update != "Нет данных" and euro_update != "Нет данных":
            latest_update = ru_update if ru_update > euro_update else euro_update
        elif ru_update != "Нет данных":
            latest_update = ru_update
        elif euro_update != "Нет данных":
            latest_update = euro_update
        else:
            latest_update = "Нет данных"
        
        await self.send_keys_message(update, all_keys, "🌍 Все ключи", "🌍")
    
    async def vless_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vless command - send top 50 fastest VLESS keys from all files"""
        ru_keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        
        # Filter only VLESS keys (any country)
        vless_keys = [k for k in ru_keys if k.startswith('vless://')]
        
        # Take first 50 fastest keys (assuming keys are already sorted by speed in files)
        fastest_vless_keys = vless_keys[:50]
        
        await self.send_keys_message(update, fastest_vless_keys, "⚡ Топ-50 VLESS ключей", "⚡", FOLDER_RU, "ru_white")
    
    async def fast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /fast command - send top 5 fastest VLESS keys from all files"""
        ru_keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        
        # Filter only VLESS keys (any country)
        vless_keys = [k for k in ru_keys if k.startswith('vless://')]
        
        if not vless_keys:
            await update.message.reply_text(
                "❌ *Самые быстрые VLESS ключи*\n\nК сожалению, в данный момент нет доступных VLESS ключей. "
                "Попробуйте позже или проверьте наш канал.",
                parse_mode='Markdown'
            )
            return
        
        # Get top 5 fastest VLESS keys
        fastest_vless_keys = vless_keys[:5]
        
        # Get last update time
        last_update = get_last_update_time(FOLDER_RU, "ru_white")
        
        # Create message with keys
        message_parts = [
            "⚡ *Топ-5 самых быстрых VLESS ключей*",
            f"🔧 *Протокол:* VLESS",
            f"📅 *Обновлено:* {last_update}",
            f"📺 *Канал:* {CHANNEL_NAME}",
            "",
            "🔑 *Ключи:*"
        ]
        
        # Add top 5 fastest keys
        for i, key in enumerate(fastest_vless_keys, 1):
            country = get_country_from_key(key)
            country_emoji = f"🇷🇺" if country == "RU" else f"🌍"
            message_parts.append(f"{i}. {country_emoji} `{country if country else '??'}`")
            message_parts.append(f"`{key}`")
            if i < len(fastest_vless_keys):
                message_parts.append("")  # Add spacing between keys
        
        await update.message.reply_text('\n'.join(message_parts), parse_mode='Markdown')
    
    async def random_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /random command - send random fast VLESS keys from all files"""
        import random
        
        ru_keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        
        # Filter only VLESS keys (any country)
        vless_keys = [k for k in ru_keys if k.startswith('vless://')]
        
        if not vless_keys:
            await update.message.reply_text(
                "❌ *Случайные VLESS ключи*\n\nК сожалению, в данный момент нет доступных VLESS ключей. "
                "Попробуйте позже или проверьте наш канал.",
                parse_mode='Markdown'
            )
            return
        
        # Take top 1000 fastest VLESS keys and select 5 random ones
        fastest_vless_keys = vless_keys[:1000]  # Take first 1000 for better variety
        random_keys = random.sample(fastest_vless_keys, min(5, len(fastest_vless_keys)))
        
        # Get last update time
        last_update = get_last_update_time(FOLDER_RU, "ru_white")
        
        # Create message
        message_parts = [
            "🎲 *Случайные быстрые VLESS ключи*",
            f"🔧 *Протокол:* VLESS",
            f"📅 *Обновлено:* {last_update}",
            f"📺 *Канал:* {CHANNEL_NAME}",
            "",
            "🔑 *Ключи:*"
        ]
        
        # Add random keys with country info
        for i, key in enumerate(random_keys, 1):
            country = get_country_from_key(key)
            country_emoji = f"🇷🇺" if country == "RU" else f"🌍"
            message_parts.append(f"{i}. {country_emoji} `{country if country else '??'}`")
            message_parts.append(f"`{key}`")
            if i < len(random_keys):
                message_parts.append("")  # Add spacing between keys
        
        await update.message.reply_text('\n'.join(message_parts), parse_mode='Markdown')
    
    
    
    
    async def update_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /update command - run main.py to update keys"""
        # Отправляем уведомление о начале обновления
        await update.message.reply_text(
            "🔄 *Начинаю обновление ключей...*\n\n"
            "⏳ Это может занять несколько минут.\n"
            "📊 Скрипт проверит работоспособность ключей.\n"
            "✅ Результаты будут доступны через команду /status",
            parse_mode='Markdown'
        )
        
        logger.info("🔄 Запуск обновления ключей через /update команду")
        
        # Запускаем main.py в отдельном процессе
        import subprocess
        try:
            # Запускаем main.py
            process = subprocess.Popen(
                ['python3', 'main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Ждем завершения (с таймаутом в 10 минут)
            try:
                stdout, stderr = process.communicate(timeout=600)
                
                if process.returncode == 0:
                    # Обновление успешно
                    await update.message.reply_text(
                        "✅ *Обновление завершено успешно!*\n\n"
                        f"📅 {get_moscow_time().strftime('%d.%m.%Y %H:%M')}\n\n"
                        "🎉 Теперь вы можете использовать команды:\n"
                        "  /ru - Ключи для России\n"
                        "  /all - Все ключи\n"
                        "  /status - Статус ключей",
                        parse_mode='Markdown'
                    )
                    logger.info("✅ Обновление ключей завершено успешно")
                else:
                    # Ошибка при выполнении
                    await update.message.reply_text(
                        f"❌ *Ошибка при обновлении*\n\n"
                        f"Код ошибки: {process.returncode}\n\n"
                        "Пожалуйста, проверьте логи или попробуйте позже.",
                        parse_mode='Markdown'
                    )
                    logger.error(f"❌ Ошибка обновления: {stderr}")
                    
            except subprocess.TimeoutExpired:
                process.kill()
                await update.message.reply_text(
                    "⏱ *Превышено время ожидания*\n\n"
                    "Обновление заняло более 10 минут.\n"
                    "Попробуйте позже или проверьте логи.",
                    parse_mode='Markdown'
                )
                logger.error("⏱ Превышен таймаут обновления")
                
        except Exception as e:
            await update.message.reply_text(
                f"❌ *Критическая ошибка*\n\n"
                f"{str(e)}\n\n"
                "Попробуйте позже или проверьте логи.",
                parse_mode='Markdown'
            )
            logger.error(f"❌ Критическая ошибка: {e}")
    
    async def youtube_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /youtube command - send VLESS keys for YouTube unblocking in Russia"""
        ru_keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        
        # Filter only VLESS keys from Russia (for YouTube unblocking)
        vless_ru_keys = [k for k in ru_keys if k.startswith('vless://') and get_country_from_key(k) == 'RU']
        
        if not vless_ru_keys:
            await update.message.reply_text(
                "❌ *VLESS ключи для разблокировки YouTube*\n\nК сожалению, в данный момент нет доступных VLESS ключей из России. "
                "Попробуйте позже или проверьте наш канал.",
                parse_mode='Markdown'
            )
            return
        
        # Take top 10 fastest Russian VLESS keys for YouTube
        fastest_ru_vless_keys = vless_ru_keys[:10]
        
        # Get last update time
        last_update = get_last_update_time(FOLDER_RU, "ru_white")
        
        # Create message
        message_parts = [
            "🎬 *VLESS ключи для разблокировки YouTube в России*",
            f"🔧 *Протокол:* VLESS",
            f"🌍 *Страна:* 🇷🇺 Россия",
            f"📅 *Обновлено:* {last_update}",
            f"📺 *Канал:* {CHANNEL_NAME}",
            "",
            "🔑 *Топ-10 VLESS ключей России:*"
        ]
        
        # Add Russian VLESS keys
        for i, key in enumerate(fastest_ru_vless_keys, 1):
            message_parts.append(f"`{key}`")
            if i < len(fastest_ru_vless_keys):
                message_parts.append("")  # Add spacing between keys
        
        await update.message.reply_text('\n'.join(message_parts), parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        ru_keys = self.get_all_keys_from_folder(FOLDER_RU, "ru_white")
        euro_keys = self.get_all_keys_from_folder(FOLDER_EURO, "my_euro")
        total_keys = len(ru_keys) + len(euro_keys)
        
        # Count by protocol
        all_keys = ru_keys + euro_keys
        vless_count = len([k for k in all_keys if k.startswith('vless://')])
        vmess_count = len([k for k in all_keys if k.startswith('vmess://')])
        trojan_count = len([k for k in all_keys if k.startswith('trojan://')])
        ss_count = len([k for k in all_keys if k.startswith('ss://')])
        
        # Get last update times
        ru_update = get_last_update_time(FOLDER_RU, "ru_white")
        euro_update = get_last_update_time(FOLDER_EURO, "my_euro")
        
        # Use most recent time
        if ru_update != "Нет данных" and euro_update != "Нет данных":
            latest_update = ru_update if ru_update > euro_update else euro_update
        elif ru_update != "Нет данных":
            latest_update = ru_update
        elif euro_update != "Нет данных":
            latest_update = euro_update
        else:
            latest_update = "Нет данных"
        
        status_message = (
            "📊 *Статус VPN ключей*\n\n"
            f"🇷🇺 *Россия:* {len(ru_keys)} ключей (обновлено: {ru_update})\n"
            f"🇪🇺 *Европа:* {len(euro_keys)} ключей (обновлено: {euro_update})\n"
            f"🌍 *Всего:* {total_keys} ключей\n\n"
            "🔹 *По протоколам:*\n"
            f"  • VLESS: {vless_count}\n"
            f"  • VMess: {vmess_count}\n"
            f"  • Trojan: {trojan_count}\n"
            f"  • Shadowsocks: {ss_count}\n\n"
            f"📅 *Последнее обновление:* {latest_update}\n"
            f"📺 *Канал:* {CHANNEL_NAME}"
        )
        
        await update.message.reply_text(status_message, parse_mode='Markdown')
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        if update and hasattr(update, 'message'):
            await update.message.reply_text(
                "❌ Произошла ошибка. Попробуйте позже.",
                parse_mode='Markdown'
            )
    
    def run(self):
        """Run bot"""
        self.application.add_error_handler(self.error_handler)
        
        print("🤖 VPN Checker Bot запущен!")
        print("📋 Доступные команды:")
        print("  /start - Приветствие")
        print("  /help - Помощь")
        print("  /ru - Ключи для России")
        print("  /all - Все ключи")
        print("  /vless - Только VLESS ключи России")
        print("  /fast - Топ-5 самых быстрых VLESS ключей России")
        print("  /random - 5 случайных VLESS ключей России (из топ-1000)")
        print("  /youtube - VLESS для разблокировки YouTube в России")
        print("  /update - 🔄 Обновить ключи")
        print("  /status - Статус ключей")
        print(f"📺 Канал: {CHANNEL_NAME}")
        
        print("💡 Примечание: Команды можно установить вручную через @BotFather")
        print("📝 Список команд для установки в @BotFather:")
        print("start - 🎉 Запустить бота")
        print("help - 📖 Показать помощь")
        print("ru - 🇷🇺 Получить ключи для России")
        print("all - 🌍 Получить все ключи")
        print("vless - ⚡ Топ-50 VLESS ключей России")
        print("fast - 🚀 Самый быстрый VLESS ключ России")
        print("random - 🎲 5 случайных VLESS ключей России")
        print("update - 🔄 Обновить ключи")
        print("status - 📊 Статус ключей")
        
        # Use run_polling (synchronous method)
        self.application.run_polling(drop_pending_updates=True)

def main():
    """Main function"""
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден!")
        print("Пожалуйста, установите переменную окружения:")
        print("export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        print("Или создайте файл .env с строкой:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    # Create and run bot
    bot = VPNBot(bot_token)
    
    # Run bot synchronously
    bot.run()

if __name__ == '__main__':
    main()
