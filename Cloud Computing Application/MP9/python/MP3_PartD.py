from pyspark import SparkContext, SQLContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType

sc = SparkContext()
sqlContext = SQLContext(sc)

####
# 1. Setup (10 points): Download the gbook file and write a function to load it in an RDD & DataFrame
####

lines = sc.textFile("gbooks", 10)
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
# 4. MapReduce (10 points): List the three most frequent 'word' with their count of appearances
####

df.createOrReplaceTempView("gbooks")

# Spark SQL

sqlDF = sqlContext.sql("SELECT word, count(1) FROM gbooks GROUP BY word ORDER BY count(1) DESC")
sqlDF.show(n=3)

# There are 18 items with count = 425, so could be different 
# +---------+--------+
# |     word|count(1)|
# +---------+--------+
# |  all_DET|     425|
# | are_VERB|     425|
# |about_ADP|     425|
# +---------+--------+

