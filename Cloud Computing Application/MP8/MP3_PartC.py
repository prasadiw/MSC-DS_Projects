from pyspark import SparkContext, SQLContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType

sc = SparkContext()
sqlContext = SQLContext(sc)

####
# 1. Setup (10 points): Download the gbook file and write a function to load it in an RDD & DataFrame
####

lines = sc.textFile("gbooks", 1)
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
# 3. Filtering (10 points) Count the number of appearances of word 'ATTRIBUTE'
####

df.createOrReplaceTempView("gbooks")

# Spark SQL

sqlDF = sqlContext.sql("SELECT count(1) FROM gbooks WHERE word = 'ATTRIBUTE'")
sqlDF.show()

# +--------+
# |count(1)|
# +--------+
# |     201|
# +--------+


