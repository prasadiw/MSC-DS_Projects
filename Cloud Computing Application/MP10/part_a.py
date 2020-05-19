from pyspark import *
from pyspark.sql import SparkSession
from graphframes import *

sc = SparkContext()
spark = SparkSession.builder.appName('fun').getOrCreate()


def get_connected_components(graphframe):
    components = {}
    rows = graphframe.connectedComponents().collect()
    for row in rows:
        component = row[1]
        if component not in components:
            components[component] = []
        components[component].append(row[0])

    return [v for v in components.values()]


if __name__ == "__main__":
    vertex_list = []
    edge_list = []
    with open('dataset/graph.data') as f:  # Do not modify
        for line in f:
            tokens = line.split()
            src = tokens[0]
            dst_list = tokens[1:]
            vertex_list.append((src,))
            edge_list += [(src, dst) for dst in dst_list]

    vertices = spark.createDataFrame(vertex_list, ["id"])
    edges = spark.createDataFrame(edge_list, ["src", "dst"])

    g = GraphFrame(vertices, edges)
    sc.setCheckpointDir("/tmp/connected-components")

    result = get_connected_components(g)
    for line in result:
        print(' '.join(line))
