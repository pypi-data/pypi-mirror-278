import re 

def isValidUrl (O0OOOO000O0OOOOO0 ):
    OO0OOOO000OO0OOO0 =f"""{O0OOOO000O0OOOOO0}"""
    O0O000O0OOO0000O0 =r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
    OO000OO000OO0OOO0 ="gm"
    OOOO0O0O00OOO000O =re .compile (O0O000O0OOO0000O0 ,sum (getattr (re ,OO0OO0OOOOOO0OOO0 .upper ())for OO0OO0OOOOOO0OOO0 in OO000OO000OO0OOO0 if OO0OO0OOOOOO0OOO0 in "imsluxa"))
    OO0O00OO0000OOO00 =OOOO0O0O00OOO000O .findall (OO0OOOO000OO0OOO0 )
    if len (OO0O00OO0000OOO00 ):
        OOOO0O0O00OOO000O ="^((?!-)[A-Za-z0-9-]"+"{1,63}(?<!-)\\.)"+"+[A-Za-z]{2,6}"
        O0O0000OOO00OOOOO =OO0OOOO000OO0OOO0 .partition ('://')
        OOOOO0O0O0OOO0O00 =re .compile (OOOO0O0O00OOO000O )
        if (re .search (OOOOO0O0O0OOO0O00 ,O0O0000OOO00OOOOO [2 ])):
            return True 
        else :
            return False
    return False 