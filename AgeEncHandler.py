from age.cli import decrypt, encrypt
import io
import os
import sys

import config, utils

# content = """---
# title: mindmap1
# ---

# ## 1
# ### 1.1
# #### 1.1a
# ### 1.2
# ## 2
# ### 2.1
# #### 2.1a
# ### 2.2"""

# encContent="""-----BEGIN AGE ENCRYPTED FILE----- YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBNckphc3VwK2NJTFczSFN2 M3c3SGZBNEphUGh4VUxBaUlTTUdMbTMxSHpJCmJEcy9MbG5UOG1kd0pTQ3VWaS9U VHI4bjNsMnR4eFY5RUZ3K0hKSnRMMzAKLT4gelIrdmI1X2stZ3JlYXNlIHEgbGd9 QkZ9SCBOK2MvfD8KditUWDRIOWZWVFBQZUhlbllOZFczVnd2WnRHOVhST2VsTERw cm5aNFdPZVJFTWtyMnBsNnhyWG5GMldOUExYcwoxTEZGRzFRTTdyTFlESWM2RExx eQotLS0gYzNHWGZISlExakZRSFBGWnBaSWlXWkZESVhaMWNCOTNwYnJDaVJuOHM0 bwo0Tonxe3w8YYPqYd/fge6J6qP8K83ioNFtj1smqXkiVVJq8tNHBV3lmcVBEB8j BakmY3PEARc+PI6bn2vgVITBTZQ/UkH7T5+isnauZe0WpdrlGj7qBT0AVXpUzV+Z u33tTdwyYhLkeEEE -----END AGE ENCRYPTED FILE-----"""


def ageDecrypt(content):
    fname = os.path.expanduser("~/.config/age/" + utils.getTimestamp(True) + ".txt")

    content = content.encode('utf-8')  

    old_stdout = sys.stdout

    sys.stdout = open(fname, 'w')

    decrypt(infile=io.BytesIO(content),ascii_armored=True)

    sys.stdout = old_stdout
    
    f = open(fname, 'r')
    out = f.read()
    f.close()
    os.remove(fname)
    return(out)


def ageEncrypt(content):
    fname = os.path.expanduser("~/.config/age/" + utils.getTimestamp(True) + ".txt")

    content = content.encode('utf-8')  
    old_stdout = sys.stdout

    sys.stdout = open(fname, 'w')

    encrypt(recipients=[config.getAgePublicKey()], infile=io.BytesIO(content),ascii_armored=True)

    sys.stdout = old_stdout

    f = open(fname, 'r')
    out = f.read()
    f.close()
    os.remove(fname)
    return(out)

def isAgeEncrypted(content):
    if content.startswith("-----BEGIN AGE ENCRYPTED FILE----- "):
        return 1
    elif content.startswith("-----BEGIN AGE ENCRYPTED FILE-----\n"):
        return 2
    else:
        return 0

def convertToAgeString(content):
    s = "-----BEGIN AGE ENCRYPTED FILE-----\n"
    s += '\n'.join(content.split("FILE----- ")[1].split(" -----END")[0].split(' '))
    s += "\n-----END AGE ENCRYPTED FILE-----"
    return s



# encContent="""-----BEGIN AGE ENCRYPTED FILE----- YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBscmd3UlAwZGdkLzVTcXAr NklQNHdMWW82TmxFLzNRWFJvRVlHS0JqMHhRClQzdTNpTGhqNnVXMFAzOE1LT1d1 alpXRlcvSWhhblV1UjM0eHVNVXlJekEKLT4gXidFKlwtZ3JlYXNlIHJUWDRwUFgg WC8scQpTMWdocldUUysxK202K1JTbVFBYk1vYXVqZkN4NzJpUXFIZGlXZ3Y2b3FV TkkzVklZUi9XejNPOWFibXN1Yi81CjJ5UHphd1FkNDhmU2ZqQjBqOXk5ME5uYk4v YUQrcTNDS2J3Ci0tLSBITU1nMHU3eExnV3QxM1pYbFpmT0ZXdU5pRldTdHZWMXc1 cDkwemlpTTRVCgsAcjgnhukeR2hMZbIY6B9RAy/BQ091Q1eZr3ucyIrI1bnI3wDw R9l+sHYZrNYvUhBviGM1mfXUYjcfenviclFaSmA0duoRpvajUKxQCZF8Xz44gjW/ Elp37mh4sYTJYDBQ8Ad9XqhxYNFmaIX+44b7DsK7slTrfzxF3cW/fw== -----END AGE ENCRYPTED FILE-----"""
# encContent="""-----BEGIN AGE ENCRYPTED FILE-----\nYWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBscmd3UlAwZGdkLzVTcXAr\nNklQNHdMWW82TmxFLzNRWFJvRVlHS0JqMHhRClQzdTNpTGhqNnVXMFAzOE1LT1d1\nalpXRlcvSWhhblV1UjM0eHVNVXlJekEKLT4gXidFKlwtZ3JlYXNlIHJUWDRwUFgg\nWC8scQpTMWdocldUUysxK202K1JTbVFBYk1vYXVqZkN4NzJpUXFIZGlXZ3Y2b3FV\nTkkzVklZUi9XejNPOWFibXN1Yi81CjJ5UHphd1FkNDhmU2ZqQjBqOXk5ME5uYk4v\nYUQrcTNDS2J3Ci0tLSBITU1nMHU3eExnV3QxM1pYbFpmT0ZXdU5pRldTdHZWMXc1\ncDkwemlpTTRVCgsAcjgnhukeR2hMZbIY6B9RAy/BQ091Q1eZr3ucyIrI1bnI3wDw\nR9l+sHYZrNYvUhBviGM1mfXUYjcfenviclFaSmA0duoRpvajUKxQCZF8Xz44gjW/\nElp37mh4sYTJYDBQ8Ad9XqhxYNFmaIX+44b7DsK7slTrfzxF3cW/fw==\n-----END AGE ENCRYPTED FILE-----\n"""
# if isAgeEncrypted(encContent) == 1:
#     print(ageDecrypt(convertToAgeString(encContent)))
# elif isAgeEncrypted(encContent) == 2:
#     print(ageDecrypt(encContent))

# PLAIN="""---
# title: 2021_02_22
# alias: 
# ---

# ## #bookmark [Mindmap terminal error · Issue #7 · akhater/Lupin · GitHub](https://github.com/akhater/Lupin/issues/7)
# """
# print(ageDecrypt(ageEncrypt(PLAIN)))