"""
Set of tools to build a networkx tree graph
"""

from pathlib import Path
import networkx as nx
from loguru import logger

from tucan.package_analysis import (
    clean_extensions_in_paths,
    rec_travel_through_package,
)
from tucan.struct_main import struct_main


def add_void_node(
    graph: nx.DiGraph, node_key: str, filepath: str, analyzed: bool = False
) -> nx.DiGraph:
    """
    Addition of void node to current graph

    Args:
        graph (obj): NetworkX graph
        node_key (str): Name of the node in the network
        filepath (str): Path to the file currently analyzed
        analyzed (bool): Was the file read or not

    Returns:
        graph (obj): networkx digraph object of tree graph updated
    """
    graph.add_node(
        node_key,
        name=node_key,
        path=filepath,
        size=1,
        ccn=1,
        line_start=None,
        line_end=None,
        defined_callables=[],
        analyzed=analyzed,
        func=[],
    )
    return graph


def add_fullnode(
    graph: nx.DiGraph,
    node_key: str,
    func_name: str,
    filepath: str,
    size: int,
    ccn: int,
    line_start: int,
    line_end: int,
    defined_callables: list,
) -> nx.DiGraph:
    """
    Add the child associated to a node by adding its parameters as well as the edge

    Args:
        graph (obj): NetworkX graph
        node_key (str): Name of the parent node
        func_name (str): Name of the function
        filepath (str): Path to the file currently analyzed
        size (int): Size of the function
        ccn (int): Cyclomatic complexity of the function
        line_start (int): Starting line of function in file
        line_end (int): Ending line of function in file
        defined_callables (list): List of functions defined in the function

    Returns:
        graph (obj): NetworkX graph updated

    """
    graph.add_node(
        node_key,
        name=node_key,
        path=filepath,
        size=size,
        ccn=ccn,
        line_start=line_start,
        line_end=line_end,
        defined_callables=defined_callables,
        func=func_name,
        analyzed=True,
    )
    # graph.add_edge(node_key, f"{node_key}:{func_name}")

    return graph


def get_tree_nx_file(filename: str, node_key: str, graph: nx.DiGraph) -> nx.DiGraph:
    """
    Analyze files to get the size, name of functions inside, complexity of it
    It also adds a node for each function inside the file as well as the edges to connect
    the file with its corresponding function.

    Args:
        filename (str): Name of the file
        node_key (str): Name of the node in the network
        graph (obj): NetworkX graph

    Returns:
        graph (obj): NetworkX graph with new edges and node corresponding
                    to the function within the file.
    """
    logger.info(f"   -{filename}:get func tree ")

    logger.debug(f"   Scan file {filename}")
    tucan_struct = struct_main(filename)
    logger.debug(f"   Tucan done")

    if not tucan_struct:
        graph = add_void_node(graph, node_key, filename)  # No function found
    else:
        graph = add_fullnode(
            graph,
            node_key,
            [],
            filename,
            1,
            1,
            0,  # Line start, to be seeked
            1,  # Line end, to be seeked
            [func_name for func_name in tucan_struct.keys()],
        )

        for func_name, struct_ in tucan_struct.items():
            graph = add_fullnode(
                graph,
                f"{node_key}:{func_name}",
                func_name,
                filename,
                struct_["NLOC"],
                struct_["CCN"],
                struct_["lines"][0],
                struct_["lines"][1],
                struct_["contains"],
            )

        # Link the nodes inside the file
        for func_name, struct_ in tucan_struct.items():
            if struct_["contains"]:
                for called in struct_["contains"]:
                    graph.add_edge(f"{node_key}:{func_name}", f"{node_key}:{called}")

        for func_name, struct_ in tucan_struct.items():
            if not nx.ancestors(graph, f"{node_key}:{func_name}"):
                graph.add_edge(node_key, f"{node_key}:{func_name}")

    logger.debug(f"   End Scan file {filename}")

    return graph


def get_tree_nx_folder(
    repo_path: Path, paths_list: list, graph: nx.DiGraph
) -> nx.DiGraph:
    """
    Function to travel through a code folder in order to analyze every folder and file
    to be the tree_graph

    Args:
        repo_path (obj): Path object pointing to the repository starting path
        current_path (obj): Path object pointing to the current position
        graph (obj): networkX graph

    Return:
        graph (obj): networkX graph updated
    """
    for element in paths_list:
        filename = element
        logger.debug(f"Get tree  element {filename}")

        file_key = Path(element).relative_to(repo_path.parents[0])

        graph = get_tree_nx_file(filename, file_key.as_posix(), graph)

        # Connection of all the nodes to meet the root on top of the graph.
        previous_link = file_key.as_posix()
        for parent in file_key.parents:
            if parent.as_posix() == ".":
                break

            if parent.as_posix() not in graph.nodes():
                # Addition of folders as void node, complexity etc will be computed later in _rec_node_stat
                path_ = filename.replace(filename.split(parent.as_posix())[-1], "")
                graph = add_void_node(graph, parent.as_posix(), path_, analyzed=True)
            graph.add_edge(parent.as_posix(), previous_link)
            previous_link = parent.as_posix()

    return graph


def _rec_node_stats(
    graph: nx.DiGraph,
    node: str,
) -> None:
    """
    Update the data of the nodes graph according to the successors, i.e. update
    the ccn, size and check if it's a leaf, or an empty folder.

    Args:
        graph (obj): networkX graph
        node (str): node name

    Returns:
        Update current graph with computed parameters
    """
    succ = list(graph.successors(node))
    graph.nodes[node]["name"] = node  # to save it explicitly in the json file

    if succ:  # NODES, not LEAFS, only
        ccn_avg = 0
        tot_nloc = 0
        mod_list = []
        for child in succ:
            _rec_node_stats(graph, child)
            ccn_avg += graph.nodes[child]["ccn"] * graph.nodes[child]["size"]
            tot_nloc += graph.nodes[child]["size"]

            if "func" in graph.nodes[child] and isinstance(
                graph.nodes[child]["func"], str
            ):
                mod_list.append(graph.nodes[child]["func"].split("::")[0])

        # path_ = graph.nodes[child]["path"].replace(
        #     "/" + graph.nodes[child]["path"].split("/")[-1], ""
        # )
        ccn_avg /= tot_nloc
        graph.nodes[node]["module"] = list(set(mod_list))
        graph.nodes[node]["size"] = tot_nloc
        graph.nodes[node]["ccn"] = ccn_avg
        graph.nodes[node]["leaf"] = False
        graph.nodes[node]["soften"] = True
        # graph.nodes[node]["path"] = path_

    else:  # LEAFS only
        graph.nodes[node]["leaf"] = True

        if "size" not in graph.nodes[node].keys():  # TMN : Case of an empty folder
            graph.nodes[node]["size"] = 1
            graph.nodes[node]["ccn"] = 1
            graph.nodes[node]["empty_folder"] = True


###################################


def get_tree(
    path: str,
    code_name: str,
    filter_extensions: bool = True,
) -> nx.DiGraph:
    """
    Main function that builds the network X tree graph, this can show the graph with nobvisual
    and / or pyvis.

    Args:
        path (str): Path to the root folder of the code or file
        code_name (str): Name of the code
        filter_extensions (bool): If this is True all files that are unreadable for tucan will be removed. Defaults to True.

    Returns:
        graph (obj): NetworkX of the tree_graph
    """
    repo_path = Path(path)
    main_folder = repo_path.relative_to(repo_path.parents[0]).as_posix()
    
    graph = nx.DiGraph()
    graph.add_node(main_folder, name=main_folder, path=repo_path.as_posix())
    logger.info(f"Get functree in path : {repo_path}")
    logger.info(f"   root folder : {main_folder}")

    if repo_path.is_file():
        filename = repo_path.as_posix()
        #file_key = filename.split(f"/{code_name}/")[-1]
        file_key = repo_path.relative_to(repo_path.parents[0]).as_posix()
        graph = get_tree_nx_file(filename, file_key, graph)
    else:
        paths_list = rec_travel_through_package(path)
        if filter_extensions:
            paths_list = clean_extensions_in_paths(paths_list)

        print("path", path)
        print("Plist", paths_list)
        graph = get_tree_nx_folder(repo_path, paths_list, graph)

    _rec_node_stats(graph, main_folder)

    return graph
