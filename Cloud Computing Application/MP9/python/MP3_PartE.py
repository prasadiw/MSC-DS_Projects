from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType

conf = SparkConf().set('spark.sql.broadcastTimeout','3000')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

####
# 1. Setup (10 points): Download the gbook file and write a function to load it in an RDD & DataFrame
####
lines = sc.textFile("gbooks")
parts = lines.map(lambda l: l.split())
gbooks = parts.map(lambda p: (p[0], int(p[1]), int(p[2]), int(p[3])))

# RDD API
# Columns:
# 0: place (string), 1: count1 (int), 2: count2 (int), 3: count3 (int)
fields = [
    StructField("word", StringType()),
    StructField("count1", IntegerType()),
    StructField("count2", IntegerType()),
    StructField("count3", IntegerType())
]
schema = StructType(fields)

# Spark SQL - DataFrame API
df = sqlContext.createDataFrame(gbooks, schema)

####
# 5. Joining (10 points): The following program construct a new dataframe out of 'df' with a much smaller size.
####
df2 = df.select("word", "count1").distinct().limit(1000);
df2.createOrReplaceTempView('gbooks2')

# Now we are going to perform a JOIN operation on 'df2'. Do a self-join on 'df2' in lines with the same #'count1' values and see how many lines this JOIN could produce. Answer this question via DataFrame API and #Spark SQL API
# Spark SQL API

sqlDF = sqlContext.sql("SELECT t1.word, t2.word FROM gbooks2 as t1, gbooks2 as t2 WHERE t1.count1 = t2.count1")
print(sqlDF.count())

# output: 9658

