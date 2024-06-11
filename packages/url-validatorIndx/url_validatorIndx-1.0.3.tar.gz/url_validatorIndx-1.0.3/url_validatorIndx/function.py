import json
import re

def greet():
    return "Hello World"

def createEnv():
    L = ["SAVE_FILE_INFO=https://api.centraluds.blattnertech.com/db/save/fileinfo \n", 
        "DB_HOST=34.129.216.255 \n", 
        "DB_PORT=5432 \n",
        "DB_USER=DataPullUser \n",
        "DB_PASSWORD=ST&cm5RK7KZ7by \n",
        "DB_NAME=UDS \n",
        "DB_SCHEMA=datapuller \n",
        "DB_TABLE=vector_store \n",
        "GATEWAY_ORIGIN=https://api.centraluds.blattnertech.com/ \n",
        "PORT=5000 \n"
         ]

    # Write the string to a .env file
    with open(".env", "w") as f:
    # f.write(json_string)
     f.writelines(L)


def isValidUrl(url):
    txt = f"""{url}"""
    pattern = r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
    flag_string = "gm"
    regex = re.compile(pattern, sum(getattr(re, flag.upper()) for flag in flag_string if flag in "imsluxa"))
    matches = regex.findall(txt)

    if len(matches):
        regex = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
        
        # Compile the ReGex
        httpVar = txt.partition('://')
        p = re.compile(regex)
        if(re.search(p, httpVar[2])):
            return True
        else:
            return False
    return False     