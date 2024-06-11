
from loguru import logger
from typing import List

TOKEN_CUT={
        ("alphanum", "alphanum") :  False, # word
        ("alphanum", "space") :  True ,# end of word
        ("alphanum", "dot"  ) :  False  ,# dotsep
        ("alphanum", "other") :  True ,# end of word

        
        ("space", "alphanum") : True, # word
        ("space", "space") : None  ,# end of word
        ("space", "dot"  ) : True ,# number
        ("space", "other") : True  ,# end of word
        
        ("dot", "alphanum") : False ,# word
        ("dot", "space") : True  ,# end of word
        ("dot", "dot")   : False ,# number
        ("dot", "other") : True  ,# end of word

        ("other", "alphanum") : True, # word
        ("other", "space") : True,# end of word
        ("other", "dot"  ) : True,# number
        ("other", "other") : True,# end of word 
    }    

META_CHARS = {
    ".eq.":  "\xaa",     #comparison
    ".neq.":  "\xab",
    ".ge.":  "\xac",
    ".gt.":  "\xad",
    ".le.":  "\xae",
    ".lt.":  "\xaf",
    
    ".and.": "\xba",     # logic
    ".or.":  "\xbb",
    
    "//":  "\xca",   # markers
    "/*":  "\xcb",   
    "*/":  "\xcc",   
    "::":  "\xcd",
    "||":  "\xce",
    "&&":  "\xcf",
    

    "+=":  "\xda",   # operands
    "-=":  "\xdb",   
    "/=":  "\xdc",   
    "*=":  "\xdd",
    "**":  "\xde",
    "==":  "\xdf",

    ">=":  "\xea",   # operands
    "<=":  "\xeb",   
    
}

META_CHARS_REV = {value:key for key,value in META_CHARS.items()}

STRING_START = "\xfa"
STRING_STOP = "\xfb"
STRING_SUB = "\xfc"

STR_SUBSTITUTE = {
    "\xfa":'"',
    "\xfb":'"',
    "\xfc":"'",
}
    

def string_encode(line:str)->str:
    string_type=""
    new_line=""
    for char in line:
        if char in ["'", '"']:
            if string_type == "":              #<- Enter string
                new_line+=STRING_START
                string_type=char
            else:  # in a string
                if char == string_type:
                    new_line+=STRING_STOP
                    string_type=""
                else:
                    new_line+=STRING_SUB
        else:
            new_line+=char 
    assert len(new_line) == len(line)
    return new_line

def string_decode(line:str)->str:
    new_line=""
    for char in line:
        new_line+=STR_SUBSTITUTE.get(char,char)  
    return new_line


def metachar_encode(line:str)->str:
    for char, proxy in META_CHARS.items():
        line = line.replace(char,proxy)
    return string_encode(line)

def metachar_decode(line:str)->str:
    for char, proxy in META_CHARS.items():
        line = line.replace(proxy,char)
    return string_decode(line)

def metachar_decode_from_list(list_:str)->List:
    #logger.critical(list_)
    list_ = [  META_CHARS_REV.get(item, item) for item in list_]
    #logger.critical(list_)
    list_ = [  string_decode(item) for item in list_]
    #logger.critical(list_)
    return list_
   


def iterate_with_neighbors(iterable_):
    # Create iterators for the current and previous characters
    prev = None  # Initialize previous character to None
    for curr in iterable_:
        # Yield the previous and current characters
        yield prev, curr    
        prev = curr
    yield prev, None



def tokenize(line:str) -> List[str]:
    """
    Light tokenizer to ease code identification
    """
    def _cast(char):
        if char == " ":
            return "space"
        if char in [".", "_", "%"]:
            return "dot"
        if char in META_CHARS_REV.keys():
            return "other"
        if char.isalnum():
            return "alphanum"
        return "other"
        
    tokens=[]
    buffer=""
    prev_cast = "other"
    instring=False
    for curr_char in metachar_encode(line):

            
            

        cur_cast = _cast(curr_char)
        to_cut = TOKEN_CUT[prev_cast,cur_cast]
        
        # string override; a string is a single token
        if curr_char == STRING_START:
            instring=True
            if buffer.strip() != "":
                tokens.append(buffer)
            buffer=""
        if curr_char == STRING_STOP:
            if buffer.strip() != "":
                buffer+=curr_char
                tokens.append(buffer)
            buffer=""
            instring=False
            continue
        
        if instring:
            buffer+= curr_char 
            continue
        # string override; a string is a single token
        

        if to_cut is None:
            continue
        elif to_cut is True:
            if buffer.strip() != "":
                tokens.append(buffer)
            buffer=curr_char
        else:
            buffer+= curr_char

        prev_cast = cur_cast
    
    if buffer.strip() != "":
        tokens.append(buffer)
        
    return metachar_decode_from_list(tokens)
        



def find_words_before_left_parenthesis_noregexp(line: str) -> List[str]:
    """Find all words before a left parenthesis in a line"""
    if "(" not in line:
        return []
    matches =[]
    for prev, curr  in iterate_with_neighbors(tokenize(line)):
        if curr == "(":
            try:
                if prev not in ",+-/*<>=;|(){}[]:&!~ ":
                    matches.append(prev)
            except TypeError:
                pass #triggered by prev == None
        
    clean_matches = sorted(set(matches))

    black_list = list(META_CHARS.keys()) + ["!"]
    # remove meta chars , whit ar not words...
    clean_matches = [ item for item in clean_matches if item not in black_list]

    return clean_matches

def get_indent(line:str)->str:
    """Get the indentation leading a line"""
    _indent=""
    for char in line:
        if char == "\t":
            _indent+="    "
        elif char != " ":
            return _indent
        else:
            _indent+=" "
    return _indent

def eat_spaces(code:List[str])->List[str]:
    """Remove unwanted multiple spacing """
    new_stmt = []
    for line in code:
        out=get_indent(line)
        
        prevchar=None    
        for i,char in enumerate(line.strip()):
            try:
                next_char=line.strip()[i+1]
            except IndexError:
                next_char=None
            
            if char == " ":
                if prevchar not in [" ",":",";",","] and next_char not in [":",";",","] :
                    out+=char
                else:
                    pass # no space needed if " " precedes, or a punctuation is before or after
            else:
                out+=char

            prevchar=char
        new_stmt.append(out)  
    return new_stmt
