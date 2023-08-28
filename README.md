# private-AI-telegram-bot
An AI LLM personal asistant that run on your local machine. 100% privacy and only CPU needed. But if you have GPU, it would decrease the inferencing time further. It means, faster at processing and generating the chat!

Unfortunately, this AI bot only has short-term memory, which can only remember the two pair of chatting between user and AI bot due to my potato laptop 🥔 💻. If you have better CPU, or even better GPU, this program can be modified to remember more pair of chat history for better chatting experiences.


## What am I use on this project?
### koboldcpp
I'm using koboldcpp as an AI LLM server. Koboldcpp can run any LLM model using CPU and sacrificing only a little bit of perplexity. The difference will be hardly noticed, but faster in inference and generate.

The LLM model need to be converted to GGML/GGUF format and then quantized to 8 bit, 5 bit, or 4 bit(Lower than 4 bit will increase the perplexity siginificantly). Or we can download the GGML/GGUF quantized model from https://huggingface.co/.

### Langchain
Langchain is used for creating LLM's memory. Currently I'm setting it to use `ConversationBufferWindowMemory` with `k=2`. Apart from my machine limitation, this is too a proof of concept that my project can run and use the chat history memory.

Langchain in here is used too as a "bridge" for connecting the Python program to koboldcpp

### python-telegram-bot
This library can provide a connection to Telegram bot. I'm using Telegram as an user interface for easy use anywhere and anytime.


## Future Plan 
This project has a lot of room for improving. My plan for the future about this project is to create a lively, talkative, and smart digital AI asistant that can help any of user needs. Now I'm working on adding:
- [ ] Long-Term Memory using vector database
- [ ] Access for read and write user's Google Calendar
- [ ] Access to internet for more knowledge and helping user to make decisions
- [ ] Processing word and excel files(Summary, analytics, seek new insights, etc...)

## How to run
### Windows
1. Download `koboldccp.exe` from https://github.com/LostRuins/koboldcpp/releases/latest
2. Locate the quantized `ggml.bin` model file
3. Install the following libraries `python-telegram-bot` and `langchain` via `pip`
4. Run the `koboldccp.exe` and select the downloaded model file
5. Edit the `url` variable on `main.py`. Match with your `koboldccp.exe` links. Usually it'll be http://localhost:5001/
6. Run the `main.py`

### Ubuntu/Linux
1. Install the following libraries `python-telegram-bot`, `langchain`, `libclblast-dev`, `libopenblas-dev`, `Tkinter` via `pip`
2. Clone the koboldcpp repo (visit: https://github.com/LostRuins/koboldcpp)
3. You will have to compile your binaries from source. A makefile is provided, simply run `make LLAMA_OPENBLAS=1 LLAMA_CLBLAST=1`
4. Locate the quantized `ggml.bin` model file
5. After all binaries are built, run the python script with the command `python koboldcpp.py` and select the downloaded model file
6. Edit the `url` variable on `main.py`. Match with your `koboldccp.exe` links. Usually it'll be http://localhost:5001/
7. Run the `main.py`


More info about koboldcpp & python-telegram-bot, please visit their github at https://github.com/LostRuins/koboldcpp & https://github.com/python-telegram-bot/python-telegram-bot


Made an tested on Acer Aspire E14(Intel i5-8250U, 12GB RAM, Nvidia MX130) 
