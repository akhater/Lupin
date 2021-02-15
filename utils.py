from datetime import datetime
import re
import json
import requests
import hashlib
from os.path import basename

from config import ( hour24, journalsFilesFormat, journalsFilesExtension, journalsFolder, 
                    journalsPrefix,getFirebaseBucketName, getlastNewsDisplayed, setlastNewsDisplayed
                  )

import flashcards
from mindmap import buildMindmapTree


bootTime = datetime.now()

def getJournalPath():
  dateTimeObj = datetime.now()

  if (journalsPrefix == "none"):
    return journalsFolder + "/" + dateTimeObj.strftime(journalsFilesFormat) + journalsFilesExtension
  else:
    return journalsFolder + "/" + journalsPrefix + dateTimeObj.strftime(journalsFilesFormat) + journalsFilesExtension

def getAnnotationPath(uri):
  return 'annotations/' + getURIHash(uri) + journalsFilesExtension

def getCurrentTime():
  dateTimeObj = datetime.now()

  if(hour24 == "true"):
    return dateTimeObj.strftime("%H:%M") 
  else:
    return dateTimeObj.strftime("%I:%M %p")

def getTimestamp(isoFormat=False):
  dateTimeObj = datetime.now()
  
  if isoFormat:
    return dateTimeObj.strftime("%Y%m%d%H%M") 
  elif (hour24 == "true"):
    return dateTimeObj.strftime("%Y-%m-%d %H:%M") 
  else:
    return dateTimeObj.strftime("%Y-%m-%d %I:%M %p")

def getUptime():
  seconds = date_diff_in_seconds(datetime.now(), bootTime)

  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  days, hours = divmod(hours, 24)
  return (days, hours, minutes, seconds)

def date_diff_in_seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def containsURL(s):
    url = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)
    if url:
      return url.group()
    else:
      return False

def containsRefBlock(s):
  try:
    return (re.search(r"\(\((.*?)\)\)", s)).group(1)
  except:
    return False
  
def getWebPageTitle(url, title_re=re.compile(r'title[^>]*>([^<]+)<\/title>', re.UNICODE )): 
    r = requests.get(url)
    if r.status_code == 200:
        match = title_re.search(r.text)
        if match:
            return match.group(1)
        return Exception("No match for title in page")
    raise Exception(r.status_code)

def containsYTURL(s):
  url = re.search('((?:https?:)?//)?((?:www|m).)?((?:youtube.com|youtu.be))(/(?:[\\w-]+\\?v=|embed/|v/)?)([\\w-]+)(\\S+)?',s)
  if url:
    return url.group()
  else:
    return False

def getMD5Hash(s):
  byte_s = s.encode('utf-8')
  return hashlib.md5(byte_s).hexdigest()

def stripURI(uri):
  regex = re.compile(r"https?://?")
  return regex.sub('', uri).strip().strip('/')

def getURIHash(uri):
  return getMD5Hash(stripURI(uri))

def getPageTitle(path):
  return basename(path).replace(journalsFilesExtension, '')

def UploadToFirebase(data, path):
  APIRUI = 'https://firebasestorage.googleapis.com/v0/b/' + getFirebaseBucketName() + "/o/" + path.replace('/', '%2F') 
  
  headers = {"Content-Type": "img/jpg"}

  result = requests.post(APIRUI, 
                        headers=headers, 
                        data=data)
  return (APIRUI + "?alt=media&token=" + result.json()['downloadTokens'])

def getlatestNews():
  url = 'https://github.com/akhater/Lupin/raw/master/news.json'

  newslist = (requests.get(url)).json()
  lastNewsDisplayed = getlastNewsDisplayed()
  recentNews = []
  for news in newslist['news']:
    # print(news)
    if(news['newsid'] > int(lastNewsDisplayed)):
      recentNews.append(news['news'])
  print(newslist['news'][len(newslist)]['newsid'])
  setlastNewsDisplayed(newslist['news'][len(newslist)]['newsid'])
  return recentNews

def saveasJson(content, file):
    with open(file, 'w') as outfile:
        json.dump(content, outfile)

def findOrigBlock(ref):
    with open('GitDump.json') as json_file:
        AllFilesContent = json.load(json_file)

    origBlock = ""
    for fileContent in AllFilesContent:
        if ":id: " + ref in fileContent.lower() or ":id:" + ref in fileContent.lower(): #add no space after id:
            lines = fileContent.split('\n')
            i = 0
            while i <= len(lines) - 1:
                if ":id: " + ref in lines[i].lower() or ":id:" + ref in lines[i].lower():
                    break
                i += 1
            origLine = lines[i-2]
            origBlock = origLine[origLine.index(' '):].strip()
            break
    return(origBlock)

def scanJson4Flashcards():
  from git import Git2Json 
  Git2Json() 
  with open('GitDump.json') as json_file:
    AllFilesContent = json.load(json_file)

  flashcardsList = []

  for fileContent in AllFilesContent:
    flashcardsList += flashcards.scan4Flashcards( fileContent ) 
  
  return(flashcardsList)

def updateFlashCards():
    return flashcards.saveFlashcardsDB( scanJson4Flashcards() )

def convert2MD(pageTitle):
  from git import Git2Json 
  Git2Json()

  with open('GitDump.json') as json_file:
    AllFilesContent = json.load(json_file)  
 
  for content in AllFilesContent:
    lines = content.split('\n')
    lvl1 = -1

    i = 0
    out = ""
    continueScan = True
    while i <= len(lines) - 1:
      line = lines[i]
      if(line):
        # print(line[0])
        if 'title:' in line.lower() and pageTitle.lower() not in line.lower(): # not correct page
          continueScan = False
        if not continueScan:
          break
        if 'title:' in line.lower() and pageTitle.lower() in line.lower():
          out += "# " + line.replace('title:', '').strip() + "\n"
        elif line[0] == "#":
          outln = ""
          blockRef = containsRefBlock(line)
          if (blockRef):
            origLine = (line[line.index(' '):]).replace("(("+blockRef+"))","").strip()
            if(origLine):
              outln = origLine + " "
            outln +=  findOrigBlock(blockRef)
          else:
            outln = line[line.index(' '):]

          if(lvl1 == -1):
            lvl1 = line.index(' ')
          space = " "
          for _ in range((line.index(' ')-lvl1)* 4):
            space += " "
          out += space + "- " + outln.strip()  + "\n" #+ (line[line.index(' '):]) + '\n' # .replace('#','-') + "\n"
          # print(out)
      i +=1
  return(out)

def convert2Mindmap(pageTitle):
  from git import Git2Json 
  Git2Json()

  with open('GitDump.json') as json_file:
    AllFilesContent = json.load(json_file)  

  for content in AllFilesContent:
    if ('---\ntitle: ' + pageTitle.lower()) in content.lower():    
      return json.dumps(buildMindmapTree(content, pageTitle), default=lambda x: x.__dict__)
      # return json.dumps(buildMindmapTree(content, pageTitle).c[0], default=lambda x: x.__dict__)
    
