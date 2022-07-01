# covid-dashboard-unitn
Big data technologies project @ Unitn 


## todo

- use env var for connecting db
- add id to stats table
- add env file
- prettify logging 
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