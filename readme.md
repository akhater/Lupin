# Who am i ?
Hey I am Lupin, an Open Source [Telegram](https://telegram.org/) [Python Chat Bot](https://github.com/python-telegram-bot/python-telegram-bot) build for adding quick Journal Entries into [LogSeq](https://github.com/logseq/logseq/)


# Getting Started
Assuming you are already using [LogSeq](https://logseq.com) & are familar with Python

1. Clone me `git clone https://github.com/akhater/Lupin.LogSeqPyBot`
1. [Create a telegram bot](https://core.telegram.org/bots#creating-a-new-bot)
1. Install [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) library using `pip install python-telegram-bot`
1. Install [PyGithub](https://github.com/PyGithub/PyGithub) library using `pip install pyGitHub`
1. Rename `config.sample.ini` to `config.ini`
1. Change values  in `config.ini` to fit your environment 
# Features
* Entries only accepted from telegram AuthorizedIDs so not anyone can add entries to your journal
* Entries will directly be added to your LogSeq Journal in Github
* Entries are tagged with a timestamp supporting both 12 and 24 hrs format
# Credits
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [PyGithub](https://github.com/PyGithub/PyGithub)
* [LogSeq](https://github.com/logseq/logseq/)
