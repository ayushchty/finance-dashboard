from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *
import os

os.environ['HADOOP_HOME'] = os.path.abspath('hadoop')

spark = SparkSession.builder \
    .appName("FinanceETL") \
    .master("local[2]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED") \
    .config("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.security=ALL-UNNAMED") \
    .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow --add-opens java.base/java.lang=ALL-UNNAMED") \
    .getOrCreate()

df = spark.read.csv("data_lake/raw/1m_transactions.csv", header=True, inferSchema=True)

window_spec = Window.partitionBy("symbol").orderBy("timestamp")
features_df = df.withColumn("returns", 
    (col("price") - lag("price", 1).over(window_spec)) / lag("price", 1).over(window_spec)
).withColumn("hour", hour("timestamp"))

portfolio_summary = features_df.groupBy("user_id").agg(
    sum("amount").alias("total_spent"),
    avg("returns").alias("avg_return"),
    count("*").alias("txn_count")
)

os.makedirs("data_lake/processed/features", exist_ok=True)
os.makedirs("data_lake/processed/portfolio", exist_ok=True)

features_df.coalesce(1).toPandas().to_parquet("data_lake/processed/features/data.parquet")
portfolio_summary.toPandas().to_parquet("data_lake/processed/portfolio/summary.parquet")
print("Done")
spark.stop()
