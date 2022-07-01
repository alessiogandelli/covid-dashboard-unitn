# covid-dashboard-unitn
Big data technologies project @ Unitn 


## todo
- dockerfile for backend 
- change db to postgres or similar 
- use env var for connecting db
- add id to stats table

- add env file
- complete requirements 
- schedule daily refresh now it's minute refresh
- prettify logging 
- understand kafka config
- mongo in docker 
- spark on docker 
- frontend 
- report 

## Backend

# Build
```
docker compose up -d   
```

# Run
```
./src/scripts/docker_run.sh
```


# spark 
install jdk 
```
pip3 install pyspark 
```

this is for reading sqlite using spark
```
curl -O https://repo1.maven.org/maven2/org/xerial/sqlite-jdbc/3.34.0/sqlite-jdbc-3.34.0.jar

https://jdbc.postgresql.org/download/postgresql-42.4.0.jar
```


# prediction 
probably since we are interested in short term prediction we should fit only on recent data 
https://www.sciencedirect.com/science/article/pii/S2213398421001615
https://github.com/AlessandroMinervini/COVID-19-forecasting

# kafka 
handled by docker 

## confluent-kafka
 docker -> https://developer.confluent.io/get-started/python/#kafka-setup