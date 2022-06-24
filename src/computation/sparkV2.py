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
df_stats = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "stats").load()
df_regions = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "regions").load()
df_age = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "age").load()

# %% prepare data for regression

df = df_stats.select(df_stats['date'], df_stats['region_id'], df_stats['total_cases'])
df = df.withColumn('date', df['date'].cast('date'))# cast date to date type

min_date = df.agg({"date": "min"}).collect()[0][0] # get max date 
max_date = df.agg({"date": "max"}).collect()[0][0] # get min date 

df = df.withColumn('time_passed', datediff(col('date'), lit(min_date))) # get time passed since start of the pandemic
df = df.filter(df['date'] >= max_date - timedelta(days=7))# select only data from the last week

#df = df.filter(df['region_id'] == 1)

assembler = VectorAssembler(
    inputCols=["time_passed"],
    outputCol="features")

df = assembler.transform(df)

# %% fit regression model 


lr = LinearRegression(featuresCol = 'features', labelCol='total_cases',maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(df)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))
# %%
# make linear regression grouped by region

import statsmodels.api as sm
import pandas as pd
# df has four columns: id, y, x1, x2

group_column = 'region_id'
y_column = 'total_cases'
x_columns = ['time_passed']
schema = df.select(group_column, *x_columns).schema

@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
# Input/output are both a pandas.DataFrame
def ols(pdf):
    group_key = pdf[group_column].iloc[0]
    y = pdf[y_column]
    X = pdf[x_columns]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model)
    return pd.DataFrame([[group_key] + [model.params[i] for i in   x_columns]], columns=[group_column] + x_columns)

beta = df.groupby(group_column).apply(ols)


# %%
import pandas as pd
from pyspark.sql.functions import pandas_udf, PandasUDFType

def linear_reg(pdf: pd.DataFrame) -> pd.DataFrame:
    lr = LinearRegression(featuresCol = 'features', labelCol='total_cases',maxIter=10, regParam=0.3, elasticNetParam=0.8)

    lrModel = lr.fit(df)
    return pd.DataFrame([1,2,3,4])

df.groupby(group_column).applyInPandas(linear_reg, schema=df.schema).show()

# %%
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
# Input/output are both a pandas.DataFrame
def ols(pdf):
    group_key = pdf[group_column].iloc[0]
    y = pdf[y_column]
    X = pdf[x_columns]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    return pd.DataFrame([[group_key] + [model.params[i] for i in   x_columns]], columns=[group_column] + x_columns)

beta = df.groupby(group_column).apply(ols)

# %%
