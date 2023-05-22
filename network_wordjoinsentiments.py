from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def print_happiest_words(rdd):
    top_list = rdd.take(5)
    print("Happiest topics in the last 5 seconds (%d total):" % rdd.count())
    for tuple in top_list:
        print("%s (%d happiness)" % (tuple[1], tuple[0]))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: network_wordjoinsentiments.py <hostname> <port>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingNetworkWordJoinSentiments")
    ssc = StreamingContext(sc, 5)

    # Read in the word-sentiment list and create a static RDD from it
    word_sentiments_file_path = "data/streaming/AFINN-111.txt"
    word_sentiments = ssc.sparkContext.textFile(word_sentiments_file_path) \
        .map(lambda line: tuple(line.split("\t")))

    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

word_counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a + b)

    # Determine the words with the highest sentiment values by joining the streaming RDD
    # with the static RDD inside the transform() method and then multiplying
    # the frequency of the words by its sentiment value
    happiest_words = word_counts.transform(lambda rdd: word_sentiments.join(rdd)) \
        .map(lambda (word, tuple): (word, float(tuple[0]) * tuple[1])) \
        .map(lambda (word, happiness): (happiness, word)) \
        .transform(lambda rdd: rdd.sortByKey(False))

    happiest_words.foreachRDD(print_happiest_words)

    ssc.start()
    ssc.awaitTermination()