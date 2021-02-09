from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, PicklePersistence, Updater
#from telegram import ParseMode

from config import (
    BotToken, isBotAuthorized, BotName, GitHubBranch, getBotVersion, isNewer, 
    getBotAuthorizedIDs, isManageHypothesis, isHypothesisEmbedded
)

from dictionaries import bot_messages
from git import updateJournal, updateAsset
from utils import getUptime, getAnnotationPath, getPageTitle, getWebPageTitle
from hypothesis import getHypothesisAnnotations
from io import BytesIO


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
                             text=bot_messages['JOURNALENTRY_MESSAGE'].format(update.message.text))

def version(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE']) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['VER_MESSAGE'].format(BotName,getBotVersion())) 

def help(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE']) 
    else:
        commands = ["/help","/start","/uptime","/ver","/anno"]
        message = bot_messages['HELP_MESSAGE']
        for command in commands:
            message += command + "\n"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=message) 

def hypothesis(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        if(isManageHypothesis()):
            path = getAnnotationPath(context.args[0])
            #print(path)
            pageAlias = getWebPageTitle(context.args[0])
            
            updateJournal(getHypothesisAnnotations(context.args[0]), False, path, True, pageAlias)

            if(isHypothesisEmbedded()):
                updateJournal(entry='{{embed [[' + getPageTitle(path) + ']]}}')
            else: 
                updateJournal(entry="Annotations of [" + pageAlias + "](" + getPageTitle(path) + ")")
        else:
            updateJournal(getHypothesisAnnotations(context.args[0]), False)

        context.bot.send_message(chat_id=update.effective_chat.id,
                            text=bot_messages['HYPOTHESIS_MESSAGE'].format(context.args[0]))
    
def image_handler(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        file = context.bot.getFile(update.message.photo[-1].file_id)
        f =  BytesIO(file.download_as_bytearray())
        path = updateAsset(f.getvalue(),"jpg")
        updateJournal(path, ignoreURL=True)
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['IMAGEUPLOAD_MESSAGE'].format(BotName,getBotVersion())) 

    
def main():
    bot_persistence = PicklePersistence(filename='persistence')

    updater = Updater(token=BotToken, persistence=bot_persistence, use_context=True)
    dispatcher = updater.dispatcher

    if(isNewer()):
        for BotAuthorizedId in getBotAuthorizedIDs():
            updater.bot.sendMessage(chat_id=BotAuthorizedId, text=bot_messages['VERCHANGE_MESSAGE'])


    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('uptime', uptime))
    dispatcher.add_handler(CommandHandler('ver', version))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('anno', hypothesis))   
    dispatcher.add_handler(MessageHandler(Filters.text, addEntry))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
