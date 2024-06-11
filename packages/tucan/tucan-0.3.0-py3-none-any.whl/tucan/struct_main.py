"""Global function to handle the struct analysis of various languages"""
from loguru import logger

from tucan.unformat_common import read_lines_with_encoding
from tucan.unformat_py import unformat_py
from tucan.unformat_ftn import unformat_ftn
from tucan.unformat_c import unformat_c
from tucan.struct_py import extract_struct_py
from tucan.struct_ftn import extract_struct_ftn
from tucan.struct_c import extract_struct_c
from tucan.clean_ifdef import remove_ifdef_from_module
from tucan.guess_language import guess_language

def struct_main(filename: str, verbose:bool=False) -> dict:
    """
    Extract structure of a fortran or python file.
    - Find the nested structures of a code
    - Find the callables in each structure
    - Evaluate sizes, CCN

    Args:
        filename (str): Name of the file (with its path) to parse.

    Returns:
        dict: Structure analyzed, with complexity, size, name, path, lines span, etc.

    """
    logger.info(f"Struct analysis on {filename}")
    code =  read_lines_with_encoding(filename)
    

    code = [line.lower() for line in code]  # Lower case for all

    if filename.lower().endswith(".py"):
        logger.debug(f"Python code detected ...")
        statements = unformat_py(code)
        struct_ = extract_struct_py(statements, verbose)
    elif filename.lower().endswith((".f", ".F", ".f77", ".F77", ".f90", ".F90")):
        logger.debug(f"Fortran code detected ...")
        code = remove_ifdef_from_module(code , [], verbose=False, fortran=True)
        statements = unformat_ftn(code)
        struct_ = extract_struct_ftn(statements,verbose)
    elif filename.lower().endswith((".c", ".cpp", ".cc")):
        logger.debug(f"C/C++ code detected ...")
        code = remove_ifdef_from_module(code , [], verbose=False)
        statements = unformat_c(code)
        struct_ = extract_struct_c(statements, verbose)
    elif filename.lower().endswith((".h", ".hpp")):
        lang = guess_language(code)
        logger.info(f"Language of .h file is ({lang}), ")
            
        if lang in ["fortran"]:
            logger.debug(f"Fortran code detected ...")
            code = remove_ifdef_from_module(code , [], verbose=False, fortran=True)
            statements = unformat_ftn(code)
            struct_ = extract_struct_ftn(statements,verbose)
        else:# lang in ["ccpp"]:
            logger.debug(f"C/C++ code detected ...")
            code = remove_ifdef_from_module(code , [], verbose=False)
            statements = unformat_c(code)
            struct_ = extract_struct_c(statements, verbose)
        
        # else:
        #     raise RuntimeError()
        
    else:
        ext = filename.lower().split(".")[-1]
        logger.error(f"Extension {ext} not supported, exiting ...")
        return {}

    return struct_


def create_empty_struct(filename: str) -> dict:
    """
    Function to create an empty structure output.

    Args:
        filename (str): Name of the file (with its path) to parse.

    Returns:
        dict: Empty structure dict i.e. with defaults values.
    """
    struct_ = {
        filename: {
            "CCN": 1,
            "NLOC": 1,
            "callables": [],
            "contains": [],
            "lines": [0, 0],
            "linestart": None,
            "name": filename,
            "path": [filename],
            "ssize": 0,
            "statements": [],
            "type": None,
        }
    }
    return struct_
