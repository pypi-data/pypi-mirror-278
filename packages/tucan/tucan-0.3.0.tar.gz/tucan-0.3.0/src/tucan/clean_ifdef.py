from typing import List
from loguru import logger
from tucan.unformat_common import strip_c_comment, clean_c_comments, read_lines_with_encoding
from tucan.string_utils import tokenize

def scan_ifdef_variables(lines: List[str]) -> list:
    """Detect ifdef variables

    cancels inner variables"""
    out = []
    inner_defined = []
    
    for line in align_continuation(lines):
        if (
            line.startswith("#ifdef")
            or line.startswith("#elif")
            or line.startswith("#if ")
        ):
            rhs = line.split()[1]

            rhs = rhs.replace("defined(", "")
            rhs = rhs.replace(")", "")

            rhs = rhs.replace("||", " ")
            rhs = rhs.replace("&&", " ")

            out.extend(rhs.split())
        if line.startswith("#define"):
            definition = line.split()
            inner_defined.append(definition[1])

        inner_def = sorted(set(inner_defined))
        global_def= sorted(set(out))
        global_def = [item for item in global_def if item not in inner_defined]
        
    return global_def,inner_def


            




def read_definition(line:str)->str:
    parts=strip_c_comment(line).split()
    out = None
    if len(parts)==2:
        out= parts[1]+"=True"
    elif len(parts)>=3:
        out=parts[1]+"="+" ".join(parts[2:])
    else:
        raise RuntimeError(f"CPP statement - definition not understood :  {line}")
    return out

def remove_ifdef_from_module(lines: List[str], definitions: List[str], verbose: bool=False, fortran:bool=False) -> List[str]:
    """Cleaned version of a code
    
    The output must be exactly as long a the input
    """

    uncommented_lines = clean_c_comments(align_continuation(lines),fortran=fortran) # we should all C comments, except // for fortran

    out = []
    context = []
    definitions_values=[ def_+"=True" for def_ in definitions]

    local_definitions=[]
    for i_line,line in enumerate(uncommented_lines):
        #ifdef_line = line.lstrip()
        if not context:
            included = True
        # ============================== Ifdef logic =============================
        if line.lstrip().startswith("#"):
            out_=""
            tokens = tokenize(line.lstrip().lstrip("#"))
            
            if tokens[0] in ["ifdef", "ifndef","elif","if"]:
                included,context = pragma_start(line,tokens,context,definitions_values+local_definitions)
            elif tokens[0]=="else":
                included, context = pragma_else(line,context)
            elif tokens[0]=="endif":
                included, context = pragma_end(line,context,i_line)
            elif tokens[0] in ["define", "undef"]:
                local_definitions = pragma_def_ndef(tokens[0],line, included, local_definitions)
            else :  # pragma not treated
                if included:
                    out_=line
            out.append(out_)

        else:  # Normal code
            if included:
                out.append(line)
                if verbose:
                    logger.success(f"{i_line:04}|{line}")
            else:
                out.append("")
                if verbose:
                    logger.error(f"{i_line:04}|{line}")
    try:       
        assert len(out)==len(lines)  # The output length must match exactly the input
    except AssertionError:
        logger.critical(f"Cleaned version {len(out)}/{len(lines)}")
        raise RuntimeError("Ifdef cleaning failed")
    return out

def pragma_start(line,tokens,context,definitions):
    status = str(interpret_ideflogic(line,definitions ))
    # increment context
    if tokens[0] == "elif":
        context[-1].append(status)  # append to the sublist of the last element
    else:
        context.append([status])  
    included = evaluate_context(context)
    return included, context

def pragma_else(line,context):
    logger.debug(f"Line {line}")
    #  if  elif  else
    #  True False False
    #  False True False
    #  False False True
    # all of the previous if/eli in the context must be false for else to be true
    status = "True"
    for bool_ in context[-1]:
        if bool_ == "True":  # if any of previous is true, status is False.
            status = "False"
    context[-1].append(status)
    included = evaluate_context(context)
    return included, context

def pragma_end(line,context,iline):
    if not context:
        logger.error(f"{iline:04}|{line} : No context found")
        raise RuntimeError("IFdef cleaning failed")
    else:
        context.pop(-1)  
    included = evaluate_context(context)
    return included, context

def pragma_def_ndef(token0,line, included, local_definitions):
    if not included:
        return local_definitions
    
    if token0=="define":  # variable definitions
            local_definitions.append(read_definition(line))
    if token0=="undef":   # variable definitions
        def_=strip_c_comment(line).split()[1]
        local_definitions = [item for item in local_definitions
            if not item.startswith(def_+"=")]   
    return local_definitions

def evaluate_context(context: list) -> bool:
    """Interpret the context to see if next lines will be included or not"""
    if context == []:
        return True 
    final_context = [bools_[-1] for bools_ in context]
    if eval(" and ".join(final_context)):
        included = True
    else:
        included = False
    return included


def replace_strings_by_proxies(line:str)-> (str, dict) :
    """Extreme measure to handle strings values in Ifdefs..."""
    proxies={}
    indexes = [i for i, char in enumerate(line) if char == '"']

    if not indexes:
        return line, proxies 
    
    #logger.critical("Replacing strings:"+line)
    last_char=0
    out_line = ""
    for i in range(0, len(indexes), 2):
        pair = indexes[i:i+2]
        key = f"#STR{i}#"
        try:
            value = line[pair[0]:pair[1]+1]
        except IndexError: # happen is " are not in even number 
            break          # well this should never happen but you never know
        proxies[key]=value
        out_line+=line[last_char:pair[0]-1] + " "+key
        last_char=pair[1]+1

    out_line+=line[last_char:]
    return out_line, proxies 


def align_continuation(lines:List[str])-> List[str] :
    """Ensure ligne continuation is understood, but keep line numbers"""
    
    lines_list = []
    new_line=""
    skip=0
    for line in lines:
        new_line+=line
        if line.endswith("\\"):
            skip+=1
            new_line=new_line[:-1]# remove last char
        else:
            lines_list.append(new_line)
            for _ in range(skip):
                lines_list.append("")
            skip = 0
            new_line =""
    return lines_list


def interpret_ideflogic(line:str,definitions:list)->bool:
    """ Assume an #ifdef-like start:  interpret the content of the line 
    
    NB: no #else or #endif should be ever encountered here (no logic to solve)
    """
    def_dict = {}
    for def_ in definitions:
        key,value=def_.split("=", 1)
        def_dict[key]=value
    
    re_line = strip_c_comment(line).lstrip().lstrip("#")
    logger.warning(">>>"+re_line)
    
    tokens = tokenize(re_line)
    # clean right hand side
    
    REPLACE = {
        "ifndef": "not",
        "ifdef":"",
        "if":"",
        "elif":"",
        "defined":"",
        "!":"not",
        "||":"or",
        "&&":"and",
    }
    tokens = [REPLACE.get(item, item) for item in tokens]
    re_line = " ".join(tokens)
    # assemble expression as string
    re_line, proxies=replace_strings_by_proxies(re_line)
    
    expr = ""
    for item in re_line.split():
        expr+= " "
        if item in def_dict:
            expr += def_dict[item]
        elif item in proxies:
            expr += proxies[item]
        elif item in [ 
            "(", ")", ">", "<",       #simple chars operators
            "<=", ">=", "==", "!=",   #double chars operators
            "not", "or", "and"        #logical operators
        ]:
            expr += item
        
        elif item.isdigit():
            expr += item
        else:
            expr += "False"
        expr+= " "
    try:
        out = eval(expr)
        #logger.warning(f"Expr   :{expr}")
    except (SyntaxError, TypeError) :
        logger.warning(f"Origin :{line}")
        logger.warning(f"Clean  :{re_line}")
        logger.warning(f"Expr   :{expr}")
        #raise RuntimeError("IFDEF expression not understood")
        logger.critical("IFDEF expression not understood, fallback to false")
        return False
    
    return out


def run_ifdef_pkg_analysis(files: dict) -> dict:
    """
    Gather the data associated to the functions and the imports within a file

    Args:
        files (dict): key: short_name , value: absolute paths

    Returns:
        dict: _description_
    """

    ifdef_analysis = {
        "global": [],
        "local": {},

    }
    
    gvars = []
    for file ,path_ in files.items():
        logger.info(f"Detecting iddefs... {path_}")
        lines= read_lines_with_encoding(path_)
        
        gv_, lv_ = scan_ifdef_variables(lines)
        
        gvars.extend(gv_)
        ifdef_analysis["local"][file]=lv_

    ifdef_analysis["global"]=sorted(set(gvars))
    logger.success("Analysis completed.")
    return ifdef_analysis

# with open("templates_ifdef.f","r") as fin:
#     lines = fin.read().split("\n")

# vars = scan_ifdef_variables(lines)
# print("Found "+ ", ".join(vars))

# out =remove_ifdef_from_module(lines,["OUIPI1","MOREARG","LVL1"])


# print("\n".join(out))