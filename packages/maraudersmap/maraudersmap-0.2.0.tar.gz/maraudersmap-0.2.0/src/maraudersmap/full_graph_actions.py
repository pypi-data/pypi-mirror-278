import os, webbrowser

import networkx as nx
import fnmatch
from copy import deepcopy
import numpy as np
from matplotlib import colors as mplcolors
from loguru import logger
from maraudersmap.nx_utils import (
    remove_by_patterns,
    remove_hyperconnect,
    remove_singles,
    get_subgraph,
    merge_links,
    cut_links,
    compute_graph_depth
)

from maraudersmap.show_pyvis import showgraph_pyvis
from maraudersmap.show_plotly import dash_app_autoload,dash_app_noload
from maraudersmap.show_pyplot import ntw_pyplot2d
from maraudersmap.show_graphviz import ntw_graphiz

from maraudersmap.colors_utils import find_color,colorscale_hex,colorscale_legend


def show_graph(
        cgs_nx:nx.DiGraph,
        backend:str="pyvis",
        color:str="type",
        patterns:str=None,
        remove_patterns:list=None,
        hyperconnect:int=10, 
        subgraph_roots:list=None,
        merge:bool=False,
        nocalls:bool=False,
        load:bool=False,
    ):
    
    cgs_nx = clean_graph(
        cgs_nx,
        remove_patterns=remove_patterns,
        hyperconnect=hyperconnect,
        subgraph_roots=subgraph_roots,
        merge_containers=merge,
        nocalls=nocalls
    )

    cgs_nx, legend = color_nodes(cgs_nx, color, color_pattern=patterns)
    
    file_prefix = f"mmap_callgraph"

    if backend == "pyvis":
        showgraph_pyvis(cgs_nx, legend, file_prefix)
        if load:
            file_url = 'file://' + os.path.realpath(file_prefix+".html")
            webbrowser.open(file_url)
    elif backend == "plotly":
        if load:
            dash_app_autoload(cgs_nx)
        else:
            app = dash_app_noload(cgs_nx)
            app.run_server(debug=True, use_reloader=True)
            logger.info("App created, Please log yourself to the url:\nhttp://127.0.0.1:8050")
    elif backend == "pyplot":
        ntw_pyplot2d(cgs_nx,file_prefix=file_prefix)
    elif backend == "pydot":
        ntw_graphiz(cgs_nx, view=load)
    else:
        logger.error(f"Backend {backend} not understood")


def clean_graph(
    nxdata: nx.DiGraph,
    remove_patterns: list = None,
    hyperconnect: int = None,
    subgraph_roots:list =None,
    merge_containers:bool=False,
    nocalls:bool=False,
    #prune_lower_levels:int=None, # unused, prefer merge containers
    # soften_patterns: list = None,
) -> nx.DiGraph:
    """
    Performs the diverse cleanings of the graph

    Args:
        ntx (obj): ntx (obj): networkX DiGraph
        remove_patterns (list): List of patterns to match in nodes name
        soften_patterns (list): List of patterns to match in nodes name
        hyperconnect (int): number of edges allowed for nodes

    Returns:
        ntx (obj): networkX DiGraph cleaned

    """

    def log_graph_size():
        logger.info(f"{nxdata.number_of_nodes()} nodes / {nxdata.number_of_edges()} edges")

    logger.info("Start filtering graph")

    log_graph_size()
    if subgraph_roots is not None:
        new_data = nx.DiGraph()
        for pattern in subgraph_roots:
            results =  fnmatch.filter(nxdata.nodes.keys(), pattern)
            if len(results)>1:
                logger.warning(f"subgraph_roots pattern {pattern} yielded several results")
                for res in results:
                    logger.warning(f" -{res}")
                logger.warning(f"Skipping...")
                
            elif len(results)==0:
                logger.warning(f"subgraph_roots pattern {pattern} yielded no results,{' '.join(results)} skipping...")
            else:
                new_data =nx.compose(new_data, get_subgraph(nxdata,results[0]))
        nxdata=new_data
        log_graph_size()
    
    # if prune_lower_levels is not None:
    #     nxdata = crop_leafs(nxdata, levels=prune_lower_levels)
    #     log_graph_size()
    
    if hyperconnect is not None:
        nxdata = remove_hyperconnect(nxdata, hyperconnect)
        log_graph_size()
    
    #nxdata = remove_by_patterns(nxdata, ["<builtin>.*", "abc.*", "os.*", "shutil.*"])
    if remove_patterns is not None:
        nxdata = remove_by_patterns(nxdata, remove_patterns)
        log_graph_size()
    if merge_containers:
        nxdata = merge_links(nxdata, "contain")
        
    if nocalls:
        nxdata = cut_links(nxdata, "call")
    
    nxdata = remove_singles(nxdata)
    log_graph_size()

    
    
    # if soften_patterns is not None:
    #     nxdata = soften_by_patterns(nxdata, soften_patterns)
        

    


    logger.info(
        "After cleaning :"
        + str(nxdata.number_of_nodes())
        + " nodes/"
        + str(nxdata.number_of_edges())
        + " edges"
    )
    if nxdata.number_of_nodes() == 0:
        msgerr = "Filtering removed all nodes, aborting"
        logger.critical(msgerr)
        raise RuntimeError( "Filtering removed all nodes, aborting")
    return nxdata


def color_nodes_by_quantity(
    graph: nx.DiGraph,
    min_lvl: int,
    max_lvl: int,
    color_by: str,
    color_map: str = "rainbow_PuRd",
    log_scale: bool = True,
) -> dict:
    """
    Add hexadecimal color to networkX graph according to a selected data

    Args:
        graph (obj): NetworkX graph
        min_lvl (int): Lower bound
        max_lvl (int): Upper bound
        color_by (str): Name of the data to look for in graph
        color_map (str): Name of the Paul Tol's color map desired
        log_scale (bool): switch to log_scale

    Returns:
        colored_graph (obj) : Update the color key in the graph nodes dict
        legend (dict): Name and color for legend
    """
    colored_graph = deepcopy(graph)
    for node in colored_graph.nodes:
        lvl = colored_graph.nodes[node].get(color_by, None)
        color = colorscale_hex(
            lvl, min_lvl, max_lvl, color_map=color_map, log_scale=log_scale
        )
        colored_graph.nodes[node]["color"] = color

    legend = {}
    color_lvl = np.linspace(min_lvl, max_lvl, 5)

    for lvl in color_lvl:
        if min_lvl != 0 and max_lvl != 1:
            lvl = round(lvl)
        color_rgb = colorscale_hex(
            lvl, min_lvl, max_lvl, color_map=color_map, log_scale=log_scale
        )
        legend[str(lvl)] = color

    return colored_graph, legend




def color_nodes(cgs_nx:nx.DiGraph, color_scheme:str, color_pattern:dict=None):

    if color_scheme == "type":
        cgs_nx, legend = color_nodes_by_type(cgs_nx)
    elif color_scheme == "lang":
        cgs_nx, legend = color_nodes_by_lang(cgs_nx)
    elif color_scheme == "cplx":
        cgs_nx, legend = color_nodes_by_cplx(cgs_nx)
    elif color_scheme == "lvl":
        cgs_nx, legend = color_nodes_by_lvl(cgs_nx)
    elif color_scheme == "ptn":
        if color_pattern==None:
            raise RuntimeWarning("Color pattern not provided, exiting...")
        cgs_nx, legend = color_nodes_by_pattern(cgs_nx, color_pattern)
    else:
        raise ValueError("Color scheme not understood...")
    
    return cgs_nx,legend

def color_nodes_by_type(graph: nx.DiGraph):
    colored_graph = deepcopy(graph)

    COLORS_TYPE={
        "blue": ["function", "def", "int", "double", "char","float"],
        "teal": ["subroutine", "void"],
        "forestgreen": ["method"],
        "limegreen": ["procedure"],
        "darkgrey": ["module"],
        "khaki": ["object", "class"],
        "orange": ["type", "struct","enum","class"],
        "red": ["template"]
    }

    unrolled_colors = {}
    legend = {}
    for color,items in COLORS_TYPE.items():
        legend[items[0]]=color
        for item in items:
            unrolled_colors[item]=color

    for node in colored_graph.nodes():
        if "type" not in colored_graph.nodes[node]:
            logger.warning(f"No type for {node}")
            type_=None
        else:
            type_ = colored_graph.nodes[node]["type"]
        if type_ not in unrolled_colors:
            logger.warning(f"Type {type_} not colored...")
        colored_graph.nodes[node]["color"] = unrolled_colors.get(type_, "black")   
    return colored_graph,legend


def color_nodes_by_lang(graph: nx.DiGraph):
    colored_graph = deepcopy(graph)

    COLORS_LANG ={
        "python": "yellow",
        "fortran": "green",
        "cpp": "blue",
        "header": "teal",
        "other": "grey"
    }
    for node in colored_graph.nodes():
        if "lang" not in colored_graph.nodes[node]:
            logger.warning(f"No lang for {node}")
            lang_=None
        else:
            lang_= colored_graph.nodes[node]["lang"]
        colored_graph.nodes[node]["color"] = mplcolors.to_hex(COLORS_LANG.get(lang_, "black"))
    return colored_graph,COLORS_LANG


def color_nodes_by_lvl(graph: nx.DiGraph):
    colored_graph = deepcopy(graph)

    depth = compute_graph_depth(colored_graph)
    cmap = "rainbow_discrete"
    min_lvl = 1
    max_lvl = 12
    legend = colorscale_legend(min_lvl=min_lvl,max_lvl=max_lvl, log_scale=False,color_map=cmap)
    for node in colored_graph.nodes():
        color = colorscale_hex(depth[node],min_lvl=min_lvl,max_lvl=max_lvl, log_scale=False,color_map=cmap) 
        colored_graph.nodes[node]["color"] = color
    return colored_graph,legend

def color_nodes_by_cplx(graph: nx.DiGraph):
    colored_graph = deepcopy(graph)

    cmap = "iridescent"
    min_lvl = 1.
    max_lvl = 100.
    legend = colorscale_legend(min_lvl=min_lvl,max_lvl=max_lvl, log_scale=True,color_map=cmap, levels=12)
    for node in colored_graph.nodes():
        color = colorscale_hex(colored_graph.nodes[node]["CCN"],min_lvl=min_lvl,max_lvl=max_lvl, log_scale=True,color_map=cmap) 
        colored_graph.nodes[node]["color"] = color
    return colored_graph,legend

def color_nodes_by_pattern(graph: nx.DiGraph, color_rules: dict):
    """
    Add hexadecimal color to networkX graph according to selected patterns

    Args:
        graph (obj): NetworkX graph
        color_rules (dict): Patterns as key, color as value

    Returns:
        colored_graph (obj) : Update the color key in the graph nodes dict
        legend (dict): Name and color for legend
    """
    if color_rules is None:
        raise RuntimeError("Colors rules are missing...")

    colored_graph = deepcopy(graph)
    for node in colored_graph.nodes():
        #color = colored_graph.nodes[node].get("color", None)
        #if not color:                               # do not get why 
        color = find_color(node, color_rules)
        colored_graph.nodes[node]["color"] = color

    legend = {}
    for key, color in color_rules.items():
        legend[key] = mplcolors.to_hex(color)

    return colored_graph, legend

