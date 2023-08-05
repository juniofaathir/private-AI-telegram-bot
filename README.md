# private-AI-telegram-bot
An AI LLM powered telegram bot that run on your local machine. 100% privacy and only CPU needed. But if you have GPU, it would decrease the inferencing time further. It means, faster at processing and generating the chat!

This project has a lot of room for improving. My plan for the future about this project is to create a lively and talkative digital AI asistant that can help any of user needs. It'll be have long-term memory and access to user's productivity apps like Google Calendar

## How to run
### Windows
1. Download `koboldccp.exe` from https://github.com/LostRuins/koboldcpp
2. Download the quantized `ggml.bin` model file from https://huggingface.co/
3. Install the following libraries `python-telegram-bot` and `langchain` via `pip`
4. Run the `koboldccp.exe` and select the downloaded model file
5. Edit the `url` variable on `main.py`. Match with your `koboldccp.exe` links. Usually it's http://localhost:5001/
6. Run the `main.py`

### Ubuntu/Linux
1. Install the following libraries `python-telegram-bot`, `langchain`, `libclblast-dev`, `libopenblas-dev`, `Tkinter` via `pip`
2. You will have to compile your binaries from source. A makefile is provided, simply run `make LLAMA_OPENBLAS=1 LLAMA_CLBLAST=1`
3. Download the quantized `ggml.bin` model file from https://huggingface.co/
4. After all binaries are built, run the python script with the command `python koboldcpp.py` and select the downloaded model file
5. Edit the `url` variable on `main.py`. Match with your `koboldccp.exe` links. Usually it's http://localhost:5001/
6. Run the `main.py`


More info about koboldcpp & python-telegram-bot, please visit their github at https://github.com/LostRuins/koboldcpp & https://github.com/python-telegram-bot/python-telegram-bot
