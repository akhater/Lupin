# Who am i ?
Hey I am Lupin, an Open Source [Telegram](https://telegram.org/) [Python Chat Bot](https://github.com/python-telegram-bot/python-telegram-bot) build for adding quick Journal Entries into [LogSeq](https://github.com/logseq/logseq/)


# Getting Started
Assuming you are already using [LogSeq](https://logseq.com) & are familar with Python.

Lupin requires Python version >= 3.x

1. Clone me `git clone https://github.com/akhater/Lupin`
1. [Create a telegram bot](https://core.telegram.org/bots#creating-a-new-bot)
1. Install [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) library using `pip install python-telegram-bot` or `pip3 install python-telegram-bot`
1. Install [PyGithub](https://github.com/PyGithub/PyGithub) library using `pip install pyGitHub` or `pip3 install pyGitHub`
1. Install the `requests` library using `pip install requests` or `pip3 install requests`
1. Generate a Github token from `https://github.com/settings/tokens`
1. Rename `config.sample.ini` to `config.ini`
1. Change values in `config.ini` to fit your environment 
1. Run the bot using `python main.py` or `python3 main.py` 
# Features
* Privacy always - self hosted & open source
* Security 
    * Entries are only accepted from telegram BotAuthorizedIDs so not anyone can add entries to your journal
* Fully customization with config.ini file
   * Rename it
   * Translate it (no hard coded messages)
   * much more
* Send a thought (any text) and Lupin will
   * Timestamp it: supporting both 12 and 24 hrs format
   * Enter it in your Github hosted Jounral 
* Send your TODO list (by including TODO in the text) and Lupin will convert it to a LogSeq TODO
    * TODO command is customizable
* Send a link and Lupin automatically create a #bookmark entry in your Journal in the form of 
    * 18:48 #bookmark [title](link)
    * #bookmark tag is customizable 
* Send a YouTube video link and Lupin will automatically embedded in your Journal in the form of 
    * 18:52 {{Youtube link}}
* Support for both LogSeq regular Journal and custom Journal folder and/or file
* Other commands: /help | /start | /uptime | /ver
# Credits
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [PyGithub](https://github.com/PyGithub/PyGithub)
* [LogSeq](https://github.com/logseq/logseq/)
## License

[MIT License](./LICENSE)
