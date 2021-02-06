from datetime import datetime
from config import hour24, journalsFilesFormat, journalsFilesExtension

dateTimeObj = datetime.now()

def getJournalPath():
  return "journals/" + dateTimeObj.strftime(journalsFilesFormat) + journalsFilesExtension

def getCurrentTime():
  if(hour24 == "true"):
    return dateTimeObj.strftime("%H:%M") 
  else:
    return dateTimeObj.strftime("%I:%M %p")

def getTimestamp():
  if(hour24 == "true"):
    return dateTimeObj.strftime("%Y-%m-%d %H:%M") 
  else:
    return dateTimeObj.strftime("%Y-%m-%d %I:%M %p")

