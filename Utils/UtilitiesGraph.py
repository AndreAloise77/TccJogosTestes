from graphviz import Digraph

# CONSTANTS TO CREATE NODE AND EDGE ON DIGRAPH
GRAPH_EDGE_STYLE_BOLD: str = 'bold'
GRAPH_EDGE_CONSTRAINT_TRUE: str = 'true'
COMMA_WITH_RESPAWNED_INDICATOR: str = ', Resp'
FREQUENCY_TEXT_TO_GRAPH: str = 'Freq: {}'
COLOR_RED: str = 'red'
COLOR_BLACK: str = 'black'
GRAPH_EDGE_STYLE_DASHED: str = 'dashed'


def create_colored_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str,
                            edge_color: str, is_respawn: bool):
    frequency_text: str = FREQUENCY_TEXT_TO_GRAPH.format(frequency)
    if is_respawn:
        frequency_text = frequency_text + COMMA_WITH_RESPAWNED_INDICATOR
        dot.edge(source_node, target_node, frequency_text,
                 color=edge_color, constraint=GRAPH_EDGE_CONSTRAINT_TRUE, style=GRAPH_EDGE_STYLE_BOLD)
    else:
        dot.edge(source_node, target_node, frequency_text,
                 color=edge_color, constraint=GRAPH_EDGE_CONSTRAINT_TRUE)


def create_invalid_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str):
    frequency_text: str = FREQUENCY_TEXT_TO_GRAPH.format(frequency)
    dot.edge(source_node, target_node, frequency_text, color=COLOR_RED, constraint=GRAPH_EDGE_CONSTRAINT_TRUE,
             style=GRAPH_EDGE_STYLE_DASHED)


def create_colorless_dot_edge(dot: Digraph, frequency: int, source_node: str, target_node: str):
    frequency_text: str = FREQUENCY_TEXT_TO_GRAPH.format(frequency)
    dot.edge(source_node, target_node, frequency_text, color=COLOR_BLACK, constraint=GRAPH_EDGE_CONSTRAINT_TRUE)
