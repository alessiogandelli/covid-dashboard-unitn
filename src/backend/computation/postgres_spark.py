#%%
from pyspark.sql import SparkSession
import os

spark = SparkSession \
    .builder \
    .master("local")\
    .appName("covid-dashboard") \
    .config("spark.jars", "{}/postgresql-42.4.0.jar".format(os.getcwd())) \
    .config("spark.executor.extraClassPath", "{}/postgresql-42.4.0.jar".format(os.getcwd())) \
    .getOrCreate()
# %%

# %%

df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://db:5432/covid") \
    .option("dbtable", "stats") \
    .option("user", "user") \
    .option("password", "example") \
    .option("driver", "org.postgresql.Driver") \
    .load()