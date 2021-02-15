from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, PicklePersistence, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO, StringIO
from uuid import uuid4

# from flashcards import updateFlashcard, getFlashcardFromPool
import flashcards

from config import (
    BotToken, isBotAuthorized, BotName, GitHubBranch, getBotVersion, isNewer, 
    getBotAuthorizedIDs, isManageHypothesis, isHypothesisEmbedded, getflashcardDailyGoal
)

from dictionaries import bot_messages, btns
from git import updateJournal, updateAsset #, updateFlashCards
from utils import getUptime, getAnnotationPath, getPageTitle, getWebPageTitle, getlatestNews, updateFlashCards, convert2MD, convert2Mindmap
from hypothesis import getHypothesisAnnotations


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
        # print ( context.bot.getFile(update.message.photo[-1]))
        file = context.bot.getFile(update.message.photo[-1].file_id)
        f =  BytesIO(file.download_as_bytearray())
        path = updateAsset(f.getvalue(),"jpg")
        updateJournal(path, ignoreURL=True)
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['IMAGEUPLOAD_MESSAGE'].format(BotName,getBotVersion())) 

def generateMD(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['FILEREQ_MESSAGE']) 
        PageName = str(' '.join(context.args))
        
        s = StringIO()
        s.write(convert2MD(PageName))
        s.seek(0)

        buf = BytesIO()
        buf.write(s.getvalue().encode())
        buf.seek(0)
        #buf.name = f'PageName.md'
        buf.name = f'{PageName}.md'

        context.bot.send_document(chat_id=update.message.chat_id, document=buf)

def generateMinmapHTML(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['FILEREQ_MESSAGE']) 

        PageName = str(' '.join(context.args))

        HTMLOut = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>""" + PageName + """ Mindmap</title>
        <style>
        * {
        margin: 0;
        padding: 0;
        }
        #mindmap {
        display: block;
        width: 100vw;
        height: 100vh;
        }
        </style>

        </head>
        <body>
        <svg id="mindmap"></svg>
        <script src="https://cdn.jsdelivr.net/npm/d3@6.3.1"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.2.2"></script>
        <script>((e,t,r)=>{const{Markmap:n}=e();window.mm=n.create("svg#mindmap",null==t?void 0:t(),r)})(()=>window.markmap,t=>{return t=t||window.d3,{color:(n=t.scaleOrdinal(t.schemeCategory10),t=>n(t.p.i))};var n},
        """ + convert2Mindmap(PageName) + """)</script>
        </body>
        </html>"""

        s = StringIO()
        s.write(HTMLOut)
        s.seek(0)

        buf = BytesIO()
        buf.write(s.getvalue().encode())
        buf.seek(0)
        fileName = "mm_" + PageName.replace(' ','_').strip()
        buf.name = f'{fileName}.html'

        context.bot.send_document(chat_id=update.message.chat_id, document=buf)

def ShowSkipCancelMenu(update, context, uid):
    button_list = [
        [InlineKeyboardButton('😭',callback_data= "ansrfdbk_0_" + uid),
         InlineKeyboardButton('😖',callback_data= "ansrfdbk_1_" + uid),
         InlineKeyboardButton('😕',callback_data= "ansrfdbk_2_" + uid)],
        [InlineKeyboardButton('😊',callback_data= "ansrfdbk_3_" + uid),
         InlineKeyboardButton('😄',callback_data= "ansrfdbk_4_" + uid),
         InlineKeyboardButton('🥳',callback_data= "ansrfdbk_5_" + uid)],
        [InlineKeyboardButton(btns['SHOW_ANSWER'], callback_data=btns['SHOW_ANSWER'] + uid), 
         InlineKeyboardButton(btns['SKIP'], callback_data=btns['SKIP'] + uid)],
        [InlineKeyboardButton(btns['CANCEL'], callback_data=btns['CANCEL'])]
    ] 

    message = bot_messages['LINE_BREAK'] + "\n\n" + context.user_data[uid][0].question + "\n" + bot_messages['LINE_BREAK'] + "\n" 
    message += bot_messages['FLASHCARD_OPTIONS']
    reply_markup =  InlineKeyboardMarkup(button_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup) 

def ShowAnswer(update,context):
    uid = update.callback_query.data.replace(btns['SHOW_ANSWER'],'')
    flashcard = context.user_data[uid][0]
    message = flashcard.answer + "\n" + bot_messages['FLASHCARD_SOURCE'] + flashcard.source 
    context.bot.send_message(chat_id=update.effective_chat.id, text=message) 

def AnswerHandler(update, context):
    args = update.callback_query.data.split('_')
    uid = args[2]
    answer = int(args[1])
    flashcard = context.user_data[uid][0]
    flashcard.history.append(answer)
    roundCount = int(context.user_data[uid][1]) + 1
    roundGoal = context.user_data[uid][2]

    message = bot_messages['NEXTROUND_MESSAGE'] + flashcards.updateFlashcard(flashcard)
    context.bot.edit_message_text(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        text = message,
        )
    if roundCount <= roundGoal:
        context.user_data[uid] = [flashcard, roundCount, roundGoal]
        TimeSpacedRepetition(update, context, uid)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="All Done for Today ") 

def Cancel(update,context):
    context.bot.edit_message_text(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        text = bot_messages['CANCELLED_MESSAGE'],
        )

def Skip(update, context):
    uid = update.callback_query.data.replace(btns['SKIP'],'')
    context.bot.edit_message_text(
        message_id = update.callback_query.message.message_id,
        chat_id = update.callback_query.message.chat.id,
        text = bot_messages['SKIPPED_MESSAGE'],
        )
    TimeSpacedRepetition(update, context, uid)

def TimeSpacedRepetition(update, context, uid=""):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE']) 
    else:
        try:
            arg = context.args[0]
        except:
            arg = ""

        if arg == "import":
            importFlashCards(update, context)
        else:
            if(uid):
                roundCount = int(context.user_data[uid][1])
                roundGoal  = int(context.user_data[uid][2])
            else:
                uid = str(uuid4())
                roundCount = 1
                try:
                    roundGoal = int(arg)
                except:
                    roundGoal = getflashcardDailyGoal()

            flashcard = flashcards.getFlashcardFromPool()
            if(flashcard):
                message = "Card " + str(roundCount) + " out of " + str(roundGoal) + "\n" 
                context.bot.send_message(chat_id=update.effective_chat.id, text=message) 
                context.user_data[uid] = [flashcard, roundCount, roundGoal]
                return ShowSkipCancelMenu(update, context, uid)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['NOPENDIGCARDS_MESSAGE'])  

def tsrRetired(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE']) 
    else:
        message = "command /tsr is being replace by /srs please use the latter from now on"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message) 

def importFlashCards(update, context):
    if(not isBotAuthorized(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['UNAUTHORIZED_MESSAGE'].format(update.effective_chat.id)) 
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages['IMPORTINGFC_MESSAGE']) 
        importResults = updateFlashCards()
        message = bot_messages['IMPORTEDFC_MESSAGE'].format(importResults[0],importResults[1])
        context.bot.send_message(chat_id=update.effective_chat.id, text=message) 


def main():
    bot_persistence = PicklePersistence(filename='persistence')

    updater = Updater(token=BotToken, persistence=bot_persistence, use_context=True)
    dispatcher = updater.dispatcher

    # if(isNewer()):
    #     for BotAuthorizedId in getBotAuthorizedIDs():
    #         updater.bot.sendMessage(chat_id=BotAuthorizedId, text=bot_messages['VERCHANGE_MESSAGE'])

    latestNews = getlatestNews()
    for news in latestNews:
        for BotAuthorizedId in getBotAuthorizedIDs():
            updater.bot.sendMessage(chat_id=BotAuthorizedId, text=news)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('uptime', uptime))
    dispatcher.add_handler(CommandHandler('ver', version))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('anno', hypothesis))   
    dispatcher.add_handler(CommandHandler('importFC', importFlashCards))   
    dispatcher.add_handler(CommandHandler('tsr', tsrRetired))   
    dispatcher.add_handler(CommandHandler('srs', TimeSpacedRepetition))   
    # dispatcher.add_handler(CommandHandler('getMD', generateMD))   
    dispatcher.add_handler(CommandHandler('getMM', generateMinmapHTML))   


    dispatcher.add_handler(MessageHandler(Filters.text, addEntry))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))

    dispatcher.add_handler(CallbackQueryHandler(ShowAnswer,pattern=btns['SHOW_ANSWER'])) 
    dispatcher.add_handler(CallbackQueryHandler(AnswerHandler,pattern="ansrfdbk"))
    dispatcher.add_handler(CallbackQueryHandler(Skip,pattern=btns['SKIP']))  
    dispatcher.add_handler(CallbackQueryHandler(Cancel,pattern=btns['CANCEL'])) 


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
