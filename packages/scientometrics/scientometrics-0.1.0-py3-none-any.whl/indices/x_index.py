#calculate the x-index for an edge-list of keywords and their citations

from typing import List
import networkx as nx
import pandas as pd


def x_index(edge_list: List) -> int:
    """
    Calculate the x-index for a given edge list of entities and their citations/scores.

    Args:
        edge_list (List): A list of edges where each edge is a tuple of 3 elements: (source/article ID, target entity, weight/ citation count)

    Returns:
        int: The x-index value for the given edge list.
    """
    G = nx.DiGraph()
    for edge in edge_list:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    x_index = 0
    key_list = [i[1] for i in edge_list]
    # remove duplicates
    key_list = list(dict.fromkeys(key_list))
    # for each keyword in key_list, get their indegree
    temp = []
    for key in key_list:
        deg = G.in_degree(key, weight='weight')
        temp.append([key, deg])
    df = pd.DataFrame(temp, columns=['keyword', 'indegree'])
    df = df.sort_values(by='indegree', ascending=False)
    df['rank'] = range(1, len(df) + 1)
    df['crr'] = df['indegree'] / df['rank']

    # x-index would be the maximum rank where crr is greater than or equal to 1
    x_index = df[df['crr'] >= 1].shape[0]
    return x_index


# Path: scientometrics/indices/x_index.py
