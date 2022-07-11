# covid-dashboard-unitn
Big data technologies project @ Unitn 

Design and implement a big data system for short- and mid-term predictions (daily, up to 14 days) of COVID-relevant metrics (new cases, hospitalization, ICUs, deaths etc.) in the various regions of Italy.

# data sources
[stats by region](https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni)

[regions and age](https://github.com/pcm-dpc/COVID-19/blob/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv)

# Repository structure 
we decided to adopt a modular approach in order to have a cleaner and more manageble project, the backend could be logically divided in two buckets: 
- **ingestion**: from the raw data source to a database where to store the covid-relevant data 
- **computation**: get the data from the database and compute the models for the prediction 

We also decided to wrap all the project in a docker container to have a more reliable and deliverable product.

# Data ingestion
technologies used: kafka, postgresql 

This package is used to fetch the raw data from the github repository of the Protezione Civile, clean it and then save it on a postgresql database.

the two main actors of this package are the producer and the consumer, while the other files are modules containing the constants and the functions used.

## Producer
It uses pandas to create and modify a dataframe from a url, we decided to use this library because allowed us to easily handle csv data. The producer also shaped the 3 table that then will be saved from the consumer in the database, in fact the csv files are full of redundant data so we decided to create more tables with the essential data.

Then kafka is used to send the tables to the consumer and to start the computation, within the same topic we used different key-value pairs to separate the data:

- `key:info ` : used to send the header of the table (column names and data types
- `key:<table name>`: used to send table rows 
- `key:finish` : used to notify the end of a table 
- `key:compute` : used to fire the computation ( more in the computation section)

The process of fetching and sending the data is made first for all the past data and then everyday thw new data is fetched and the tables updated 

## Consumer
It's always listeing for a message from the producer, when the info of a table arrives creates a new table and fill it as the rows arrives, it is unaware of how the data is gathered, its only job is to save the data that arrives in the database.

# computation
technologies used: sparq, mongodb 

The computation part takes the data from the postgresql database, using spark to compute the models and then save the models on a mongodb.

## prediction
Currently a linear regression using data from the past week is implemented to do the prevision, this is just the simplest one. More complex models could be used to have a better accuracy such as [this](https://www.sciencedirect.com/science/article/pii/S2213398421001615) and 
[this](https://github.com/AlessandroMinervini/COVID-19-forecasting)



# Run the project 

```
docker compose up -d   
```





