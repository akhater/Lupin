import json
import urllib
import requests

newslist = {}
newslist['news'] = []
newslist['news'].append({
    'newsid': 1,
    'date': '2020-02-11',
    'news': 'Verion 2.0.0 alpha updates\nLupin now supports Time Spaced Repetition based on SM2 algorithm!!\n Import your flashcards directly \
from your github by running /tsr import ... you can then go over your pending flashcards using /tsr x where \
x is the number of cards you\'d like to see. If you don\'t specify x the value set in your config.ini will be used.\
\nAlso Lupin can now pull these news updates after each significatif update. This will keep you posted about the latest news.\n\n \
This version requires new values in your config.ini file'
})

newslist['news'].append({
    'newsid': 2,
    'date': '2020-02-15',
    'news': 'Verion 3.0.0 experimental updates\n \
A new version upgrade introducing MinMap capabilties among other thing. \
Send /getMM pageTitle and Lupin will generate a Markmap file containing a mindmap of that page and send it to you. \nCredits to https://markmap.js.org/\n \
/tsr command is now renamed to /srs'
})

with open('news.json', 'w') as outfile:
    json.dump(newslist, outfile)
