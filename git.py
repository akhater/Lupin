from github import Github, InputGitAuthor
from pprint import pprint
#import json

import config
import utils

from dictionaries import git_messages
import flashcards 

GitHubToken = config.GitHubToken
GitHubFullRepo = config.GitHubUser + "/" + config.GitHubRepo
GitHubBranch = config.GitHubBranch
BotName = config.BotName
TODOCommand = config.TODOCommand
assetsFolder = config.getAssetsFolder()

g = Github(GitHubToken)
repo = g.get_repo(GitHubFullRepo)

def push(path, message, content, branch, update=False):
    author = InputGitAuthor(
        config.GitHubAuthor,
        config.GitHubEmail
    )
    #source = repo.get_Branch(Branch)
    #repo.create_git_ref(ref=f"refs/heads/{Branch}", sha=source.commit.sha)  # Create new Branch from master
    if update:  # If file already exists, update it
        #pass
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author)  # Add, commit and push Branch
    else:  # If file doesn't exist, create it
        #pass
        repo.create_file(path, message, content, branch=branch, author=author)  # Add, commit and push Branch
     
def updateJournal(entry, needsBuilding = True, path = None, overwrite=False, alias='', ignoreURL=False):
    if path == None:
        path = utils.getJournalPath()
    if needsBuilding:
        entry = buildJournalEntry(entry, ignoreURL)
    if(GitFileExists(path)):
        file = repo.get_contents(path, ref=GitHubBranch)  # Get file from Branch
        if(overwrite):
            #print(getPageTitle(path))
            data = "---\ntitle: " + utils.getPageTitle(path) + "\nalias: " + alias + "\n---\n\n"
            #print(data)
        else:
            data = file.decoded_content.decode("utf-8")  # Get raw string data
        
        data += (entry).strip() + "\n"

        push(path, git_messages['COMMIT_MESSAGE'].format(BotName, utils.getTimestamp()) , data, GitHubBranch, update=True)
    else:
        data =  "---\ntitle: " + utils.getPageTitle(path) + "\nalias: " + alias + "\n---\n\n" + (entry).strip() + "\n"
        
        push(path, git_messages['COMMIT_MESSAGE'].format(BotName, utils.getTimestamp()) , data, GitHubBranch, update=False)

def GitFileExists(path):
    try:
        repo.get_contents(path, ref=GitHubBranch)  # Get file from Branch
        return True
    except Exception  as e:
        if (e.args[0] == 404):
            print (e.args[0])
            return False

def buildJournalEntry(entry, ignoreURL):
    journalEntry = ""

    if(TODOCommand in entry):
        journalEntry = config.defaultIndentLevel + " TODO " + utils.getCurrentTime() + " " + entry.replace(TODOCommand,'')
    else:
        journalEntry = config.defaultIndentLevel + " " + utils.getCurrentTime() + " " + entry
    
    if(not(ignoreURL)):
        print(entry)
        journalEntryURL = utils.containsYTURL(entry)
        print (journalEntryURL)
        if(journalEntryURL):
            #title = getWebPageTitle(journalEntryURL)
            journalEntry = journalEntry.replace(journalEntryURL, '{{youtube ' + journalEntryURL +'}}')
        else:
            journalEntryURL = utils.containsURL(entry)
            if(journalEntryURL):
                title = utils.getWebPageTitle(journalEntryURL)
                journalEntry = journalEntry.replace(journalEntryURL, '#' + config.BookmarkTag + ' [' + title + '](' + journalEntryURL + ')')
            
    print (journalEntry)
    return journalEntry

def updateAsset(data, fileType):
    print('u')
    path = assetsFolder + "/" + utils.getTimestamp(True) + "." + fileType
    print(config.getAssetsDestination())
    if(config.getAssetsDestination() == 'github'):
        update = False
        if(GitFileExists(path)):
            update = True
        push(path, git_messages['COMMIT_MESSAGE'].format(BotName, utils.getTimestamp()) , data, GitHubBranch, update=update)
        path = ("![](./" + path + ")")
    elif(config.getAssetsDestination() == 'firebase'):
        path = ("![](" + utils.UploadToFirebase(data, path) + ")")
    
    return path

def getGitFileContent(file, fetchContent = False):
    if (fetchContent):
        file = repo.get_contents(file, ref=GitHubBranch)  # Get file from Branch
    # print(file.decoded_content.decode("utf-8"))
    return file.decoded_content.decode("utf-8")  # Get raw string data

def scanGit4Flashcards(path=""):
    contents = repo.get_contents(path)
    flashcardsList = []
    #print (contents)

    while contents:
        content = contents.pop(0)
        # print(content.url)
        if '/assets/' not in content.url: #TODO change to assetsfolder
            if content.type == "dir":
                contents.extend(repo.get_contents(content.path))
            else:
                #pass
                #file = content
                flashcardsList += flashcards.scan4Flashcards( getGitFileContent(content) ) 
    return(flashcardsList)

def updateFlashCards():
    return flashcards.saveFlashcardsDB( scanGit4Flashcards() )

def Git2Json(path=""):
    AllFilesContent = []
    contents = repo.get_contents(path)

    while contents:
        content = contents.pop(0)

        if '/assets/' not in content.url:
            if content.type == "dir":
                contents.extend(repo.get_contents(content.path))
            else:
                AllFilesContent.append(getGitFileContent(content))
    utils.saveasJson(AllFilesContent,"GitDump.json")
