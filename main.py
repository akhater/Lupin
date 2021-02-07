from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, PicklePersistence, Updater
#from telegram import ParseMode

from config import BotToken, isBotAuthorized, BotName, GitHubBranch, __version__
from dictionaries import bot_messages
from git import updateJournal
from utils import getUptime


def start(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['WELCOME_MESSAGE'].format(BotName)) 

def uptime(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        message = "I've been up for %d days, %d hours, %d minutes, %d seconds" % getUptime()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message) 

def addEntry(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        updateJournal(update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bot_messages['CONFIRMATION_MESSAGE'].format(update.message.text))

def version(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE']) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['VER_MESSAGE'].format(BotName,__version__)) 

def help(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE']) 
    else:
        commands = ["/help","/start","/uptime","/ver"]
        message = bot_messages['HELP_MESSAGE']
        for command in commands:
            message += command + "\n"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=message) 

def main():
    bot_persistence = PicklePersistence(filename='persistence')

    updater = Updater(token=BotToken, persistence=bot_persistence, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('uptime', uptime))
    dispatcher.add_handler(CommandHandler('ver', version))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, addEntry))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()