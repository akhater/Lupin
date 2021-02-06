from datetime import datetime
from config import hour24

dateTimeObj = datetime.now()

def getJournalPath():
  return "journals/" + dateTimeObj.strftime("%Y_%m_%d") + ".md"

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

