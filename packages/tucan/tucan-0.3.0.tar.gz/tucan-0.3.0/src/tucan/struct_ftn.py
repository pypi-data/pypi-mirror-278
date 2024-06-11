import re
from typing import Tuple
from loguru import logger
from tucan.unformat_common import Statements
from tucan.struct_common import (
    new_buffer_item,
    new_stack_item,
    struct_from_stack,
    struct_augment,
)
from tucan.unformat_common import rm_parenthesis_content
from tucan.string_utils import find_words_before_left_parenthesis_noregexp, tokenize


from tucan.kw_lang import STRUCTURES_FTN, NESTS_FTN, OTHERS_FTN


PARTS = sorted(STRUCTURES_FTN, reverse=True)
NESTS = sorted(NESTS_FTN, reverse=True)
INTRINSICS = OTHERS_FTN


def extract_struct_ftn(stmts: Statements, verbose) -> dict:
    """Main calls to build structure form statements

    statements is the output of tucan.unformat_ftn.unformat_ftn
    """
    clean_code = stmts.to_code()

    try:
        all_structs = _extract_on_cleaned_ftn(stmts, verbose=verbose)
    except RuntimeError:
        return None
    all_structs = struct_augment(
        all_structs, clean_code, find_callables_ftn, compute_ccn_approx_ftn
    )
    return all_structs


def _extract_on_cleaned_ftn(stmts: Statements, verbose=False) -> dict:
    """Extract structure from cleaned statements."""
    buffer_pile = []
    stack = []
    path = []

    ins_ = []
    out_ = []
    stat_idx = 0
    for line, (line_idx1, line_idx2) in zip(stmts.stmt, stmts.lines):
        stat_idx += 1

        line = line.lstrip(" ")

        # you must also note nests because bare end statement can jam the system
        # kw are listed in reverse order to try longer kwords first: type_real before
        # for part in sorted(STRUCTURES_FTN + NESTS_FTN, reverse=True):
        for part in sorted(PARTS + NESTS, reverse=True):
            if line.startswith(part + " ") or line == part:
                ins_.append(line)
                name, type_ = _parse_name_ftn(line, line_idx1)
                path.append(name)
                buffer_pile.append(
                    new_buffer_item(
                        type_=type_,
                        path=path,
                        name=name,
                        first_line=line,
                        line_idx=line_idx1,
                        statement_idx=stat_idx,
                        verbose=verbose,
                    )
                )
                break  # must not look at the following part, or both function and function_elemental will trigger

        if "procedure" in line:
            tokens = tokenize(line)
            if "=>" in tokens:
                idx = tokens.index("=>")
                target = tokens[idx + 1]
                proxy = tokens[idx - 1]
            else:
                target = tokens[-1]
                proxy = tokens[-1]

            target_name = ".".join(path[:-1]) + "." + target
            proxy_name = ".".join(path) + "." + proxy
            path.append(proxy)
            last_buff = buffer_pile[-1]

            # logger.warning(f"Adding proxy {proxy_name} (pointer to {target_name}) to {last_buff.name}")

            buf_ = new_buffer_item(
                type_="procedure",
                path=path,
                name=proxy_name,
                first_line=line,
                line_idx=line_idx1,
                statement_idx=stat_idx,
                verbose=verbose,
                callables=[target_name],
            )
            stack.append(
                new_stack_item(buf_, line_idx1, stat_idx, line, verbose=verbose)
            )
            path.pop(-1)

        if line.startswith("__type_from__"):
            parent = tokenize(line)[2]
            # logger.warning(f"Adding parent {parent}")
            if parent not in buffer_pile[-1].parents:
                buffer_pile[-1].parents.append(parent)

        if line.startswith("type") and "extends" in line:
            strt_ = line.index("extends")
            read = False
            parent = ""
            for char in line[strt_:]:
                if char == "(":
                    read = True
                elif char == ")":
                    break
                else:
                    if read:
                        parent += char
            parent = parent.strip()
            # logger.warning(f"Adding parent {parent}")
            if parent not in buffer_pile[-1].parents:
                buffer_pile[-1].parents.append(parent)

        if line.startswith("end ") or line.strip() == "end":
            out_.append(line)
            try:
                last_buff = buffer_pile[-1]  # Here
            except IndexError:
                msg = f"No buffer for line {line_idx1}:{line}"
                logger.critical(msg)
                raise RuntimeError(msg)

            stack.append(
                new_stack_item(last_buff, line_idx2, stat_idx, line, verbose=verbose)
            )
            path.pop(-1)
            buffer_pile.pop(-1)
            continue

    # Check specific to fortran
    for stack_item in stack:
        short_type = stack_item.type_.split("_")[0].strip()
        if short_type not in stack_item.end_line:
            pathstr = ".".join(path)
            logger.debug(
                f"End mismatch \nat {pathstr} for {short_type}:\n '{stack_item.start_line_idx}' to '{stack_item.end_line_idx}'.\n For {stack_item.type_} in {stack_item.end_line}"
            )

    # if len(ins_) != len(out_):
    #     for aa, bb in zip(ins_, out_):
    #         logger.warning(f"{aa}<>{bb}")
    #     logger.error(
    #         "Missing one structure statement such as end if... removing file from current analysis"
    #     )
    #     return {}

    return struct_from_stack(stack, main_types=PARTS + ["procedure"])


def _parse_name_ftn(line: str, line_nb: int) -> Tuple[str, str]:
    """expect a lowercase stripped line
    takes the second word as the name
    """

    line = rm_parenthesis_content(line)

    tokens = tokenize(line)
    # no names
    if tokens[0] in NESTS + [
        "interface"
    ]:  # because interface is usually used without name
        name = line.split()[0] + str(line_nb)
        if "#LABEL" in line:
            name += "_" + line.split("#")[-1].split(":")[-1].strip()
    elif "::" in tokens:
        idx = tokens.index("::")
        name = tokens[idx + 1]
    else:
        name = tokens[1]

    type_ = tokens[0]

    return name, type_


##### FTN specific functions


def find_callables_ftn(code: list) -> list:
    """Find callables in python"""
    candidates = []
    for line in code[1:]:
        if " call " in line:
            candidates.append(line.split("(")[0].split()[-1])
        else:
            candidates.extend(find_words_before_left_parenthesis_noregexp(line.strip()))
    # NB we expect lines like 'call mysubroutine()' to be caught by left parenthesis law$
    matches = [
        cand.replace("%", ".")
        for cand in set(candidates)
        if cand
        not in INTRINSICS
        + [
            "__type_is__",
            "__type_from__",
            "select_type",
            "double_precision",
            "if",
            ".or.",
            ".and.",
        ]
    ]

    return sorted(matches)  # Must be sorted for testing


def compute_ccn_approx_ftn(code: list) -> int:
    """Count decision points (if, else if, do, select, etc.)"""
    decision_points = re.findall(
        r"(?i)(if |else if|do |select case|select default)", "\n".join(code)
    )
    complexity = len(decision_points) + 1
    return complexity
