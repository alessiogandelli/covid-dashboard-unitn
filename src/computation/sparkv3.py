#%%
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.pandas as ps
from datetime import timedelta
import os
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

# note this will not work if the sqlite-jdbc jar file and the sqlite one are not in the same folder from where you launch
spark = SparkSession.builder.master("local").appName("SQLite JDBC").config(
        "spark.jars",
        "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).config(
        "spark.driver.extraClassPath",
        "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).getOrCreate()


#%% load data in a spark-friendly way ( using spark dataframes )
db =  spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite")
df_stats =   db.option("dbtable", "stats").load()       # load stats data
df_regions = db.option("dbtable", "regions").load()     # load regions data
df_age =     db.option("dbtable", "age").load()         # load age data

# %% prepare data

df = df_stats.select(df_stats['date'], df_stats['region_id'], df_stats['total_cases'])   # select only relevant columns ( date, region_id, total_cases )
df = df.withColumn('date', df['date'].cast('date'))                                      # cast date to date type

min_date = df.agg({"date": "min"}).collect()[0][0] # get max date 
max_date = df.agg({"date": "max"}).collect()[0][0] # get min date 

df = df.withColumn('time_passed', datediff(col('date'), lit(min_date)))                  # get time passed since start of the pandemic
df = df.filter(df['date'] >= max_date - timedelta(days=7)                                )# select only data from the last week

# create data in the format required by the LinearRegression model
assembler = VectorAssembler(
    inputCols=["time_passed"],
    outputCol="features")

df = assembler.transform(df)
# %%
