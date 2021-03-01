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
    fname = os.path.expanduser("~/.config/age/" + utils.getTimestamp(True, True) + ".txt")

    content = content.encode('utf-8')  

    # old_stdout = sys.stdout

    # sys.stdout = open(fname, 'w')

    # decrypt(infile=io.BytesIO(content),ascii_armored=True)

    # sys.stdout = old_stdout
    f = open(fname, 'wb')
    decrypt(infile=io.BytesIO(content),outfile=f,ascii_armored=True)

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



# encContent = """-----BEGIN AGE ENCRYPTED FILE-----
# YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBUQ0xxRi96NXA1Vnd6aXFB
# MC9SNktqQ2Q1d3BpM0hDdHhqYW1CQXNFeGh3ClBZRVZYZlJaMXlpa1RMVkg1RHNz
# Vk1Xd0xBbSt5cDlEUG11bUZLY0ZZZDQKLS0tIG9VT25iZDN3WVprUjJXQllCcG5C
# dUh2RkdUZWNsVGpHV2lxaDJwTDFmb3MKdANQTPytONgfuHB2Pmqd6R1AlEUh2ZgB
# I0AQsILPcWZaB1zgCDlKxUhcGZuvbOpmSjHKVxiCdgZ4VmQW0cCYNGUtCO6irnKD
# e3t7izZ0fZVrgI+zTiSpClbfJNAQYDx9JVJnyDjMeT8+WqMZp4jWzClcjRguu1uQ
# lrW7SpaGF6Ny1rkSRHY+8OIy2Kkrdx4BF6SFwDlP6w6zuAjYcwvcf2modPQDSDY7
# zkUgArC8jjHF62/F7aWn7UVUx2+vEsfJRlYhFdt0k0ykCi/aA4dt8mmyO1bl3dkp
# YsdovHSnrJyTiDh6OW2YKljX2jfNGw9YOquEKmbpRPqbmjVZPc/BjH1IlzUTFt41
# MRrL56ySj+4Owyml29esk3VydfbmqLgE9NNW+ntjOCdOsKZqC6YlXlnyZtKHQ6vu
# L95l4xYZfN+KOvjVOagiTdzjS9YFde+jSGcIQJcIII2NgCdnIT8zw4XGv245NEsK
# 5duagx3onwt3XOtW4ljGTgJw9cHQ6MisW+qdLe3Pl2MhkuqmKQXVbdqnmbqz8yG1
# rWWmmIguI0qj1NwhrL8L3/33Z2zf93V9OiT+E/dUxdiiLZd5qHn9DhtImqvuSkMS
# BUGQ9i8FSJK3fRBBUAnHAWLuqtwr1W92jNDZB1KQknCy1AWOZimRmmgm82w/pYy9
# G0nKLOiK9UgNWCE8co0h4uwhq4jdBautEbywc0/yDmV3dg/AwpAldfECVux9oqTj
# DVC4X0KHTFtTP6DRD5kjj+fXXpB3pPilWdXdt1I7Po2g/DrUbjmk8XMHY1ui0khT
# rEczBiWjeArT3/KHVgTz5uL5TwiWqoADzscyC/lXSPaDJuoHNtP7MkgscGxA6g9e
# 8W5uCHwWmE6w0CBJxIvZMmD6gwwZU5Avl21a8y17tjOCoIh3NXRItzcD1652280i
# mXoAwGUDnQ9Q+yetPQ46F/iibntAgNnpcpeWev2VYlsQrWOoZepL16zMYwFOfUtK
# ZdRWZXJ8xXyz3aygi2aBsoYN+lC1wrbdtI9fU/5/IOFMsR+uY6wqXutVMd3eeXfQ
# 2rr3I/QK/D/4Qb73kbWiiol48DHONwm79S+Y725FPqb6ZL+dUqp33G8C8t3owzZI
# dRfcMZRQKds7Ynzf1IIJJViIHkYGEpjokZazZ7VGHBQRMon38CSXclyWziNLLOTX
# ppkI46O3wHoGWfCWuBJlOOb4p5J78B0kg6dwKIv6ZqDliJp23wTxqAOr8LnC8ezO
# ZHTSivezhh6DLW24RtEw1YFc2yijErLQIWwDXVVOgnU49YGJn181DdQkuiuHSGlW
# /yVI4uheICiwmqEsfmK6y2LSJgoDB2BNjo0X
# -----END AGE ENCRYPTED FILE-----"""

# if isAgeEncrypted(encContent) == 1:
#     print(ageDecrypt(convertToAgeString(encContent)))
# elif isAgeEncrypted(encContent) == 2:
#     print(ageDecrypt(encContent))
