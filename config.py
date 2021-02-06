import configparser
from datetime import datetime
import os

config = configparser.RawConfigParser()
config.optionxform = str #not to convert config to lowercase
config.read('config.ini')

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

def isBotAuthorized(chat_id):
    isBotAuthorizedID = False
    for BotAuthorizedId in BotAuthorizedIds:
        if str(chat_id) == str(BotAuthorizedId):
            isBotAuthorizedID = True
    return isBotAuthorizedID