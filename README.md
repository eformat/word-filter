# word-filter

This is a word filter that will listen on a kafka topic for single words that
are emitted, then it will filter them according to a supplied regular
expression and publish any words that match the filter onto a second kafka
topic.

## OpenShift quickstart

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
