# private-AI-telegram-bot 🤖 💬
My personal project on weekend. An AI LLM personal asistant that run on your local machine. 100% privacy and only CPU needed. But if you have GPU, it would decrease the inferencing time further. It means, faster at processing and generating the chat!

Unfortunately, this AI bot only has short-term memory, which can only remember the last 10 messages between user and bot due to my potato laptop 🥔 💻. If you have better CPU, or even better GPU, this program can be modified to remember more pair of chat history for better chatting experiences.


## What am I use on this project?
### vLLM
As the AI LLM backend. Why bother paying external services, if your potato PC could run on your own privately?

### python-telegram-bot
This library can provide a connection to Telegram bot. I'm using Telegram as an user interface for easy use anywhere and anytime.


## Future Plan 
This project has a lot of room for improving. My plan for the future about this project is to create a lively, talkative, and smart digital AI asistant that can help any of user needs.
- [ ] Long-Term Memory using vector database
- [ ] Access for read and write user's Google Calendar
- [ ] Access to internet for more knowledge and helping user to make decisions
- [ ] Processing word and excel files(Summary, analytics, seek new insights, etc...)

## Installation
1. Install vLLM by `pip install vllm`
2. Download open source models from HuggingFace. Then run them as the server with Open AI schema
3. Go to folder repository
4. Then `pip install -r requirements.txt`

## How to run
FYI I use Linux Ubuntu. So I just need to go to the folder repo, then `python telegram_bot.py`. Don't forget to put your Telegram bot token, local LLM url, and the api key.


More info about vLLM & python-telegram-bot, please visit them at https://docs.vllm.ai/en/latest/ & https://github.com/python-telegram-bot/python-telegram-bot