from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Dict, Optional
from telegram import Update
from ai_chat import AIChat


class TelegramAIBot:
    """
    Telegram bot integrated with Local LLM to provide AI responses. Supports multiple chat sessions for multiple users.
    """
    def __init__(
        self,
        telegram_token: str,
        base_url: str,
        openai_api_key: str,
        system_prompt: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ):
        """
        Args:
            telegram_token (str): Token bot Telegram
            openai_api_key (str): API key OpenAI
            system_prompt (str, optional): System prompt untuk AI
            model (str, optional): Model OpenAI yang digunakan
        """
        self.telegram_token = telegram_token
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        self.system_prompt = system_prompt
        self.model = model
        # Save chat instance for each user
        self.chat_sessions: Dict[int, AIChat] = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler for command /start"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        welcome_message = (
            f"Halo {user_name}! 👋\n\n"
            "Saya Nina, asisten digital AI buatan Lord Jofand.\n"
            "Jadi ada yang bisa saya bantu hari ini?.\n\n"
            "Beberapa command yang tersedia:\n"
            "/start - Memulai bot\n"
            "/clear - Menghapus riwayat chat\n"
            "/help - Menampilkan bantuan"
        )
        
        await update.message.reply_text(welcome_message)
        
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler for command /help"""
        help_text = (
            "🤖 *Bantuan Penggunaan Bot*\n\n"
            "1. Kirim pesan apapun untuk mendapatkan respons\n"
            "2. Bot akan mengingat konteks percakapan\n"
            "3. Gunakan /clear untuk menghapus riwayat\n"
            "4. Bot sadar akan waktu dan akan merespons sesuai\n\n"
            "Command tersedia:\n"
            "/start - Memulai bot\n"
            "/clear - Menghapus riwayat chat\n"
            "/help - Menampilkan pesan ini"
        )
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
        
    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler for command /clear"""
        user_id = update.effective_user.id
        
        if user_id in self.chat_sessions:
            self.chat_sessions[user_id].clear_history()
            await update.message.reply_text("✨ Riwayat chat telah dihapus!")
        else:
            await update.message.reply_text("Belum ada riwayat chat yang perlu dihapus.")
            
    def get_user_chat(self, user_id: int) -> AIChat:
        """
        Create or get chat session for each users.
        
        Args:
            user_id (int): Telegram User ID
            
        Returns:
            AIChat: Instance AIChat for specific users
        """
        if user_id not in self.chat_sessions:
            self.chat_sessions[user_id] = AIChat(
                api_key = self.openai_api_key,
                base_url = self.base_url,
                system_prompt = self.system_prompt,
                model = self.model,
                timezone = "Asia/Jakarta"
            )
        return self.chat_sessions[user_id]
            
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """User message handler"""
        user_id = update.effective_user.id
        user_message = update.message.text
        # Typing status
        await context.bot.send_chat_action(chat_id = update.effective_chat.id, action = 'typing')
        try:
            # Get chat session for  user
            user_chat = self.get_user_chat(user_id)
            # Get responds from AI
            response = user_chat.send_message(user_message)
            # Send responds
            await update.message.reply_text(response)
            
        except Exception as e:
            error_message = (
                "Maaf, terjadi kesalahan saat memproses pesan Anda. "
                "Silakan coba lagi nanti atau hubungi administrator."
            )
            await update.message.reply_text(error_message)
            print(f"Error handling message: {str(e)}")
                
    def run(self):
        application = Application.builder().token(self.telegram_token).build()
        
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help))
        application.add_handler(CommandHandler("clear", self.clear))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        print("Bot is running...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":    
    bot = TelegramAIBot(
        telegram_token = "6373263211:AAEtw-ng4l58YqcCwvm_Mi-q0NqGCsB7QCQ",
        base_url = "http://10.12.1.175:11112/v1",
        openai_api_key = "sk-hynix",
        model = "gemma2-9b-cpt-sahabatai-v1-instruct"
    )
    
    bot.run()