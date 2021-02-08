import configparser
import os

config = configparser.RawConfigParser()
config.optionxform = str #not to convert config to lowercase
config.read('config.ini')

__vMajor__     = '0'
__vMinor__     = '1'
__vPatch__     = '0'
__vRel__       = 'r'
__version__    = __vMajor__ + '.' + __vMinor__ + '.' + __vPatch__ + __vRel__

BotToken = config.get('Bot','BotToken')
BotAuthorizedIds = config.get('Bot','BotAuthorizedIDs').split(',')
BotName = config.get('Bot','BotName')
GitHubToken = config.get('GitHub','GitHubToken')
GitHubBranch = config.get('GitHub','GitHubBranch')
GitHubUser = config.get('GitHub','GitHubUser')
GitHubRepo = config.get('GitHub','GitHubRepo')
GitHubAuthor = config.get('GitHub','GitHubAuthor')
GitHubEmail  = config.get('GitHub','GitHubEmail')
hour24 = (config.get('Misc','hour24')).lower()
defaultIndentLevel = (config.get('Misc','defaultIndentLevel'))
journalsFilesFormat = (config.get('Misc','journalsFilesFormat'))
journalsFilesExtension = (config.get('Misc','journalsFilesExtension'))
journalsFolder = (config.get('Misc','journalsFolder'))
journalsPrefix = (config.get('Misc','journalsPrefix'))
TODOCommand = (config.get('Misc','TODOCommand'))
BookmarkTag = (config.get('Misc','BookmarkTag'))
hypothesisToken = (config.get('hypothesis','hypothesisToken'))
hypothesisUsername = (config.get('hypothesis','hypothesisUsername'))

def isBotAuthorized(chat_id):
    isBotAuthorizedID = False
    for BotAuthorizedId in BotAuthorizedIds:
        if str(chat_id) == str(BotAuthorizedId):
            isBotAuthorizedID = True
    return isBotAuthorizedID

def isNewer():
    try:
        LastVersionRun = config.get('Bot', 'LastVersionRun')
        if(__version__ != LastVersionRun):
            config.set('Bot', 'LastVersionRun', __version__)
            with open('config.ini', 'w') as configfile: 
                config.write(configfile)
            return True
        else:
            return False
    except:
        config.set('Bot', 'LastVersionRun', __version__)
        with open('config.ini', 'w') as configfile: 
            config.write(configfile)
        return True

def getBotVersion():
    return __version__

def getBotAuthorizedIDs():
    return BotAuthorizedIds