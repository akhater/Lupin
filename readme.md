# Who am I ?
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
* Send `/anno uri` to import all your annotations from for the uri from [Hypothesis](https://web.hypothes.is/)
* Support for both LogSeq regular Journal and custom Journal folder and/or file
* Spaced Repetion: Spaced Repetition capabilities based on SuperMemo2 Algorithm 
* Calendar Generation: Auto generates [PiotrSss](https://piotrsss.github.io/logseq-tools/public/#/mini-calendar) calendar and puts them in the sidebar
* Theme Switcher: Switch between multiple themes by calling /themes
* Generate Mindmaps of your pages by called /getMM PageTitle
* Support for [AGE encryption](https://age-encryption.org/) and encrypted Graphs
## Spaced Repetition
Supported format for flaschards is
```
## #flashcardtag
### Question 1
#### answer line 1
#### answer line 2
### Question 2
#### Answer 2
```
Flashcard tag is customizable
Algorithm used is SuperMemo2
Triggers are 
/tsr import --> scan - import - update your flashcards
/tsr x -> retrieve x flashcards from you pending pool
/tsr -> retrieve the default number of cards set in your config .ini file
Below entry in config.ini specifies you default number of flashcards
```
[TimeSpacedRepetion]
flashcardDailyGoal=10
```
## Theme Switcher
Before being able to use this feature you need to name your various themes in the format `ThemeName.custom.css` and place them in the /logseq folder

## Commands summary 
| Command          | Description                                   |
|------------------|-----------------------------------------------|
| /start           | Just a greeting                               |
| /uptime          | returns Lupin Uptime                          |
| /ver             | returns Lupin running Version                 |
| /help            | help command (WIP)                            |
| /anno URL        | Import hypothesis annotations from URL        |
| /importFC        | Imports your Flashcards into Lupin            |
| /srs import      | alias of /importFC                            |
| /srs x           | starts a round of SRS for x flashcards        |
| /getMM pageTitle | Generates a dynamic MindMap for pageTitle     |
| /pullNow         | Pulls all pages from your Git for fast access |
| /themes          | calls the theme changer                       |
| /encryptAll      | Encrypts all your pages with AGE keys         |
| /decryptAll      | Decrypts all your pages back to clear text    |
## Screenshots
Imported [Hypothesis](https://web.hypothes.is/) notes into LogSeq
![](https://media.discordapp.net/attachments/808007880988426250/808378985016721408/unknown.png?width=998&height=821)
# Credits
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [PyGithub](https://github.com/PyGithub/PyGithub)
* [LogSeq](https://github.com/logseq/logseq/)
* [Hypothesis](https://web.hypothes.is/)
* [PiotrSss](https://piotrsss.github.io/logseq-tools/public/#/mini-calendar)
* [Doctorpangloss](https://gist.github.com/doctorpangloss/13ab29abd087dc1927475e560f876797)
* [Markmap](https://markmap.js.org/)
* [PyAge](https://github.com/jojonas/pyage/tree/master/src/age)
## License
[MIT License](./LICENSE)
