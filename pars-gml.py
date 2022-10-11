from pygmlparser.Parser import Parser
from pathlib import Path
from random import randint


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.nodes = len(matrix)


directory = './GML_files'
path_list = list(Path(directory).glob('*.gml'))
print(path_list)
topologies = []

for PATH in path_list:
    parser = Parser()
    parser.loadGML(path=PATH)
    parser.parse()

    nodes = parser.graph.graphNodes
    edges = parser.graph.graphEdges

    matrix = [[0] * len(nodes) for _ in range(len(nodes))]

    for edge in edges:
        matrix[edge.source][edge.target] = matrix[edge.target][edge.source] = randint(10, 50)

    density = 2 * len(edges) / (len(nodes) * len(nodes))

    topologies.append(
        {
            "path": PATH,
            "matrix": Matrix(matrix),
            "density": density,
        }
    )

topologies = sorted(topologies, key=lambda x: x["density"])

# print(*[topo["density"] for topo in topologies])
with open("density.txt", "w") as file:
    for topo in topologies:
        file.write(
            f"PATH={topo['path']}, nodes={topo['matrix'].nodes}, density={topo['density']}\n"
        )
