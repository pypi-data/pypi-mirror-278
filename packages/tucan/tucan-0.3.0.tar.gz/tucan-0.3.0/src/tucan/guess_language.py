
# """module to guess the language of a code base"""

from loguru import logger
from typing import List

def guess_language(lines: List[str])->str:
    """return the language according to lines content
    return None if no clue found"""              

    cpp_clues=0
    ftn_clues=0
    py_clues=0
    for line in lines:
        # C/C++ clues
        if line.rstrip().endswith(";"):
            cpp_clues+=1
        for pattern in ["//", '/*', 'def ', '#include ', 'void']:
            if line.lstrip().startswith(pattern):
                cpp_clues+=1

        # Python clues
        for pattern in ["'''", '"""', 'def ', 'import ']:
            if line.lstrip().startswith(pattern):
                py_clues+=1
        
        # fortran clues
        for pattern in ["function ", 'module ', 'subroutine ',  'implicit ']:
            if line.lstrip().startswith(pattern):
                ftn_clues+=1
        for pattern in ['! ', "     +", "* "]:
            if line.startswith(pattern):
                ftn_clues+=1


    logger.info(f"C {cpp_clues}, Py {py_clues}, FTN {ftn_clues}")
    if cpp_clues> max(py_clues,ftn_clues):
        return "ccpp"
    if ftn_clues> max(py_clues,cpp_clues):
        return "fortran"
    if py_clues> max(ftn_clues,cpp_clues):
        return "python"
    return None
        
        

