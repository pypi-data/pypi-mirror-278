import json #line:1:import json
import re #line:2:import re

def isValidUrl (OO0OOO00O0000OOOO ):
    O0O00OO0OO0OO00OO =f"""{OO0OOO00O0000OOOO}"""
    OO0O0OOO0O0000O00 =r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
    O0000O0O00OOO0000 ="gm"
    OO0OO0000O0OO0OOO =re .compile (OO0O0OOO0O0000O00 ,sum (getattr (re ,OO000OO0O00000000 .upper ())for OO000OO0O00000000 in O0000O0O00OOO0000 if OO000OO0O00000000 in "imsluxa"))
    O0O0OOO00O00OO000 =OO0OO0000O0OO0OOO .findall (O0O00OO0OO0OO00OO )
    if len (O0O0OOO00O00OO000 ):
        OO0OO0000O0OO0OOO ="^((?!-)[A-Za-z0-9-]"+"{1,63}(?<!-)\\.)"+"+[A-Za-z]{2,6}"
        O0OO00O0000O000O0 =O0O00OO0OO0OO00OO .partition ('://')
        OOOOO0O000O00O0O0 =re .compile (OO0OO0000O0OO0OOO )
        if (re .search (OOOOO0O000O00O0O0 ,O0OO00O0000O000O0 [2 ])):
            return True 
        else :
            return False 
    return False 