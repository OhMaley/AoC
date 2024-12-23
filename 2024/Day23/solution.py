import networkx as nx
from networkx import Graph
from typing import List, Tuple, Dict, Set


def get_graph_from_input_file(file_path: str) -> Dict[str, List[str]]:
    with open(file_path, "r") as file:
        graph_dict = {}
        for connection in file.read().strip().splitlines():
            node1, node2 = connection.split("-")
            if node1 not in graph_dict:
                graph_dict[node1] = []
            graph_dict[node1].append(node2)
            if node2 not in graph_dict:
                graph_dict[node2] = []
            graph_dict[node2].append(node1)
        return graph_dict


def get_triangles_from_graph(graph: Graph) -> Set[Tuple[str]]:
    triangles = set()
    for node in graph.nodes():
        neighbors = set(graph[node])
        for neighbor in neighbors:
            common_neighbors = neighbors & set(graph[neighbor])
            for common_neighbor in common_neighbors:
                triangle = tuple(sorted((node, neighbor, common_neighbor)))
                triangles.add(triangle)
    return triangles


if __name__ == "__main__":
    # Get the graph from the file
    graph_dict = get_graph_from_input_file("./input.txt")

    # Construct the NetworkX graph
    graph = nx.Graph()
    for node, neighbors in graph_dict.items():
        for neighbor in neighbors:
            graph.add_edge(node, neighbor)

    # Find triangles in the network
    triangle_counts = nx.triangles(graph)
    total_triangles = sum(triangle_counts.values()) // 3
    print(f"There are a total of {total_triangles} triangles in this graph")
    # Actually get those triangles
    triangles = get_triangles_from_graph(graph)
    # Filter to only keep those starting with the letter 't'
    filtered_triangles = [
        triangle for triangle in triangles if any(n.startswith("t") for n in triangle)
    ]
    print("Triangles including a node starting with 't':", len(filtered_triangles))

    # Find the largest clique
    cliques = list(nx.find_cliques(graph))
    largest_clique = max(cliques, key=len)
    print("Largest clique:", largest_clique)
    password = ",".join(sorted(largest_clique))
    print(f"Password is {password}")
