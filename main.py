from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import KoboldApiLLM
import re

print('Starting up bot...')

TOKEN: Final = 'put your telegram token bot here!'
BOT_USERNAME: Final = '@your_bot_name'
llm = KoboldApiLLM(endpoint="http://localhost:5001")#change endpoint link to yours
#you can set the conversation parameter like temperature on variable above
memory = ConversationBufferWindowMemory(k=2) #k means how much conversation will be saved. k=2 means only 2 conversation before saved(Human, AI, Human, AI)


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = 'Hello there! I\'m Nina, an AI assistant. What\'s up?'
    await update.message.reply_text(reply)
    memory.save_context({"Human": "Hello"}, {"AI": reply})


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()
    today = date.today()

    if 'hello' in processed:
        memory.save_context({"Human": text}, {"AI": "Hello there. How can I help you?"})
        return "Hello there. How can I help you?"

    if 'who are you' in processed:
        memory.save_context({"Human": text}, {"AI": "I'm an AI digital assistant. I'm here ready to help you."})
        return "I'm an AI digital assistant. I'm here ready to help you."
    
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    response = conversation.predict(input=text, stop=["You: ", "User: ", "Human: ", "Bot: ", "AI: ", "Nina: "])
    response = re.split("Human: |User: |\n", response)
    response = response[0]

    memory.buffer.pop()
    memory.buffer.pop()
    memory.save_context({"input": text}, {"output": response})

    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('AI:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
