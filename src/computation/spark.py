#%%
from pyspark.sql import SparkSession
import pyspark.pandas as ps
import os

# note this will not work if the sqlite-jdbc jar file and the sqlite one are not in the same folder from where you launch
spark = SparkSession.builder.master("local").appName("SQLite JDBC").config(
        "spark.jars",
        "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).config(
        "spark.driver.extraClassPath",
        "{}/sqlite-jdbc-3.34.0.jar".format(os.getcwd())).getOrCreate()

# %%
df_case = spark.read.format("jdbc").option("url", "jdbc:sqlite:covid.sqlite").option("dbtable", "cases").load()

#parallelize computation based on the region
df_positive = df_case.groupBy(["date","region_id"]).sum("total_positive").alias("cases")

#split by region



# %%
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.linalg import Vectors

# Label points for regression
def groupid_to_feature(group_id, x, num_groups):
    intercept_id = num_groups + group_id-1
    # Need a vector containing x and a '1' for the intercept term
    return Vectors.sparse(num_groups*2, {group_id-1: x, intercept_id: 1.0})

labelled = df_positive.rdd.map(lambda line:LabeledPoint(line[2], groupid_to_feature(line[1], line[0], 21)))

labelled.take(5)
# %%

######################################### OTHER TRIAL
import statsmodels.api as sm
import pandas as pd
# df has four columns: id, y, x1, x2
url_tot = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'

df = pd.read_csv(url_tot)
group_column = 'denominazione_regione'
y_column = 'y'
x_columns = 'data'
schema = df.select(group_column, *x_columns).schema

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
