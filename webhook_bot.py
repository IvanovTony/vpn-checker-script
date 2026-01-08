#!/usr/bin/env python3
"""
Webhook mode Telegram Bot for 24/7 operation on cloud platforms
Works with Flask for webhook handling
"""

import os
import logging
import asyncio
from telegram_bot import VPNBot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request, abort
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class WebhookVPNBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.webhook_url = os.getenv('WEBHOOK_URL')
        self.port = int(os.getenv('PORT', 8080))
        
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Initialize bot core
        self.bot_core = VPNBot(self.token)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.application = None
        
    async def setup_bot(self):
        """Setup bot with handlers"""
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers using correct method names from VPNBot
        self.application.add_handler(CommandHandler("start", self.bot_core.start_command))
        self.application.add_handler(CommandHandler("help", self.bot_core.help_command))
        self.application.add_handler(CommandHandler("ru", self.bot_core.ru_command))
        self.application.add_handler(CommandHandler("all", self.bot_core.all_command))
        self.application.add_handler(CommandHandler("vless", self.bot_core.vless_command))
        self.application.add_handler(CommandHandler("fast", self.bot_core.fast_command))
        self.application.add_handler(CommandHandler("random", self.bot_core.random_command))
        self.application.add_handler(CommandHandler("status", self.bot_core.status_command))
        
        # Add error handler
        self.application.add_error_handler(self.bot_core.error_handler)
        
        logger.info("Bot handlers configured")
        
    def setup_flask_routes(self):
        """Setup Flask routes for webhook"""
        
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            """Handle webhook requests from Telegram"""
            if request.headers.get('content-type') != 'application/json':
                abort(403)
                
            update = request.get_json()
            if update:
                # Process update asynchronously
                asyncio.create_task(self.process_update(update))
                return 'OK'
            else:
                abort(400)
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return {'status': 'healthy', 'bot': 'running'}, 200
            
        @self.app.route('/')
        def index():
            """Index endpoint"""
            return {
                'service': 'VPN Checker Bot',
                'mode': 'webhook',
                'status': 'running',
                'webhook_url': self.webhook_url
            }, 200
        
        logger.info("Flask routes configured")
        
    async def process_update(self, update):
        """Process Telegram update"""
        try:
            if self.application:
                await self.application.initialize()
                await self.application.process_update(update)
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            
    async def setup_webhook(self):
        """Setup Telegram webhook"""
        try:
            if self.application and self.application.bot:
                await self.application.bot.set_webhook(
                    url=f"{self.webhook_url}/webhook",
                    drop_pending_updates=True
                )
                logger.info(f"Webhook set to: {self.webhook_url}/webhook")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            raise
            
    async def run(self):
        """Run the bot with webhook"""
        await self.setup_bot()
        self.setup_flask_routes()
        
        # Setup webhook
        if self.webhook_url:
            await self.setup_webhook()
        else:
            logger.warning("WEBHOOK_URL not set, webhook won't be configured")
        
        logger.info("Webhook bot is ready to receive updates")
        
        # Run Flask app
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

def run_polling_bot():
    """Fallback to polling mode if webhook is not configured"""
    logger.info("Running bot in polling mode...")
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found")
        return
        
    bot_core = VPNBot(bot_token)
    bot_core.run()

if __name__ == "__main__":
    # Railway automatically sets PORT and provides webhook URL
    port = int(os.getenv('PORT', 8080))
    webhook_url = os.getenv('WEBHOOK_URL')
    
    # For Railway, we need to detect if we're in production
    is_railway = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RAILWAY_SERVICE_NAME')
    
    if webhook_url or is_railway:
        # Run webhook mode (production on Railway)
        logger.info("🚀 Starting bot in webhook mode for Railway...")
        logger.info(f"🌐 Port: {port}")
        logger.info(f"🔗 Webhook URL: {webhook_url or 'Will be set automatically'}")
        
        bot = WebhookVPNBot()
        
        # For Railway, we need to run the webhook server
        async def start_webhook():
            await bot.setup_bot()
            bot.setup_flask_routes()
            
            if bot.webhook_url:
                await bot.setup_webhook()
            
            logger.info("🤖 Webhook bot is ready!")
            bot.app.run(host='0.0.0.0', port=port, debug=False)
        
        asyncio.run(start_webhook())
    else:
        # Run polling mode (local development)
        logger.info("🔧 Starting bot in polling mode (local development)...")
        run_polling_bot()
