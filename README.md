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
<br>
<img src="Terminal 1.1.png"/>

### Terminal 2

<div align="justify">
Pada Terminal 2, perintah spark-submit --master local[*] network_wordcount.py localhost 9999 digunakan untuk menjalankan aplikasi Spark Streaming yang disebut network_wordcount.py. Aplikasi ini akan terhubung ke sumber data di localhost dengan menggunakan port 9999.
</div>
<br>
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

### Output 

<img src="Output 1.png"/>
</div>

## Metode 2: Mode Stateful Stream Processing
<div align="justify">
Sekarang coba untuk file stateful_network_wordcount.py yang isi kodenya seperti berikut ini.
</div>

### Terminal 1

<div align="justify">
Pada Terminal 1, perintah nc -lk 9999 digunakan untuk membuka netcat dalam mode listening pada port 9999. Netcat adalah utilitas jaringan yang digunakan untuk membaca dan menulis data melalui koneksi jaringan.
</div>
<br>
<img src="Terminal 2.1.png"/>

### Terminal 2

<div align="justify">
Pada Terminal 2, perintah spark-submit --master local[*] stateful_network_wordcount.py localhost 9999 digunakan untuk menjalankan aplikasi Spark Streaming yang disebut stateful_network_wordcount.py. Aplikasi ini akan terhubung ke sumber data di localhost dengan menggunakan port 9999.
</div>
<br>
<img src="Terminal 2.2.png"/>
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
        print("Usage: stateful_network_wordcount.py <hostname> <port>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="PythonStreamingStatefulNetworkWordCount")
    ssc = StreamingContext(sc, 5)
    ssc.checkpoint("checkpoint")

    # RDD with initial state (key, value) pairs
    initialStateRDD = sc.parallelize([(u'hello', 1), (u'world', 1)])

    def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)

    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    running_counts = lines.flatMap(lambda line: line.split(" "))\
                          .map(lambda word: (word, 1))\
                          .updateStateByKey(updateFunc, initialRDD=initialStateRDD)

    running_counts.pprint()

    ssc.start()
    ssc.awaitTermination()
</code>
</pre>
<p align="justify">
 PySpark dan Spark Streaming untuk melakukan pengolahan data streaming dengan keadaan (stateful stream processing). Program ini membaca data streaming dari soket, mempertahankan hitungan kata yang berjalan, dan mencetak jumlah terbaru untuk setiap kata secara real-time. Dalam implementasinya, konteks Spark dan konteks Streaming dibuat, interval batch ditetapkan, dan direktori checkpoint digunakan untuk menyimpan data status sementara. Program juga mendefinisikan fungsi updateFunc yang menggabungkan data baru dengan data sebelumnya untuk memperbarui status. Data streaming diproses melalui operasi-transformasi seperti flatMap dan map, dan updateStateByKey digunakan untuk melakukan pengolahan stream dengan keadaan. Hasilnya dicetak menggunakan pprint(), dan konteks streaming dimulai dengan start() dan awaitTermination() digunakan untuk menunggu penghentian konteks streaming. Secara keseluruhan, program ini merupakan contoh yang menggambarkan cara kerja pengolahan stream dengan keadaan menggunakan Spark Streaming.
</p>

### Output 

<img src="Output 2.png"/>
</div>

