# covid-dashboard-unitn
Big data technologies project @ Unitn 

Design and implement a big data system for short- and mid-term predictions (daily, up to 14 days) of COVID-relevant metrics (new cases, hospitalization, ICUs, deaths etc.) in the various regions of Italy.

# Run the project
We are using Docker Compose to deploy the services.

```
docker compose up  
```

# data sources
[stats by region](https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni)

[regions and age](https://github.com/pcm-dpc/COVID-19/blob/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv)

# Repository structure 
We decided to adopt a modular approach in order to have a cleaner and more manageble project, the backend could be logically divided in two buckets: 
- **ingestion**: from the raw data source to a database where to store the covid-relevant data 
- **computation**: get the data from the database and compute the models for the prediction 

All the services of the project can be run as docker containers. Therefore, the frontend and backend each contain a dockerfile. Some services are used as provided in the dockerhub such as the confluent implementation of Kafka & Zookeeper. They are configured in the docker compose file in the root directory. Using Docker makes the deployment more reliable on different machines.

# Data ingestion
Technologies used: Kafka, Postgresql 

This package is used to fetch the raw data from the github repository of the Protezione Civile, clean it and then save it on a postgresql database.

The two main actors of this package are the producer and the consumer, while the other files are modules containing the constants and the functions used.

## Producer
It uses pandas to create and modify a dataframe from a url, we decided to use this library because it allows us to easily handle csv data. The producer also shaped the 3 tables that then will be saved from the consumer in the database, in fact the csv files are full of redundant data so we decided to create new tables with the essential data.

Then kafka is used to send the tables to the consumer and to start the computation, within the same topic we used different key-value pairs to separate the data:

- `key:info ` : used to send the header of the table (column names and data types)
- `key:<table name>`: used to send table rows 
- `key:finish` : used to notify the end of a table 
- `key:compute` : used to fire the computation (more in the computation section)

The process of fetching and sending the data is made first for all the past data and then everyday the new data is fetched and the tables will be updated 

## Consumer
The Consumer is always listening for a message from the producer. When the info of a table arrives, it creates a new table and fills it as the rows arrive. It is unaware of how the data is gathered, its only job is to save the data that arrives in the database.

# Computation
Technologies used: spark, mongodb 

The computation part takes the data from the postgresql database, using spark to compute the models and then save the models on a mongodb.

## Prediction
Currently a linear regression is run on data from the past week. More complex models could be used to have a better accuracy such as [this](https://www.sciencedirect.com/science/article/pii/S2213398421001615) and 
[this](https://github.com/AlessandroMinervini/COVID-19-forecasting)






