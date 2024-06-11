"""Main function used to compute the imports graph for either fortran or python code."""
from pathlib import Path
import networkx as nx
from loguru import logger

from maraudersmap.macro_tree import get_macro_tree
from maraudersmap.tree import add_void_node

from tucan.imports_main import imports_main


def add_import_graph_nodes(
    imports_dict: dict, macro_tree_graph: nx.DiGraph
) -> nx.DiGraph:
    """
    Add nodes for the import graph relative to the nodes in the tree.
    If the import detected is not a tree node, the node wont be added for the moment.

    Args:
        imports_dict (dict): Dict with the module or function name associated with its various imports.
        macro_tree_graph (nx.DiGraph): NetworkX of the macro_tree_graph

    Returns:
        nx.DiGraph: Imports graph with its various node unconnected yet.
    """

    importsgraph = nx.DiGraph()
    for mod_ref in imports_dict.keys():
        imports = imports_dict[mod_ref]

        for node in macro_tree_graph.nodes():
            if (
                mod_ref in macro_tree_graph.nodes[node]["path"]
                and macro_tree_graph.nodes[node]["name"] not in importsgraph.nodes()
            ):
                importsgraph.add_node(
                    macro_tree_graph.nodes[node]["name"],
                    size=macro_tree_graph.nodes[node]["size"],
                    ccn=macro_tree_graph.nodes[node]["ccn"],
                    imports=imports,
                )
                logger.debug(
                    f"Adding node {macro_tree_graph.nodes[node]['name']} to imports graph"
                )

    return importsgraph


def build_importsgraph(imports_dict: dict, macro_tree_graph: nx.DiGraph) -> nx.DiGraph:
    """
    Create the networkX graph from the data computed in the previous functions.

    Args:
        imports_dict (dict): Dict with the module or function name associated with its various imports.
        macro_tree_graph (obj): NetworkX of the macro_tree_graph

    Returns:
        importsraph (obj): NetworkX DiGraph corresponding to the imports_graph.
    """
    imports_graph = add_import_graph_nodes(imports_dict, macro_tree_graph)

    # Add imports edges
    enhanced_imports_graph = imports_graph.copy()
    for import_node in imports_graph.nodes():
        for module_from, _ in imports_graph.nodes[import_node]["imports"].items():
            module_path = module_from.replace(".", "/")  # Useful for python imports
            mod_added = False

            for file_node in macro_tree_graph.nodes():
                if file_node.endswith(module_path) or module_path + "." in file_node:
                    # First condition for folder oriented imports
                    # Second condition for file oriented imports
                    if (
                        macro_tree_graph.nodes[file_node]["name"]
                        not in enhanced_imports_graph.nodes()
                    ):
                        enhanced_imports_graph.add_node(
                            macro_tree_graph.nodes[file_node]["name"],
                            size=macro_tree_graph.nodes[file_node]["size"],
                            ccn=macro_tree_graph.nodes[file_node]["ccn"],
                        )
                    enhanced_imports_graph.add_edge(
                        import_node, macro_tree_graph.nodes[file_node]["name"]
                    )
                    logger.debug(
                        f"Adding edge between {import_node} -> {macro_tree_graph.nodes[file_node]['name']}"
                    )
                    mod_added = True
                    break

            if not mod_added:
                if module_path not in imports_graph.nodes():
                    add_void_node(enhanced_imports_graph, module_from, None)
                    logger.debug(
                        f"Node not in database, adding void node {module_path}"
                    )
                enhanced_imports_graph.add_edge(import_node, module_path)
                logger.debug(f"Edge added between {import_node} --> {module_path}")

    return enhanced_imports_graph


def get_importsgraph(
    path: str,
    code_name: str,
) -> nx.DiGraph:
    """
    Main function that builds the network X tree graph, this can show the graph with nobvisual
    and / or pyvis.

    Args:
        path (str): Path to the root folder of the code or file
        code_name (str): Name of the code

    Returns:
        graph (obj): NetworkX of the imports_graph
    """
    macro_graph = get_macro_tree(path, code_name)

    imports_dict = {}
    for macro_node in macro_graph.nodes():
        if Path(macro_graph.nodes[macro_node]["path"]).is_file():
            imports_dict.update(imports_main(macro_graph.nodes[macro_node]["path"]))

    logger.info("Generating imports database")
    imports_graph = build_importsgraph(imports_dict, macro_graph)
    logger.info("Imports graph generated")
    return imports_graph
