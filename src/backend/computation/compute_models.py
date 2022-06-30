# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import timedelta
import os
from confluent_kafka import Consumer, OFFSET_BEGINNING
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
import db_helper
import logging

logging.basicConfig(filename='flow.log', level=logging.DEBUG, format='%(asctime)s:%(process)d:%(levelname)s:%(message)s')


# note this will not work if the sqlite-jdbc jar file and the sqlite one are not in the same folder from where you launch
# spark = SparkSession.builder.master("local").appName("SQLite JDBC").config(
#     "spark.jars",
#     "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).config(
#     "spark.driver.extraClassPath",
#     "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).getOrCreate()

spark = SparkSession \
    .builder \
    .master("local")\
    .appName("covid-dashboard") \
    .config("spark.jars", "{}/postgresql-42.4.0.jar".format(os.getcwd())) \
    .config("spark.executor.extraClassPath", "{}/postgresql-42.4.0.jar".format(os.getcwd())) \
    .getOrCreate()
# %%




#load data in a spark-friendly way ( using spark dataframes )
def fetch_data():
    db = spark.read.format("jdbc").option("url", "jdbc:postgresql://localhost:5432/covid") \
    .option("user", "user").option("password", "example").option("driver", "org.postgresql.Driver")
    df_stats = db.option("dbtable", "stats").load()       # load stats data
    df_regions = db.option("dbtable", "regions").load()     # load regions data
    df_age = db.option("dbtable", "age").load()         # load age data
    return df_stats, df_regions, df_age

# prepare data for regession
def prepare_data(df_stats, y):

    # select only relevant columns ( date, region_id, total_cases )
    df = df_stats.select('date', 'region_id', *y)
    df = df.withColumn('date', df['date'].cast('date'))    # cast date to date type

    min_date = df.agg({"date": "min"}).collect()[0][0]  # get max date
    max_date = df.agg({"date": "max"}).collect()[0][0]  # get min date

    df = df.withColumn('time_passed', datediff(col('date'), lit(min_date)))    # get time passed since start of the pandemic
    df = df.filter(df['date'] >= max_date - timedelta(days=7))    # select only data from the last week


    # create data in the format required by the LinearRegression model
    assembler = VectorAssembler(
        inputCols=["time_passed"],
        outputCol="features")

    df = assembler.transform(df)
    
    
    return df
# 
# perform linear regression on all the regions and save the model


def compute():
    df_stats, df_regions, df_age = fetch_data()
    logging.info('fetched data')
    labels = ['total_cases', 'intensive_care', 'hospitalized', 'domestic_isolation', 'deaths']

    df = prepare_data(df_stats, labels)
    logging.info('prepared data')

    regions_ids = df.select('region_id').distinct().rdd.map( lambda x: x[0]).collect()
    last_day = df.agg({"time_passed": "max"}).collect()[0][0] 
    for i in regions_ids:

        # subset data for a single region
        df1 = df.filter(df['region_id'] == i)

        for y in labels:

            lr = LinearRegression(featuresCol='features', labelCol=y, maxIter=10, regParam=0.3, elasticNetParam=0.8)
            lrModel = lr.fit(df1)

            model = {'name': y,
                     'day': last_day,
                     'region_id': i,
                     'intercept': lrModel.intercept,
                     'coefficients': lrModel.coefficients.toArray().tolist()}

            db_helper.save_model(model)
    logging.info('computed today for all regions')


# %%
config_consumer = {'bootstrap.servers': 'localhost:9092',
                   'group.id': 'python_example_group_1',
                   'auto.offset.reset': 'earliest'}
consumer = Consumer(config_consumer)
consumer.subscribe(['covid'])

print('listening..')

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        pass
    else:
        
        if msg.key().decode('utf-8') == 'compute':
            compute()
            print('computed', )
            logging.info('computed')



# %%

labels = ['total_cases', 'intensive_care', 'hospitalized', 'domestic_isolation', 'deaths']
# %%


# %%
