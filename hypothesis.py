import requests
# add / to the uri to make exclude sub pages
from config import hypothesisToken, hypothesisUsername, defaultIndentLevel, isManageHypothesis
from utils import getWebPageTitle
from itertools import groupby

defaultIndentLevel = defaultIndentLevel + " "
  
def byURI(data):
    return data['uri']

def getHypothesisAnnotations(targetURI):

    headers = {"Authorization": "Bearer " + hypothesisToken}
    # targetURI = "https://web.hypothes.is"
    endpoint = "https://api.hypothes.is/api/search?url=" + targetURI + "&limit=200&order=asc&user=acct:" + hypothesisUsername

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
        #print(row)
        outText += defaultIndentLevel + "[" + getWebPageTitle(row) + "](" + row + ")" + "\n"
        #print(title)
#        print((groupedByURI[row][0]['target'][0]['selector'][2]['exact']).strip())
        for i in range(len(groupedByURI[row])):
            outText += "#" + defaultIndentLevel + (groupedByURI[row][i]['target'][0]['selector'][2]['exact']).strip() + "\n"

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

#uri = "https://stackoverflow.com/questions/4776924/how-to-safely-get-the-file-extension-from-a-url/21836410"
#getHypothesisAnnotations(uri)