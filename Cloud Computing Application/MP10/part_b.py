from pyspark import SparkContext
from numpy import array
from pyspark.mllib.clustering import KMeans, KMeansModel

############################################
#### PLEASE USE THE GIVEN PARAMETERS     ###
#### FOR TRAINING YOUR KMEANS CLUSTERING ###
#### MODEL                               ###
############################################

NUM_CLUSTERS = 4
SEED = 0
MAX_ITERATIONS = 100
INITIALIZATION_MODE = "random"

sc = SparkContext()


def get_clusters(data_rdd, num_clusters=NUM_CLUSTERS, max_iterations=MAX_ITERATIONS,
                 initialization_mode=INITIALIZATION_MODE, seed=SEED):
    # TODO:
    # Use the given data and the cluster pparameters to train a K-Means model
    # Find the cluster id corresponding to data point (a car)
    # Return a list of lists of the titles which belong to the same cluster
    # For example, if the output is [["Mercedes", "Audi"], ["Honda", "Hyundai"]]
    # Then "Mercedes" and "Audi" should have the same cluster id, and "Honda" and
    # "Hyundai" should have the same cluster id
    model_data = data_rdd.map(lambda x: x[1:])
    model = KMeans.train(
        model_data,
        num_clusters,
        maxIterations=max_iterations,
        initializationMode=initialization_mode,
        seed=seed)
    predictions = data_rdd.map(lambda x: convert_list(model, x)).collect()
    tmp = {}
    for prediction in predictions:
        if prediction[1] not in tmp:
            tmp[prediction[1]] = []
        tmp[prediction[1]].append(prediction[0])
    return [v for k, v in tmp.items()]


def convert_list(model, item):
    return item[0], model.predict(item[1:])


if __name__ == "__main__":
    f = sc.textFile("dataset/cars.data")

    # TODO: Parse data from file into an RDD
    data_rdd = f\
        .map(lambda x: x.split(",")) \
        .map(lambda x: [x[0],
                        float(x[1]),
                        float(x[2]),
                        float(x[3]),
                        float(x[4]),
                        float(x[5]),
                        float(x[6]),
                        float(x[7]),
                        float(x[8]),
                        float(x[9]),
                        float(x[10]),
                        float(x[11])]
             )
    clusters = get_clusters(data_rdd)

    for cluster in clusters:
        print(','.join(cluster))
