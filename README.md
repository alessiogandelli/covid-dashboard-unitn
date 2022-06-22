# covid-dashboard-unitn
Big data technologies project @ Unitn 

## questions 
why sqlite? because it is serverless and lightweight


## todo
create a more complex schema in order to avoid repetition 

use self hosted broker

prettify logging 

understand kafka config

other sql dbsm?

# Buld
```
docker build --tag python-docker .
```

# Run
```
docker run -it python-docker  
```


# spark 
install jdk 
```
pip3 install pyspark 
```
```
curl -O https://repo1.maven.org/maven2/org/xerial/sqlite-jdbc/3.34.0/sqlite-jdbc-3.34.0.jar
```


let's consider saving the data in a sql spark friendly manner from the ingestion part

https://stackoverflow.com/questions/33999156/grouped-linear-regression-in-spark


# prediction 
probably since we are interested in short term prediction we should fit only on recent data 


# kafka 
install kafka with homebrew
```
brew install kafka 
```

start kafka server 
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

```
bin/kafka-server-start.sh config/server.properties
```
create topic covid
```
usr/local/bin/kafka-topics --create --topic covid --bootstrap-server localhost:9092
```
start  producer console

usr/local/bin/kafka-console-producer --topic covid --bootstrap-server localhost:9092

## confluent-kafka
 docker -> https://developer.confluent.io/get-started/python/#kafka-setup