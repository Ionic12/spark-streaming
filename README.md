# Spark Streaming
<div align="justify">
Tugas ini merupakan bagian dari mata kuliah Big Data dan berfokus pada topik Spark Streaming pada Apache Spark.
</div>

## Metode 1: Mode Stateless Stream Processing
<div align="justify">
Buka 2 terminal atau CMD untuk melakukan simulasi stateless stream processing dengan spark streaming.
</div>

### Terminal 1

<div align="justify">
Pada Terminal 1, perintah nc -lk 9999 digunakan untuk membuka netcat dalam mode listening pada port 9999. Netcat adalah utilitas jaringan yang digunakan untuk membaca dan menulis data melalui koneksi jaringan.
</div>
<img src="Terminal 1.1.png"/>

### Terminal 2

<div align="justify">
Pada Terminal 2, perintah spark-submit --master local[*] network_wordcount.py localhost 9999 digunakan untuk menjalankan aplikasi Spark Streaming yang disebut network_wordcount.py. Aplikasi ini akan terhubung ke sumber data di localhost dengan menggunakan port 9999.
</div>
<img src="Terminal 1.2.png"/>
<div>
    
### network_wordcount.py
    
<pre>
<code>
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: network_wordcount.py <hostname> <port>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="PythonStreamingNetworkWordCount")
    ssc = StreamingContext(sc, 1)

    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    counts = lines.flatMap(lambda line: line.split(" "))\
                  .map(lambda word: (word, 1))\
                  .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
</code>
</pre>
<p align="justify">
Kode di atas adalah contoh program PySpark untuk melakukan streaming penghitungan kata dari sebuah socket. Program ini menggunakan StreamingContext untuk membuat konteks streaming Spark, membaca aliran data dari socket menggunakan socketTextStream, dan melakukan operasi-transformasi seperti flatMap, map, dan reduceByKey untuk menghitung jumlah kata yang sama. Hasil penghitungan kata dicetak menggunakan pprint(). Program ini memulai proses streaming dengan start() dan menunggu hingga proses streaming berakhir dengan awaitTermination(). Secara keseluruhan, program ini memanfaatkan PySpark untuk melakukan streaming dan pengolahan data secara real-time dari socket.
</p>
</div>
