import requests
# add / to the uri to make exclude sub pages
from config import hypothesisToken, hypothesisUsername, defaultIndentLevel
from utils import getPageTitle
from collections import OrderedDict
from itertools import groupby

defaultIndentLevel = defaultIndentLevel + " "
  
def byURI(data):
    return data['uri']

def getHypothesisAnnotations(targetURI):

    headers = {"Authorization": "Bearer " + hypothesisToken}
    # targetURI = "https://web.hypothes.is"
    endpoint = "https://api.hypothes.is/api/search?url=" + targetURI + "&limit=200&user=acct:" + hypothesisUsername

    #print(endpoint)
    r = requests.get(endpoint, headers=headers).json()

    # headers = {"Authorization": "Bearer " + hypothesisToken}
    # targetURI = "https://web.hypothes.is"
    # endpoint = "https://api.hypothes.is/api/search?url=" + targetURI + "&limit=200&user=acct:" + hypothesisUsername

    grouped_byURI = groupby(sorted(r['rows'], key=byURI), byURI)

    groupedByURI = {}

    for k, v in grouped_byURI:
        groupedByURI[k] = list(v)
    
    # Title r['https://web.hypothes.is/'][0]['document']['title']
    # Highlighted r['https://web.hypothes.is/'][0]['target'][0]['selector'][2]['exact']
    # annotation r['https://web.hypothes.is/'][0]['text']
    # tags   r['https://web.hypothes.is/'][0]['tags']

    #print(groupedByURI)
    outText = ""
    for row in groupedByURI:
        outText += defaultIndentLevel + "[" + getPageTitle(row) + "](" + row + ")" + "\n"
        #print(title)
        for i in range(len(groupedByURI[row])):
            outText += "#" + defaultIndentLevel + groupedByURI[row][i]['target'][0]['selector'][2]['exact'] + "\n"

            if  groupedByURI[row][i]['text']:
                annotation =  groupedByURI[row][i]['text'] + "\n"
            else:
                annotation = ""
            
            tags = ""
            for tag in groupedByURI[row][i]['tags']:
                tags += "#" + tag + " "
            
            if annotation:
                outText += "##" + defaultIndentLevel + annotation 
   
            if tags:
                tags += "\n"
                
                if annotation:
                    outText += "###" + defaultIndentLevel + tags
                else:
                    outText += "##" + defaultIndentLevel + tags
    
    #print(outText)
    return outText

#print(getHypothesisAnnotations("https://web.hypothes.is"))