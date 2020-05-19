import scala.Tuple2;

import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.apache.spark.sql.types.StringType;
import org.apache.spark.sql.types.IntegerType;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.regex.Pattern;
//import java.util.function.Function;

public final class MP3_PartD {

  public static void main(String[] args) throws Exception {
    SparkSession spark = SparkSession
      .builder()
      .appName("MP3")
      .getOrCreate();
    JavaSparkContext sc = new JavaSparkContext(spark.sparkContext());
    SQLContext sqlContext = new SQLContext(sc);
    /*
     * 1. Setup (10 points): Download the gbook file and write a function 
     * to load it in an RDD & DataFrame
     */
    
    // RDD API
    // Columns: 0: place (string), 1: count1 (int), 2: count2 (int), 3: count3 (int)


    // Spark SQL - DataSet API


    /*
     * 4. MapReduce (10 points): List the three most frequent 'word' with their count 
     * of appearances
     */

    // Dataset/Spark SQL API


    spark.stop();
    sc.stop();
  }
}
