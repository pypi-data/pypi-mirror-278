#!/usr/bin/env python
"""
cli.py

Command line interface for tools in MaraudersMaps
"""
import click
import os
from loguru import logger

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def add_version(f):
    """
    Add the version of the tool to the help heading.
    :param f: function to decorate
    :return: decorated function
    """
    import maraudersmap

    doc = f.__doc__
    f.__doc__ = (
        "Package "
        + maraudersmap.__name__
        + " v"
        + maraudersmap.__version__
        + "\n\n"
        + doc
    )

    return f


@click.group()
@add_version
def main_cli():
    """
    \b
            ---------------    Marauders map  --------------------
            You are now using the Command line interface of Marauders map package,
            a set of tools created at CERFACS (https://cerfacs.fr).
            It creates callgraphs for python and fortran projects.
    \b
            For the impatients;
            Use `mmap cg_fast`for a quick generation on a single file
    \b
            For larger projects:
            1 - Use `mmap anew` to create your main control file `mmap_in.yml`,
            2 - Edit `mmap_in.yml` to describe your project
            3 - Use `cg-gen` to pre-compute the callgraph (can take minutes)
            4 - Use `cg-show` with the different options to explore the callgraph
    """
    pass


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
def anew(file):
    """Create the default control file mmap_in.yml"""
    from pkg_resources import resource_filename
    import os, shutil

    write = True
    if os.path.isfile(file):
        msg = f"File {file} already exists. Overwrite ? [y/N] "
        if input(msg).lower() == "n":
            write = False
    if write:
        logger.info(f"Generating template inputfile {file} for maraudersmap.")
        shutil.copy2(
            resource_filename(__name__, "./mmap_in.yml"),
            file,
        )
    logger.success(f"File {file} created. Edit this file to set up your project...")


main_cli.add_command(anew)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def treefunc(file, verbose):
    """Create the tree of functions from sourcecode.

    Output is (name-of-pkg)/func_tree.json

    Need the MMAP Control file to find the sources,
    and obviously the sources themselves...
    """
    from maraudersmap.tree import get_tree
    import networkx as nx
    from json import dump as jdump
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)
    tree_graph = get_tree(
        param["path"],
        param["package"],
    )
    outdir = ensure_dir(param["package"])
    with open(outdir / "func_tree.json", "w") as fout:
        jdump(nx.node_link_data(tree_graph), fout, indent=4, sort_keys=True)
    logger.success(f"Generating {param['package']} / func_tree.json.")


main_cli.add_command(treefunc)


# @click.command()
# @click.option(
#     "--file",
#     "-f",
#     type=str,
#     default="./mmap_in.yml",
#     help="Input file with a custom name (.yml)",
# )
# @click.option(
#     "-v",
#     "--verbose",
#     is_flag=True,
#     show_default=True,
#     default=False,
#     help="Verbose mode",
# )
# def treefile(file, verbose):
#     """Create the tree of files from sourcecode.

#     Output is (name-of-pkg)/file_tree.json

#     Need the MMAP Control file to find the sources,
#     and obviously the sources themselves...
#     """
#     from maraudersmap.macro_tree import get_macro_tree
#     from networkx import node_link_data
#     from json import dump as jdump
#     from maraudersmap.mmap_startlog import mmap_startlog

#     mmap_startlog(verbose)
#     param = prepare_cmd(file)
#     macro_graph = get_macro_tree(
#         param["path"],
#         param["package"],
#     )
#     outdir = ensure_dir(param["package"])
#     with open(outdir / "file_tree.json", "w") as fout:
#         jdump(node_link_data(macro_graph), fout, indent=4, sort_keys=True)
#     logger.success(f"Generating {param['package']} / file_tree.json.")


# main_cli.add_command(treefile)


# @click.command()
# @click.argument(
#     "rules",
#     nargs=1,
#     type=click.Choice(["python", "fortran"]),
# )
# @click.option(
#     "-v",
#     "--verbose",
#     is_flag=True,
#     show_default=True,
#     default=False,
#     help="Verbose mode",
# )
# def regexp_input(rules, verbose):
#     """Create a score rules file"""
#     from pkg_resources import resource_filename
#     import os, shutil
#     from maraudersmap.mmap_startlog import mmap_startlog

#     mmap_startlog(verbose)
#     write = True
#     if rules == "python":
#         file = "./python_rc_default.yml"
#         if os.path.isfile(file):
#             msg = f"File {file} already exists. Overwrite ? [y/N] "
#             if input(msg).lower() == "n":
#                 write = False
#     elif rules == "fortran":
#         file = "./fortran_rc_default.yml"
#         if os.path.isfile(file):
#             msg = f"File {file} already exists. Overwrite ? [y/N] "
#             if input(msg).lower() == "n":
#                 write = False
#     if write:
#         logger.info(f"Generating dummy regexp inputfile {file} for maraudersmap score.")
#         shutil.copy2(
#             resource_filename(__name__, f"{file}"),
#             file,
#         )
#     logger.info(f"File {file} created. Edit this file to customize your own rules.")


# main_cli.add_command(regexp_input)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.argument(
    "rules",
    type=str,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def score(rules, file, verbose):
    """
    Add score to the MMAP tree of functions

    Need the MMAP Control file to find the sources,

    RULES is the regexp&structure set of rules.
    These rules can be generated through mmap regexp-input (can be edited)
    """
    import json, os
    from networkx import node_link_data, node_link_graph
    from json import dump as jdump
    from maraudersmap.score import get_score
    from pathlib import Path
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)

    func_tree = Path(param["package"]) / "func_tree.json"
    if not func_tree.exists():
        logger.warning(
            f"Function tree {str(func_tree)} is missing. Use `mmap tree` to create it."
        )

    with open(func_tree, "r") as fin:
        nld = json.load(fin)
    tree_graph = node_link_graph(nld)
    score_graph = get_score(param["path"], tree_graph, rules)
    with open(Path(param["package"]) / "func_tree_score.json", "w") as fout:
        jdump(node_link_data(score_graph), fout, indent=4, sort_keys=True)
    logger.success(f"Generating {param['package']}/func_tree_score.json with scores.")


main_cli.add_command(score)


@click.command()
@click.argument(
    "pattern",
    type=str,
)
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def grep(file, pattern, verbose):
    """

    JSON_DATA is the database of the tree graph generated through mmap tree
    """
    import json
    from pathlib import Path
    from networkx import node_link_data, node_link_graph
    import tkinter as tk
    from nobvisual.tkinter_circlify import tkcirclify
    from nobvisual.circlifast import circlifast
    from nobvisual.colorize import color_by_value
    from nobvisual.helpers import from_circlify_to_nobvisual
    from maraudersmap.grep import get_grep_coverage
    from maraudersmap.show_nobvisual import ntw_nobvisual
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)
    param = prepare_cmd(file)
    func_tree = Path(param["package"]) / "func_tree.json"
    print(func_tree)
    if not func_tree.exists():
        logger.warning(
            f"Function tree {str(func_tree)} is missing. Use `mmap tree` to create it."
        )
    with open(func_tree, "r") as fin:
        nld = json.load(fin)

    tree_graph = node_link_graph(nld)
    grep_cov_graph = get_grep_coverage(pattern, tree_graph)
    nobj = ntw_nobvisual(grep_cov_graph)
    legend = color_by_value(nobj, "grep", tolcmap="rainbow_WhRd")
    circles = circlifast(nobj, show_enclosure=False)
    draw_canvas = tkcirclify(from_circlify_to_nobvisual(circles), legend=legend)
    draw_canvas.show_names(level=2)
    tk.mainloop()


main_cli.add_command(grep)


@click.command()
@click.argument(
    "colorby",
    nargs=1,
    type=click.Choice(
        [
            "complexity",
            "score",
            "patterns",
            "size",
            "file_patterns",
            "file_complexity",
            "file_size",
        ]
    ),
)
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def showtree(colorby, file, verbose):
    """Visualize MMAP trees

    Need the MMAP Control file to find the sources
    """
    import json
    from pathlib import Path
    import networkx as nx
    import tkinter as tk
    from nobvisual.tkinter_circlify import tkcirclify
    from nobvisual.circlifast import circlifast
    from nobvisual.colorize import color_by_name_pattern, color_by_value
    from nobvisual.helpers import from_circlify_to_nobvisual
    from maraudersmap.show_nobvisual import ntw_nobvisual
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)
    # Select source
    if colorby in ["file_complexity", "file_size", "file_patterns"]:
        func_tree = Path(param["package"]) / "file_tree.json"
    elif colorby == "score":
        func_tree = Path(param["package"]) / "func_tree_score.json"
    else:
        func_tree = Path(param["package"]) / "func_tree.json"

    if not func_tree.exists():
        logger.warning(
            f"Tree {str(func_tree)} is missing. Use `mmap tree` to create it."
        )
    with open(func_tree, "r") as fin:
        nld = json.load(fin)
    cgs_nx = nx.node_link_graph(nld)
    nobj = ntw_nobvisual(cgs_nx)

    if colorby in ["patterns", "file_patterns"]:
        legend = [(f"*{key}*", value) for key, value in param["color_rules"].items()]
        color_by_name_pattern(nobj, legend)
    elif colorby in ["complexity", "file_complexity"]:
        legend = color_by_value(nobj, "ccn", tolcmap="BuRd", logarithmic=True)
    elif colorby == "score":
        legend = color_by_value(nobj, "score", tolcmap="YlOrBr")
    elif colorby in ["size", "file_size"]:
        legend = color_by_value(nobj, "size", tolcmap="rainbow_PuRd", logarithmic=False)
    else:
        logger.warning(f"color by {colorby} is not an option")

    circles = circlifast(nobj, show_enclosure=False)
    draw_canvas = tkcirclify(from_circlify_to_nobvisual(circles), legend=legend)
    draw_canvas.show_names(level=2)
    tk.mainloop()


main_cli.add_command(showtree)


# @click.command()
# @click.argument("macro_graph", type=str)
# @click.option(
#     "--file",
#     "-f",
#     type=str,
#     default="./coverage.json",
#     help="Coverage json file from gcov",
# )
# def coverage_tree(macro_graph, file):
#     """Dump .json of mmap coverage macro tree graph."""
#     import json
#     from networkx import node_link_data, node_link_graph
#     from json import dump as jdump
#     from maraudersmap.coverage import get_coverage_tree

#     with open(macro_graph, "r") as fin:
#         nld = json.load(fin)
#     macro_graph = node_link_graph(nld)

#     coverage_graph = get_coverage_tree(macro_graph, file)

#     with open(f"coverage_tree.json", "w") as fout:
#         jdump(node_link_data(coverage_graph), fout, indent=4, sort_keys=True)

#     logger.success(f"Generating coverage_tree.json, use show command to see your results.")


# main_cli.add_command(coverage_tree)


# @click.command()
# @click.option(
#     "--file",
#     "-f",
#     type=str,
#     default="./mmap_in.yml",
#     help="Input file with a custom name (.yml)",
# )
# @click.option(
#     "-v",
#     "--verbose",
#     is_flag=True,
#     show_default=True,
#     default=False,
#     help="Verbose mode",
# )
# def imports(file, verbose):
#     """Create the MMAP import graph of functions

#     Need the MMAP Control file to find the sources,
#     """
#     import os
#     from maraudersmap.imports import get_importsgraph
#     from networkx import node_link_data
#     from json import dump as jdump
#     from maraudersmap.mmap_startlog import mmap_startlog

#     mmap_startlog(verbose)

#     param = prepare_cmd(file)

#     wkdir = os.getcwd()

#     imports_graph = get_importsgraph(
#         os.path.join(wkdir, param["path"]),
#         param["package"],
#         # tree_graph
#     )
#     outdir = ensure_dir(param["package"])
#     with open(outdir / "imports.json", "w") as fout:
#         jdump(node_link_data(imports_graph), fout, indent=4, sort_keys=True)

#     logger.success(f"Generating {param['package']}/imports.json.")


# main_cli.add_command(imports)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def cg_gen(file, verbose):
    """Gen callgraph ddb of a project defined mmap_in.yml"""
    from json import dump as jdump
    from maraudersmap.callgraph import get_callgraph
    from networkx import node_link_data
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)
    param = prepare_cmd(file)
    callgraph = get_callgraph(
        param["path"],
        param["context"],
    )
    outdir = ensure_dir(param["package"])
    with open(outdir / "callgraph.json", "w") as fout:
        jdump(node_link_data(callgraph), fout, indent=4, sort_keys=True)
    logger.success(f"Generating {param['package']}/callgraph.json.")


main_cli.add_command(cg_gen)


@click.command()
@click.argument("file",
    nargs=1,
    type=str,
)
@click.option(
    "--backend",
    "-b",
    type=click.Choice(["pydot", "pyplot", "plotly", "pyvis"]),
    default="pyvis",
    help="Backend for rendering",
)
@click.option(
    "--merge",
    "-m",
    is_flag=True,
    show_default=True,
    default=False,
    help="""Merge childs of containers (reduce graph)

\b  
    Each container will merge its childs eg:
    - methods  merged in their object
    - subroutines  merged in their module

    This makes graphs easier to read and faster to render.
        
""",
)
@click.option(
    "--color",
    "-c",
    type=click.Choice(
        [
            "type",
            "lang",
            "cplx",
            "lvl",
        ]
    ),
    default="type",
    help="""Coloring strategy

\b  
    type : by type (subroutine, method, object)
    lang : by language (fortran, cpp, c, python)
    cplx : by complexity 
    lvl  : by API lvl (0 - low level, 1- high level)
    ptn  : by the patterns in the mmap_in.yml 

    
""",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
@click.option(
    "-l",
    "--load",
    is_flag=True,
    show_default=True,
    default=False,
    help="Load result in default webbrowser",
)
def cg_fast(file, backend, merge, color, verbose,load):
    """
    Fast Gen.& Visualize callgraph on single file (no mmap_in.yml)
    """
    from maraudersmap.callgraph import get_callgraph
    from maraudersmap.mmap_startlog import mmap_startlog
    from maraudersmap.full_graph_actions import  show_graph

    mmap_startlog(verbose)

    cgs_nx = get_callgraph(
        file,
        file,
    )

    show_graph(
        cgs_nx,
        backend=backend,
        color=color,
        patterns=None,
        remove_patterns=[],
        hyperconnect=10,
        subgraph_roots=None,
        merge=merge,
        load=load
    )
main_cli.add_command(cg_fast)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
@click.option(
    "--backend",
    "-b",
    type=click.Choice(["pydot", "pyplot", "plotly", "pyvis"]),
    default="pyvis",
    help="Backend for rendering",
)
@click.option(
    "--nocalls",
    "-n",
    is_flag=True,
    show_default=True,
    default=False,
    help="Remove Calls from callgraph (structure only)",
)
@click.option(
    "--merge",
    "-m",
    is_flag=True,
    show_default=True,
    default=False,
    help="""Merge childs of containers (reduce graph)

\b  
    Each container will merge its childs eg:
    - methods  merged in their object
    - subroutines  merged in their module

    This makes graphs easier to read and faster to render.
        
""",
)
@click.option(
    "--color",
    "-c",
    type=click.Choice(
        [
            "type",
            "lang",
            "cplx",
            "lvl",
            "ptn",
        ]
    ),
    default="type",
    help="""Coloring strategy

\b  
    type : by type (subroutine, method, object)
    lang : by language (fortran, cpp, c, python)
    cplx : by complexity 
    lvl  : by API lvl (0 - low level, 1- high level)
    ptn  : by the patterns in the mmap_in.yml 

    
""",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
@click.option(
    "-l",
    "--load",
    is_flag=True,
    show_default=True,
    default=False,
    help="Load result in default webbrowser",
)
def cg_show(file, backend, merge, color,nocalls, verbose,load):
    """Visualize callgraph on a project defined in mmap_in.yml"""
    import json
    from pathlib import Path
    import networkx as nx
    from maraudersmap.full_graph_actions import  show_graph
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)
    #load files
    param = prepare_cmd(file)
    graph_json = Path(param["package"]) / "callgraph.json"
    with open(graph_json, "r") as fin:
        nld = json.load(fin)
    cgs_nx = nx.node_link_graph(nld)
    # visualise
    show_graph(
        cgs_nx,
        backend=backend,
        color=color,
        patterns=param["color_rules"],
        remove_patterns=param["clean_graph"].get("remove_patterns", []),
        hyperconnect=param["clean_graph"].get("remove_hyperconnect", 5),
        subgraph_roots=param["clean_graph"].get("subgraph_roots", []),
        merge=merge,
        nocalls=nocalls,
        load=load
    )
main_cli.add_command(cg_show)


########################################################
####################### UTILITIES ######################
########################################################


def dump_json(nx_data, type_):
    import json
    from networkx import node_link_data

    fname = f"mmap_{type_}_graph.json"
    with open(fname, "w") as fout:
        json.dump(node_link_data(nx_data), fout, indent=4, sort_keys=True)
    logger.info(f"Graph dumped as {fname}")


def prepare_cmd(file) -> dict:
    """Read and check the control file of MMAP."""
    from yaml import safe_load
    from pathlib import Path

    ctrl_file = Path(file)
    if not ctrl_file.exists():
        logger.warning(
            f"File {file} does not exist. Use  >mmap anew  to create a new one"
        )

    with open(file, "r") as fin:
        param = safe_load(fin)

    if param is None:
        raise RuntimeError(f"No parameters found in {file}")

    tgt = Path(param["path"])
    if not tgt.exists():
        raise RuntimeError(f"Path {param['path']} not found")

    if "context" not in param:
        param["context"] = param["path"]

    return param


def ensure_dir(dir):
    """As name says

    So short we could remove it."""
    from pathlib import Path

    outdir = Path.cwd().absolute() / dir
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir
