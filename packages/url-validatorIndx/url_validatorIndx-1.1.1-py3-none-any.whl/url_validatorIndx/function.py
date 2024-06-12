import json 
import re
def isValidUrl (OOO00OO0OOO000000 ):
    O00O0OOOO0OO00O0O =f"""{OOO00OO0OOO000000}"""
    O0O0O0OOO0O000O00 =r"((((https?|ftps?|gopher|telnet|nntp)://))(?:www\.)?([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
    O0OOOO000OO00O000 ="gm"
    O000000000OO0OOOO =re .compile (O0O0O0OOO0O000O00 ,sum (getattr (re ,O0O00O0OOO00OO0OO .upper ())for O0O00O0OOO00OO0OO in O0OOOO000OO00O000 if O0O00O0OOO00OO0OO in "imsluxa"))
    OOOO0O00O00OOOOOO =O000000000OO0OOOO .findall (O00O0OOOO0OO00O0O )
    if len (OOOO0O00O00OOOOOO ):
        O000000000OO0OOOO ="^((?!-)[A-Za-z0-9-]"+"{1,63}(?<!-)\\.)"+"+[A-Za-z]{2,6}"
        OO0O0O000OOO00OOO =O00O0OOOO0OO00O0O .partition ('://')
        OOOOOO00OOOO0OOOO =re .compile (O000000000OO0OOOO )
        if (re .search (OOOOOO00OOOO0OOOO ,OO0O0O000OOO00OOO [2 ])):
            return {"isValid":True ,"message":"Valid expression"}
        else :
            return {"isValid":False ,"message":"Invalid expression"}
    return {"isValid":False ,"message":"https: missing"}
def isValidString (OOOO0O00000O00O00 ):
    O00O00000OO0O0OO0 =f"""{OOOO0O00000O00O00}"""
    if len (O00O00000OO0O0OO0 )< 255 :
        OO000OO000OO0O0OO =r"^[0-9a-zA-Z]+((?:\s*,)?\s*[0-9a-zA-Z]+)*$"
        O0OO000OO0OO0OOOO ="gm"
        OO000OO000OO0O0OO =re .compile (OO000OO000OO0O0OO ,sum (getattr (re ,OO0O0000OO0O0OOO0 .upper ())for OO0O0000OO0O0OOO0 in O0OO000OO0OO0OOOO if OO0O0000OO0O0OOO0 in "imsluxa"))
        if (re .search (OO000OO000OO0O0OO ,O00O00000OO0O0OO0 )):
            return {"isValid":True ,"message":"Valid Expression"}
        else :
            return {"isValid":False ,"message":"Invalid expression"}
    return {"isValid":False ,"message":"Length of string exceeds 255 chars"}