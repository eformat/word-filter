import argparse
import os
import re

import kafka
import pyspark
from pyspark import streaming
from pyspark.streaming import kafka as kstreaming


def main():
    parser = argparse.ArgumentParser(
        description='filter some words on a kafka topic')
    parser.add_argument('--in', default='word-fountain', dest='intopic',
        help='the kafka topic to read words from')
    parser.add_argument('--out', default='word-filter',
        help='the kafka topic to publish filtered words on')
    parser.add_argument('--regex', default='.*',
        help='the regular expression to use as a filter')
    parser.add_argument('--servers', default='localhost:9092',
        help='the kafka brokers')
    args = parser.parse_args()
    intopic = args.intopic
    outtopic = args.out
    regexp = args.regex
    servers = args.servers

    print('using the following parameters:')
    print('input topic: {}'.format(intopic))
    print('output topic: {}'.format(outtopic))
    print('regexp: "{}"'.format(regexp))
    print('servers: {}'.format(servers))

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
