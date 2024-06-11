"""
Module that gather the most common functions of unformat
"""

from __future__ import annotations
from typing import Tuple,List
from dataclasses import dataclass
from loguru import logger
import json


from tucan.string_utils import get_indent

CHAR_CMT_START = "\xaa"
CHAR_CMT_STOP = "\xbb"
CHAR_EOL = "\xcc"
CHAR_CMT_EOL = "\xdd"

@dataclass
class Statements():
    stmt:List[str]= None
    lines:List[Tuple[int,int]]= None

    def __str__(self):
        out=""
        for line,(i1,i2) in zip(self.stmt,self.lines):
            out+= f"({i1}-{i2})  {line}\n"
        out += "======================="
        out += f"Statements found : {len(self.stmt)}"
        return out
    
    def to_code(self):
        out=[f"{stmt}" for stmt in self.stmt]
        return out
    
    def to_nob(self):
        return [[st, lsp] for st,lsp in zip(self.stmt, self.lines)]

    def dump_json(self,newfile):
        
        logger.info(f"Data dumped to {newfile}")
        with open(newfile,"w") as fout:
            json.dump(self.to_nob(),fout,indent=2,sort_keys=True)

    def dump_code(self,newfile):
        
        with open(newfile,"w") as fout:
            fout.write("\n".join(self.to_code()))
        print(f"\n\nCleaned version dumped in {newfile}")



def new_stmts(code:List[str])->Statements:
    return Statements(
        code,
        [[i+1,i+1] for i,_ in enumerate(code)]
    )


def remove_strings(code:List[str], string_char:str)->List[str]:
    new_stmt=[]

    for line in code:
        inside_string_context=False
        buffer=""
        tmp_buffer=""
        for char in line:
            if char == string_char:
                if not inside_string_context:
                    inside_string_context=True
                else:
                    buffer+=f"{char}___"
                    inside_string_context=False
                    tmp_buffer=""
                #buffer+=char
            
            if not inside_string_context:
                buffer+=char
            else:
                tmp_buffer+=char

        if inside_string_context: #if the string context is not ended ath the end of the line, put the skipped chars
            buffer+=tmp_buffer

        new_stmt.append(buffer)
    return new_stmt


def rm_parenthesis_content(buffer:str, lchar:str="(", rchar:str=")", greedy=True)->str:
    """Remove the content of parenthesis"""
    lvl=0
    out=""
    for char in buffer:
        if lvl==0:
            out+=char
        if char == lchar:
            lvl+=1
            
        if char == rchar:
            lvl-=1
    
    if greedy:
        out = out.replace( lchar, "")
        out = out.replace( rchar, "")
    return out
        

def clean_blanks(stmts:Statements)->Statements:
    """
    Perform the first pass to strip comments and blank lines.

    Args:
        code (List[str]): List of code lines.

    Returns:
        List[Tuple[str, int]]: List of code lines without comments and blank lines.
    """
    new_stmt=[]
    new_lines=[]
    for line, lines_span in zip(stmts.stmt,stmts.lines):
        if line.strip() == "":  # Blank lines
            continue

        new_stmt.append(line)
        new_lines.append(lines_span)
        
    # Add final newline if missing. Useful to finish cleanly the parsing
    if new_stmt:
        if new_stmt[-1] != "":
            new_stmt.append("")
            last_line=new_lines[-1][0]
            new_lines.append([last_line+1,last_line+1])
        
    return Statements(new_stmt,new_lines)





def clean_inline_comments(stmts:Statements, symbol:str="#")->Statements:
    """
   
    """
    new_stmt=[]
    new_lines=[]
    for line, lines_span in zip(stmts.stmt,stmts.lines):
        
        if symbol in line:
            line=line.split(symbol)[0].rstrip()
            if line.strip()=="":
                continue
        new_stmt.append(line)
        new_lines.append(lines_span)
        
    return Statements(new_stmt,new_lines)

def clean_pure_comments(stmts:Statements, symbol:str="#")->Statements:
    """
   
    """
    new_stmt=[]
    new_lines=[]
    for line, lines_span in zip(stmts.stmt,stmts.lines):
        if line.startswith(symbol):
            continue
        new_stmt.append(line)
        new_lines.append(lines_span)
    return Statements(new_stmt,new_lines)


def split_multi_statement_lines(stmts:Statements)->Statements:
    """Split statements on ;"""
    new_stmt=[]
    new_lines=[]
    for line, (lstart,lend) in zip(stmts.stmt,stmts.lines):
        if ";" not in line:
            new_stmt.append(line)
            new_lines.append([lstart,lend])
        else:
            indent=get_indent(line)
            for stmt in line.split(";"):
                new_stmt.append(indent+stmt.strip())
                new_lines.append([lstart,lend])
    return Statements(new_stmt,new_lines)




def align_multiline_blocks(stmts:Statements, markup_in:str,markup_out:str)->Statements:

    merge_=[]
    i_in=None
    for i,line in enumerate(stmts.stmt):
        if markup_in in line:
            if i_in is not None:
                logger.info(f"Multiple start of continuation block at line {i}")
            i_in = i #mark this line in all cases
        if markup_out in line:
            if i_in == i:
                pass  # no merge required actually
                i_in= None
            elif i_in is not None:
                merge_.append((i_in, i)) #store a merging range
                i_in= None
            else:
                logger.info(f"Spurious end of continuation block at line {i}")
    #logger.critical(merge_)

    new_stmt=stmts.stmt
    new_lines=stmts.lines
    def replace_slice_(lst, start, end, new_item):
        return lst[:start] + [new_item] + lst[end+1:]    
    
    for (i_in_, i_out_) in merge_:
        tmp_line = (stmts.lines[i_in_][0],stmts.lines[i_out_][1])

        tmp_stmt = (
            get_indent(stmts.stmt[i_in_])
            + ' '.join(
                [item.lstrip() for item in stmts.stmt[i_in_:i_out_+1]]
            )
        )
        

        new_stmt = replace_slice_(new_stmt,i_in_, i_out_, tmp_stmt)
        new_lines= replace_slice_(new_lines,i_in_, i_out_, tmp_line)
    
    

    return Statements(new_stmt,new_lines)



def strip_c_comment(line:str, fortran:bool=False)->str:
    """
    Fortran=True :  equivalent to cpp --traditional
    """
    cline=""
    read=True
    _line =line.replace("//", CHAR_CMT_EOL).replace("/*", CHAR_CMT_START).replace("*/",CHAR_CMT_STOP)
    for char in _line:
        if char == CHAR_EOL:
            cline+=char
            if read==None:
                read=True
        elif char == CHAR_CMT_START and read is not None:
            read=False                 # Read False if multiline Comment
        elif char == CHAR_CMT_STOP and read is not None:
            read=True
        elif char == CHAR_CMT_EOL and read is True:
            if not fortran:
                read=None         # Read None if single line comment
            else:
                cline+=char        # Skipp this in Fortran            
        else:
            if read is True :
                cline+=char
    
    cline = cline.replace(CHAR_CMT_EOL,"//")
    return cline


def clean_c_comments(lines:List[str],fortran:bool=False)->List[str]:    
    if not lines:
        return []
    raw = CHAR_EOL.join(lines)
    out = strip_c_comment(raw,fortran=fortran).split(CHAR_EOL)
    assert len(lines) == len(out)
    return out



def read_lines_with_encoding(filename:str)-> list:
    """Sacres francais"""
    try: 
        with open(filename,"r", encoding="utf8") as fin:
            lines = fin.read().split("\n")
    except UnicodeDecodeError as e :
        with open(filename,"r", encoding="latin1") as fin:
            lines = fin.read().split("\n")
    
    return lines
    

def align_end_continuations(stmts: Statements, cont_char:str) -> Statements:
    """Align continuation with amprsand
    
    For example

     FORMAT("Lorem ipsum &
     sic hamet") 
    
    """
    new_stmt = []
    new_lines = []
    last_line = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if last_line.strip().endswith(cont_char):
            new_stmt[-1] = last_line[:-1] + " " + line.strip().lstrip(cont_char)
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

        last_line = new_stmt[-1]
    return Statements(new_stmt, new_lines)
