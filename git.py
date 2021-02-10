from github import Github, InputGitAuthor
from pprint import pprint
import json

import config
from utils import (
    getJournalPath, getCurrentTime, getTimestamp, containsURL, getWebPageTitle, 
    containsYTURL, getPageTitle, UploadToFirebase
)
from dictionaries import git_messages

#file_path = utils.getJournalPath()

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
     
def updateJournal(entry, needsBuilding = True, path=getJournalPath(), overwrite=False, alias='', ignoreURL=False):
    if needsBuilding:
        entry = buildJournalEntry(entry, ignoreURL)
    if(GitFileExists(path)):
        file = repo.get_contents(path, ref=GitHubBranch)  # Get file from Branch
        if(overwrite):
            #print(getPageTitle(path))
            data = "---\ntitle: " + getPageTitle(path) + "\nalias: " + alias + "\n---\n\n"
            #print(data)
        else:
            data = file.decoded_content.decode("utf-8")  # Get raw string data
        
        data += (entry).strip() + "\n"

        push(path, git_messages['COMMIT_MESSAGE'].format(BotName, getTimestamp()) , data, GitHubBranch, update=True)
    else:
        data =  "---\ntitle: " + getPageTitle(path) + "\nalias: " + alias + "\n---\n\n" + (entry).strip() + "\n"
        
        push(path, git_messages['COMMIT_MESSAGE'].format(BotName, getTimestamp()) , data, GitHubBranch, update=False)

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
        journalEntry = config.defaultIndentLevel + " TODO " + getCurrentTime() + " " + entry.replace(TODOCommand,'')
    else:
        journalEntry = config.defaultIndentLevel + " " + getCurrentTime() + " " + entry
    
    if(not(ignoreURL)):
        print(entry)
        journalEntryURL = containsYTURL(entry)
        print (journalEntryURL)
        if(journalEntryURL):
            #title = getWebPageTitle(journalEntryURL)
            journalEntry = journalEntry.replace(journalEntryURL, '{{youtube ' + journalEntryURL +'}}')
        else:
            journalEntryURL = containsURL(entry)
            if(journalEntryURL):
                title = getWebPageTitle(journalEntryURL)
                journalEntry = journalEntry.replace(journalEntryURL, '#' + config.BookmarkTag + ' [' + title + '](' + journalEntryURL + ')')
            
    print (journalEntry)
    return journalEntry

def updateAsset(data, fileType):
    print('u')
    path = assetsFolder + "/" + getTimestamp(True) + "." + fileType
    print(config.getAssetsDestination())
    if(config.getAssetsDestination() == 'github'):
        update = False
        if(GitFileExists(path)):
            update = True
        push(path, git_messages['COMMIT_MESSAGE'].format(BotName, getTimestamp()) , data, GitHubBranch, update=update)
        path = ("![](./" + path + ")")
    elif(config.getAssetsDestination() == 'firebase'):
        path = ("![](" + UploadToFirebase(data, path) + ")")
    
    return path

def a(path):
    # contents = repo.get_contents(path, ref=GitHubBranch) 
    # cont = contents.decoded_content.decode()
    cont = "---\ntitle: Feb 9th, 2021\n---\n\n## #flashcard \n### question 1 \n#### some answer \n# ### question 2 \n#### some answer"
    lines = cont.split('\n')
    sparator = '#'
    print(cont)
    for i in range(len(lines) - 1):
        if '#flashcard' in lines[i]:
            print(lines[i])

a("journals/2021_02_09.md")
