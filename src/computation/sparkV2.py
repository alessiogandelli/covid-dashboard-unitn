#%%
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.pandas as ps
from datetime import timedelta
import os

# note this will not work if the sqlite-jdbc jar file and the sqlite one are not in the same folder from where you launch
spark = SparkSession.builder.master("local").appName("SQLite JDBC").config(
        "spark.jars",
        "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).config(
        "spark.driver.extraClassPath",
        "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).getOrCreate()


#%% load data in a spark-friendly way ( using spark dataframes )
df_stats = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "stats").load()
df_regions = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "regions").load()
df_age = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "age").load()

# %%
# our goal is to predict the number of cases in a region in a short term, 
# we need only last week data to do that ( or maybe a different time frame )
# we should do the same thing for different metrics, for simplicity we start 
# with total cases and deaths 

# select only interesting columns 

df = df_stats.select(df_stats['date'], df_stats['region_id'], df_stats['total_cases'])

# cast date to date type
df = df.withColumn('date', df['date'].cast('date'))


## get max date
min_date = df.agg({"date": "min"}).collect()[0][0]
max_date = df.agg({"date": "max"}).collect()[0][0]

df = df.withColumn('time_passed', datediff(col('date'), lit(min_date)))


# select only data from the last week
df = df.filter(df['date'] >= max_date - timedelta(days=7))


# select only data from region 1
df = df.filter(df['region_id'] == 1)


df
# %%
# edit df for ml spark format with vectorUDT
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

assembler = VectorAssembler(
    inputCols=["time_passed"],
    outputCol="features")

df = assembler.transform(df)

lr = LinearRegression(featuresCol = 'features', labelCol='total_cases',maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(df)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))
# %%
