import os
import re

import kafka
import pyspark
from pyspark import streaming
from pyspark.streaming import kafka as kstreaming


def main():
    intopic = os.getenv('IN_TOPIC', 'word-fountain')
    outtopic = os.getenv('OUT_TOPIC', 'word-filter')
    servers = os.getenv('SERVERS', 'localhost:9092')
    regexp = os.getenv('REGEX', '.*')

    sc = pyspark.SparkContext(appName='word-filter')
    ssc = streaming.StreamingContext(sc, 3)
    kds = kstreaming.KafkaUtils.createDirectStream(
            ssc, [intopic], {'bootstrap.servers': servers})
    words = kds.map(lambda x: x[1])
    filterwords = words.filter(lambda x: False if re.search(regexp, x) is None else True)

    def send_response(rdd):
        producer = kafka.KafkaProducer(bootstrap_servers=servers)
        for r in rdd.collect():
            producer.send(outtopic, str(r))
        producer.flush()

    filterwords.pprint()
    filterwords.foreachRDD(send_response)
    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
    main()
