from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Dict, Optional
from telegram import Update
from ai_chat import AIChat


class TelegramAIBot:
    """
    Telegram bot integrated with Local LLM to provide AI responses. Supports multiple chat sessions for multiple users.
    
    Parameters:
    ----------
    telegram_token (str): Token bot Telegram
    base_url (str): Local LLM URL with OpenAI schema
    openai_api_key (str): API key OpenAI
    system_prompt (str, optional): AI's system prompt
    model (str): Model name
    memory_size (int): Chat memory window
    """
    def __init__(
        self,
        telegram_token: str,
        base_url: str,
        openai_api_key: str,
        model: str,
        system_prompt: Optional[str] = None,
        memory_size: int = 20
    ):
        self.telegram_token = telegram_token
        self.base_url = base_url
        self.openai_api_key = openai_api_key
        self.system_prompt = system_prompt
        self.model = model
        self.memory_size = memory_size
        # Save chat instance for each user
        self.chat_sessions: Dict[int, AIChat] = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler for command /start"""
        user_name = update.effective_user.first_name
        
        welcome_message = (
            f"Halo {user_name}! 👋\n\n"
            "Aku Nina, asisten digital AI."
            "Jadi ada yang bisa kubantu hari ini?.\n\n"
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
                memory_size = self.memory_size,
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
        telegram_token = "qwertyuiop",
        base_url = ".../v1",
        openai_api_key = "abcdefghij",
        model = "model-name"
    )
    
    bot.run()