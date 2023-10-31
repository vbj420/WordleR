def create_graph(vertices, edges, weights):
    graph = {}
    for vertex in vertices:
        graph[vertex] = []

    for edge, weight in zip(edges, weights):
        u, v = edge
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return graph

def find_longest_path(graph, source, destination, visited, current_path):
    visited[source] = True
    current_path.append(source)

    if source == destination:
        return current_path

    longest_path = None

    for neighbor, weight in graph[source]:
        if not visited[neighbor]:
            path = find_longest_path(graph, neighbor, destination, visited, current_path[:])
            if path is not None and (longest_path is None or len(path) > len(longest_path)):
                longest_path = path

    return longest_path

def main():
    vertices = set(input("Enter vertices (space-separated): ").split())
    edges = set()
    weights = []
    while True:
        edge_input = input("Enter an edge (u v) and its weight (or type 'done' to finish): ")
        if edge_input.lower() == 'done':
            break
        else:
            u, v, weight = edge_input.split()
            if (u, v) not in edges and (v, u) not in edges:  # Check for duplicate edges
                edges.add((u, v))
                weights.append(int(weight))
            else:
                print("Duplicate edges not allowed")

    graph = create_graph(vertices, list(edges), weights)
    source = input("Enter the source vertex: ")
    destination = input("Enter the destination vertex: ")

    if source in vertices and destination in vertices:
        visited = {vertex: False for vertex in vertices}
        longest_path = find_longest_path(graph, source, destination, visited, [])
        if longest_path:
            print(f"Longest path from {source} to {destination}: {' -> '.join(longest_path)}")
        else:
            print(f"No path exists from {source} to {destination}.")
    else:
        print("Source or destination vertex not in the graph.")

if __name__ == "__main__":
    main()
