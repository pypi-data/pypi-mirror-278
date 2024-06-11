import networkx as nx
from loguru import logger
from pathlib import Path
import json,os

from typing import List
from tucan.package_analysis import (
    run_struct,
    rec_travel_through_package,
    clean_extensions_in_paths,
)

EPS = 1e-12

def get_callgraph(
        path: str,
        context: str,
    ) -> nx.DiGraph:
    """Get the  structure (what), and the context structure (with respect to what) to build the calgraph"""

    if Path(path).is_file():
        tgt_code_db = run_struct([path])
    else:
        tgt_paths_list = rec_travel_through_package(path)
        tgt_paths_list = clean_extensions_in_paths(tgt_paths_list)
        tgt_code_db = run_struct(tgt_paths_list)
    

    if context == path:  # often the case so it avoid recomputation
        context_code_db = tgt_code_db
    else:
        if Path(context).is_file():
            context_code_db = run_struct([context])
        else:
            context_paths_list = rec_travel_through_package(context)
            context_paths_list = clean_extensions_in_paths(context_paths_list)
            context_code_db = run_struct(context_paths_list)

    # with open("debug_struct.json","w") as fout:
    #     json.dump(context_code_db,fout,indent=4)
    callgraph = build_callgraph(
            tgt_code_db,
            context_code_db,
        )

    return callgraph

def build_callgraph(
    tgt_code_db: dict,
    context_code_db: dict,
) -> nx.DiGraph:
    """
    Build the callgraph.

    """
    logger.info("Computing callgraph, this can take a while...")

    ref_list = []
    for filename,fileddb in context_code_db.items():
        for funcname in fileddb:
            ref_list.append(filename+":"+funcname)
    print("\n".join(ref_list))

    positive_i=0
    negative_i=0
    positive_p=0
    negative_p=0
    positive_c=0
    negative_c=0

    callgraph = nx.DiGraph()
    for file_orig, file_db in tgt_code_db.items():
        for func_orig, func_db in file_db.items():
            if f"{file_orig}:{func_orig}" not in callgraph.nodes:
                #callgraph.add_node(f"{file_orig}:{func_orig}", **func_db)
                _add_node(callgraph,file_orig,func_orig,func_db)

            for contained_name in func_db["contains"]:
                match_name,match_file = find_function_reference(ref_list,contained_name,file_orig)

                if match_name is not None:
                    match_ddb = context_code_db[match_file][match_name]
                    _add_link(
                        callgraph,
                        match_ddb,
                        file_orig,
                        file_orig,
                        func_orig,
                        match_name,
                        type="contain"
                    )
                    positive_i+=1
                else:
                    negative_i+=1
        
            for parent_name in func_db["parents"]:
                match_name, match_file = find_function_reference(ref_list, parent_name,file_orig)
                if match_name is not None:
                    match_ddb = context_code_db[match_file][match_name]
                    _add_link(
                        callgraph,
                        match_ddb,
                        file_orig,
                        match_file,
                        func_orig,
                        match_name,
                        type="parent",
                    )
                    positive_p+=1
                else:
                    negative_p+=1

            for called_name in func_db["callables"]:
                
              #  _,match_name2,match_file2 = _fetch_function_in_all_ddb(context_code_db, called_name, init_file_guess=file_orig) 
                match_name,match_file = find_function_reference(ref_list, called_name,file_orig)
                # if match_name != match_name2:
                #     logger.critical(f"mismatch \n{file_orig} : {called_name}\n{match_file} : {match_name} \n{match_file2} : {match_name2}")
                if match_name is not None:
                    match_ddb = context_code_db[match_file][match_name]
                    _add_link(
                        callgraph,
                        match_ddb,
                        file_orig,
                        match_file,
                        func_orig,
                        match_name,
                        type="call",
                    )
                    positive_c+=1
                else:
                    negative_c+=1
 
    logger.success(f" Found contains  {positive_i} / {positive_i+negative_i} {positive_i/(positive_i+negative_i+EPS)*100}%")
    logger.success(f" Found parents   {positive_p} / {positive_p+negative_p} {positive_p/(positive_p+negative_p+EPS)*100}%")
    logger.success(f" Found callables {positive_c} / {positive_c+negative_c} {positive_c/(positive_c+negative_c+EPS)*100}%")
    logger.info("Callgraph generated")
    return callgraph


def keys_with_max_values(d):
    """
    Returns the set of keys with the maximum values from the dictionary.
    If the maximum value is zero, returns an empty set.

    Parameters:
    d (dict): The dictionary with integer values.

    Returns:
    set: The set of keys with the maximum values, or an empty set if the maximum value is zero.
    
    Example:
    >>> keys_with_max_values({'a': 3, 'b': 5, 'c': 5, 'd': 2})
    {'b', 'c'}
    >>> keys_with_max_values({'a': 0, 'b': 0, 'c': 0})
    set()
    """
    if not d:
        return list()
    max_value = max(d.values())
    if max_value == 0:
        return list()
    return [k for k, v in d.items() if v == max_value]


def back_match(list1: list, list2: list) -> int:
    """
    Count the number of matching elements from the end of two lists.

    Args:
        list1 (list): The first list to compare.
        list2 (list): The second list to compare.

    Returns:
        int: The number of matching elements from the end of both lists.
    """
    count = 0

    # Compare elements from the end of the lists
    for elem1, elem2 in zip(reversed(list1), reversed(list2)):
        if elem1 == elem2:
            count += 1
        else:
            break

    return count


def end_match(references:List[str], suffix:str, rootless:bool=False)->List[str]:
    """
    Finds and returns a list of strings from `references` that end with `str_`, with optional filtering based on `rootless` and `prefix`.

    Parameters:
    references (List[str]): A list of reference strings to be searched.
    str_ (str): The string to match at the end of each reference.
    rootless (bool): If True, strips the leading portion of `str_` before matching, starting from the first period character. Default is False.
    prefix (str): If provided, filters `references` to include only those that start with this prefix.

    Returns:
    List[str]: A list of strings from `references` that end with `str_` (or its rootless version if `rootless` is True).
    """
    
    #references = [ref for ref in references if ref.startswith(prefix)]
    
    items = suffix.split(".")
    if rootless:
        if len(items) == 1:
            return []
        items.pop(0)

    matches={}
    for ref in references:
        if ref.endswith(items[-1]):
            if rootless and "." not in ref.split(":")[1]:
                continue
            matches[ref] = back_match(ref.split(":")[1].split("."), items)
    out = keys_with_max_values(matches)
    return out


def find_function_reference(ref_list:list,  func_name:str, orig_file:str) -> (str, str):
    
    matchs = end_match(ref_list,  suffix= func_name)
    if not matchs:
        matchs = end_match(ref_list,   suffix=func_name, rootless=True)
    
    if matchs:
        #logger.success(f"Reference found {matchs[0]} <= {func_name} ")
        i_match = 0
        for i_m,match in enumerate(matchs):
            if match.startswith(orig_file):
                i_match = i_m
                break
            if len(match) < len(matchs[i_match]):
                i_match=i_m
            
        fileref,funcref=matchs[i_match].split(":")
        return funcref,fileref
    #logger.warning(f"Ref. to {func_name} not found")
    return None,None



def _add_node(callgraph:nx.DiGraph,file_:str, func_:str,db_by_func:dict):
    callgraph.add_node(
        f"{file_}:{func_}", 
        **db_by_func, 
        filename=file_, 
        lang=_cast_lang(file_)
    )

def _add_link(
        callgraph:nx.DiGraph, # the callgraph
        db_by_func:dict, # the func tree ddb for one file
        file_orig:str,  # the origin func filename
        file_target:str, # the target func filename
        func_orig:str,  # the origin func name
        func_target:str,  # the target func
        type: str= None
    ):
    """Add a link in the graph"""
    
    # for func_target_full, func_db in db_by_file.items():
    #     # test if a fiunc_name matches the call. if yes add the node and the edge
    #     #if _longest_match(func_target_full, func_target):  # pas necessaire
    if f"{file_target}:{func_target}" not in callgraph.nodes:
        # callgraph.add_node(
        #     f"{file_target}:{func_target}", **db_by_func, filename=file_orig, lang=_cast_lang(file_orig)
        # )
        _add_node(callgraph,file_target,func_target,db_by_func)

    callgraph.add_edge(
        f"{file_orig}:{func_orig}",
        f"{file_target}:{func_target}",
        type=type,

    )
    return

def _cast_lang(filename:str):

    _,ext = os.path.splitext(filename)
    if ext in (".f", ".F", ".f77", ".f90", ".F77", ".F90"):
        lang="fortran"
    elif ext in (".c", ".cpp", ".cc"):
        lang="cpp"
    elif ext in (".py"):
        lang="python"
    elif ext in (".h", ".hpp"):
        lang="header"
    else:
        logger.critical(f"extension not understood {ext}")
        lang="other"
    
    return lang

        
        
        

# def _try_add_callable_all(
#         callgraph:nx.DiGraph,
#         full_context_code_db:dict,# the func tree ddb for all files
#         file_orig:str,
#         func_orig:str,
#         func_target:str 
#     )-> bool:
#     """Try to add a callable if it is in the context of the same file"""
#     added = False
#     for file_target, db_by_file in full_context_code_db.items():

#         # for ctxt_func_name, func_db in ctxt_file_db.items():
#         #     if  _longest_match(ctxt_func_name, call):
#         #         if (f"{ctxt_filename}:{ctxt_func_name}"not in callgraph.nodes):
#         #             callgraph.add_node(
#         #                 f"{ctxt_filename}:{ctxt_func_name}",**func_db,
#         #             )
#         #         callgraph.add_edge(
#         #             f"{filename}:{func_name}",
#         #             f"{ctxt_filename}:{ctxt_func_name}",
#         #         )
#         #         break
#         added = _add_link(
#             callgraph ,
#             db_by_file,
#             file_orig,
#             file_target,
#             func_orig,
#             func_target
#         )
#         if added:
#             break    
       
#     return added





# def _fetch_function_in_all_ddb(allfiles_ddb:dict, func_name:str, init_file_guess:str=None) -> (dict, str, str):

#     all_filenames= list(allfiles_ddb.keys())

#     if init_file_guess is not None:
#         all_filenames = [init_file_guess] + all_filenames
#     for _file in  all_filenames: # search parent anywhere in the code
#         db_by_file = allfiles_ddb[_file]
#         match_ddb, match_name = _fetch_function_in_file_ddb(db_by_file, func_name)
#         if match_name is not None:
#             match_file=_file
            
#             return match_ddb, match_name, match_file

#     #logger.warning(f"Ref. to {func_name} not found")
#     return None,None,None

# def _fetch_function_in_file_ddb(file_ddb:dict, func_name:str) -> (dict, str):
#     for _func,_db_func in file_ddb.items():
#         if _longest_match(_func,func_name) :
#             match_name=_func
#             match_ddb=_db_func


#             #logger.success(f"Parent {match_name}  found")
#             return match_ddb, match_name
                
#     #logger.warning(f"Parent {func_name} not found")
#     return None,None

# def _longest_match(ctxt_func_name:str,call_func:str)->bool:
#     """Search for the longest match in the functions"""

#     try:
#         if ctxt_func_name.split(".")[-4:] == call_func.split(".") :
#             return True
#     except IndexError:
#         pass

#     try:
#         if ctxt_func_name.split(".")[-3:] == call_func.split(".") :
#             return True
#     except IndexError:
#         pass

#     try:
#         if ctxt_func_name.split(".")[-2:] == call_func.split(".") :
#             return True
#     except IndexError:
#         pass

#     if ctxt_func_name.split(".")[-1] == call_func :
#         return True


#     return False


    

    