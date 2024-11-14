import requests
import networkx as nx
import matplotlib.pyplot as plt

def get_dependencies(package_name):
    """Fetches dependencies for a given package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        requires_dist = data['info'].get('requires_dist', [])
        dependencies = [req.split()[0] for req in requires_dist if req]
        return dependencies
    else:
        return []

def build_dependency_graph(package_name, max_depth=2):
    """Builds a dependency graph using NetworkX."""
    G = nx.DiGraph()
    to_visit = [(package_name, 0)]
    visited = set()

    while to_visit:
        current_package, depth = to_visit.pop(0)
        if current_package not in visited and depth <= max_depth:
            visited.add(current_package)
            dependencies = get_dependencies(current_package)
            for dep in dependencies:
                G.add_edge(current_package, dep)
                to_visit.append((dep, depth + 1))
    
    return G

def draw_graph(G):
    """Draws the graph using Matplotlib."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.show()

if __name__ == "__main__":
    package_name = "requests"  # Example package
    graph = build_dependency_graph(package_name)
    draw_graph(graph)