from datetime import datetime
import re
from config import ( hour24, journalsFilesFormat, journalsFilesExtension, journalsFolder, 
                    journalsPrefix,getFirebaseBucketName, getlastNewsDisplayed, setlastNewsDisplayed
                  )
import requests
import hashlib
from os.path import basename

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
  #https://firebasestorage.googleapis.com/v0/b/monolith-6154f.appspot.com/o/shareX%2F$filename$
  APIRUI = 'https://firebasestorage.googleapis.com/v0/b/' + getFirebaseBucketName() + "/o/" + path.replace('/', '%2F') 
  
  headers = {"Content-Type": "img/jpg"}

  result = requests.post(APIRUI, 
                        headers=headers, 
                        data=data)
  #print (APIRUI + "?alt=media&token=" + result.json()['downloadTokens'])
  # https://firebasestorage.googleapis.com/v0/b/monolith-6154f.appspot.com/o/assets%2F202102091338.jpg?alt=media&token=95ace281-fa00-42f8-837a-8f80e6bc4ca9
  return (APIRUI + "?alt=media&token=" + result.json()['downloadTokens'])

def getlatestNews():
  url = 'https://github.com/akhater/Lupin/raw/master/news.json'

  newslist = (requests.get(url)).json()
  lastNewsDisplayed = getlastNewsDisplayed()
  # print (newslist['news'][0]['news'])
  recentNews = []
  for news in newslist['news']:
    # print(news)
    if(news['newsid'] > int(lastNewsDisplayed)):
      recentNews.append(news['news'])
  print(newslist['news'][len(newslist)-1]['newsid'])
  setlastNewsDisplayed(newslist['news'][len(newslist)-1]['newsid'])
  # print (recentNews)
  return recentNews

