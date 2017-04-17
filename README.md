# word-filter

This is a word filter that will listen on a kafka topic for single words that
are emitted, then it will filter them according to a supplied regular
expression and publish any words that match the filter onto a second kafka
topic.

## Quick start

1. Install app requirements
   ```bash
   pip install -r requirement.txt
   ```

1. Get a copy of Apache Spark (requires 2.1.0+)
   ```bash
   mkdir spark
   curl https://www.apache.org/dist/spark/spark-2.1.0/spark-2.1.0-bin-hadoop2.7.tgz | tar zx -C spark --strip-components=1
   ```
1. [Setup Apache Kafka](https://kafka.apache.org/documentation.html#quickstart)

1. Run the app
   ```bash
   spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 app.py --regex="[A-Z]"
   ```

1. Publish some words to topic `word-fountain`

1. Watch the output on topic `word-filter`, with the regular expression listed
   you should only see words with at least one upper case letter in them

## OpenShift tutorial

The word-filter is most easily demonstrated in OpenShift by utilizing the
[grafzahl](http://radanalytics.io/applications/grafzahl#installation)
application.

1. Install and start the [grafzahl](http://radanalytics.io/applications/grafzahl#installation)
   application, including Apache Kafka, and word-fountain

1. Start the word-filter, the regex specified will filter all words that
   contain at least one capital letter
   ```bash
   oc new-app --template=oshinko-pyspark-build-dc \
              -p APPLICATION_NAME=word-filter \
              -p GIT_URI=https://github.com/elmiko/word-filter \
              -p APP_ARGS='--servers=apache-kafka:9092 --regex="[A-Z]"'  \
              -p SPARK_OPTIONS='--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0'
   ```

1. Start a second grafzahl to view the filtered results
   ```bash
   oc new-app --template=oshinko-pyspark-build-dc \
              -p APPLICATION_NAME=grafzahl2 \
              -p GIT_URI=https://github.com/mattf/grafzahl \
              -p APP_ARGS='--servers=apache-kafka:9092 --topic=word-filter' \
              -p SPARK_OPTIONS='--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0'
   ```

1. Expose the second grafzahl
   ```bash
   oc expose svc/grafzahl2
   ```

Now navigate to the second grafzahl application with your web browser to view
the filtered output results..
