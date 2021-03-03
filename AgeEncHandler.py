from age.cli import decrypt, encrypt
import io
import os
import sys

import config, utils

def ageDecrypt(content):
    fname = os.path.expanduser("~/.config/age/" + utils.getTimestamp(True, True) + ".txt")

    content = content.encode('utf-8')  

    f = open(fname, 'wb')
    decrypt(infile=io.BytesIO(content),outfile=f,ascii_armored=True)

    f = open(fname, 'r')
    out = f.read()
    f.close()
    os.remove(fname)
    return(out)


def ageEncrypt(content):
    fname = os.path.expanduser("~/.config/age/" + utils.getTimestamp(True, True) + ".txt")

    f = open(fname, 'wb')

    encrypt(recipients=[config.getAgePublicKey()], infile=io.BytesIO(content.encode('utf-8')), outfile=f,ascii_armored=True)

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



# encContent = """-----BEGIN AGE ENCRYPTED FILE-----
# YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSA1eWx4L2lHcXp6VEowWi9S
# VjdSWnJlbzNkK0JwTVEzQU9UcndTKzdnVGw4Cll1MjJEczhJNGpTWWJBZWRKeEdm
# VXlOL2J6WElRbmtkUE9ING9FUXRsQTgKLT4gZ1FdODdTMi1ncmVhc2UgTS0ofmM+
# ICZCPVMgRzNtJnlOIC5pSD11ClRKM1ZwRHRaeHNDR0Qwa0pKU0hmdElkWUlpSFdw
# dzZOSGQ4U2xQM29JaDVpR3ZJS3IzYUdjUW5HdHh6TVV3Mm8KRmUxS2tCbHEzMWw4
# V1NTNWZQSUczSTRXT293Ci0tLSB0dGhjR1Z4SnFCbXdLSEdZTXBsUTc3WDFlMVpX
# a3QvQ0h1WkphU3ZsSnhRCo57XUKTWVOgacwUNCN81+T4nUKzLMwddOXYpvpa1QwI
# SgimgEyvpVSBt06F6iQq34yc+4HgH40nrJr+v/V7zZE=
# -----END AGE ENCRYPTED FILE-----"""

# if isAgeEncrypted(encContent) == 1:
#     print(ageDecrypt(convertToAgeString(encContent)))
# elif isAgeEncrypted(encContent) == 2:
#     print(ageDecrypt(encContent))

# CLEARTEXT = "Hello World!"

# print(ageDecrypt(ageEncrypt(CLEARTEXT)))