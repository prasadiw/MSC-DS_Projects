from pyspark import *
from pyspark.sql import SparkSession
from graphframes import *

sc = SparkContext()
spark = SparkSession.builder.appName('fun').getOrCreate()


def get_shortest_distances(graphframe, dst_id):
    # Find shortest distances in the given graphframe to the vertex which has id `dst_id`
    # The result is a dictionary where key is a vertex id and the corresponding value is
    # the distance of this node to vertex `dst_id`.
    distances = {}
    rows = graphframe.shortestPaths(landmarks=[dst_id]).collect()
    for row in rows:
        distance = row[1][dst_id] if dst_id in row[1] else -1
        distances[row[0]] = distance
    return distances


if __name__ == "__main__":
    vertex_list = []
    edge_list = []
    with open('dataset/graph.data') as f:
        for line in f:
            # TODO: Parse line to get vertex id
            tokens = line.split()
            src = tokens[0]
            # TODO: Parse line to get ids of vertices that src is connected to
            dst_list = tokens[1:]
            vertex_list.append((src,))
            edge_list += [(src, dst) for dst in dst_list]

    vertices = spark.createDataFrame(vertex_list, ["id"]) # TODO: Create dataframe for vertices
    edges = spark.createDataFrame(edge_list, ["src", "dst"])  # TODO: Create dataframe for edges

    g = GraphFrame(vertices, edges)
    sc.setCheckpointDir("/tmp/shortest-paths")

    # We want the shortest distance from every vertex to vertex 1
    for k, v in get_shortest_distances(g, '1').items():
        print(k, v)
