"""
Tucan module to get the imports of a python file
"""
from tucan.unformat_common import Statements


def imports_c(statements: Statements) -> dict:
    """
    Main function to search the imports in a C C++ file.

    Args:
        statements (Statements): List of unformatted code statements along with line number ranges.

    Returns:
        dict: Dict with the module or function name associated with its various imports.
    """
    imports_dict = c_imports(statements)

    return imports_dict


def c_imports(stmts: Statements) -> dict:
    """
    Parse the C/C++ code to check for the imports and update the imports database.

    Args:
        stmts (Statements): List of unformatted code statements along with line number ranges.

    Returns:
        imports_dict (dict): Dict with the module or function name associated with its various imports.
    """
    imports_dict = {}
    

    return imports_dict
