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
    
### stateful_network_wordcount.py
    
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

## Melakukan Transformasi di Spark Streaming
<div align="justify">
Untuk melanjutkan praktik sebelumnya dengan transformasi data menggunakan sentimen kata sederhana, kita dapat memodifikasi kode sebelumnya atau menggunakan metode baru.
</div>

### Mempersiapkan Folder Untuk File AFINN-111.txt dan Copy File  AFINN-111.txt

<div align="justify">
Untuk membuat folder baru untuk file AFINN-111.txt, Anda dapat membuka terminal atau command prompt, pindah ke direktori yang diinginkan menggunakan perintah cd, dan menggunakan perintah mkdir diikuti dengan nama folder yang ingin Anda buat. Misalnya, Anda dapat menggunakan perintah mkdir data untuk membuat folder "data". Selanjutnya, Anda dapat menggunakan perintah mkdir data/streaming untuk membuat folder "streaming" di dalam folder "data". Setelah folder baru dibuat, Anda dapat menyalin file AFINN-111.txt ke folder tersebut menggunakan perintah cp AFINN-111.txt /opt/spark/examples/src/main/python/streaming/data/streaming. 
</div>
<br>
<img src="Text 3.1.png"/>
<img src="Text 3.2.png"/>

### Output

<div align="justify">
Perintah spark-submit --master local[*] network_wordjoinsentiments.py localhost 9999 digunakan untuk menjalankan aplikasi Spark Streaming yang disebut network_wordjoinsentiments.py. Aplikasi ini akan terhubung ke sumber data di localhost dengan menggunakan port 9999.
</div>
<br>
<img src="Output 3.png"/>
<div>
    
### network_wordjoinsentiments.py
    
<pre>
<code>
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
</code>
</pre>
<p align="justify">
PySpark untuk menghitung kata-kata paling bahagia (happiest words) dalam data streaming. Program ini menggunakan konteks Spark Streaming untuk membaca data streaming dari soket, menghitung jumlah kata, dan melakukan join dengan RDD statis yang berisi nilai sentimen kata. Setelah itu, program menghitung skor sentimen kata dengan mengalikan frekuensi kata dengan nilai sentimennya. Hasilnya adalah 5 kata paling bahagia yang dicetak setiap 5 detik. Program ini membantu dalam menganalisis sentimen kata dalam data streaming secara real-time.
</p>
</div>

## Pengertian Kode
<table>
  <tr>
    <th align="center">No</th>
    <th>Kode</th>
    <th>Penjelasan</th>
  </tr>
  <tr>
    <td align="center">1</td>
    <td align="center">sys.argv, sys.stderr, StreamingContext, sc, socketTextStream, reduceByKey, lambda line, awaitTermination</td>
    <td align="justify">Dalam konteks Spark Streaming, beberapa elemen penting yang sering digunakan adalah sys.argv untuk mengambil argumen baris perintah, sys.stderr untuk mencetak pesan kesalahan, StreamingContext untuk mengatur aliran streaming, sc untuk menginisialisasi konteks Spark, socketTextStream untuk membuat aliran streaming dari soket, reduceByKey untuk menggabungkan nilai-nilai berdasarkan kunci dalam data streaming, lambda line sebagai fungsi anonim untuk memproses setiap baris data streaming, dan awaitTermination untuk menunggu hingga konteks streaming dihentikan. Semua elemen ini berguna dalam membangun dan menjalankan aplikasi streaming menggunakan Spark Streaming dalam konteks Spark.</td>
  </tr>
  <tr>
    <td align="center">2</td>
    <td align="center">nc, lk</td>
    <td align="justify">
nc, singkatan dari "netcat", adalah utilitas baris perintah yang digunakan untuk mengirim dan menerima data melalui koneksi jaringan. Dalam konteks yang disebutkan, nc digunakan untuk membuat soket dan mengaktifkan mode "listening" atau "server" dengan opsi -l. Ini memungkinkan netcat untuk menerima koneksi dari klien atau program lain yang ingin mengirimkan data melalui koneksi jaringan. Opsi -k digunakan agar netcat tetap berjalan setelah koneksi ditutup, sehingga tetap dapat mendengarkan pada port tertentu (9999 dalam kasus ini) dan menerima koneksi berikutnya setelah koneksi sebelumnya ditutup. Dalam kode yang diberikan, netcat digunakan untuk mengirimkan data streaming ke soket yang akan dibaca oleh program PySpark.</td>
  </tr>
  <tr>
    <td align="center">3</td>
    <td align="center">spark-submit, master, local[*]</td>
    <td align="justify">
Dalam konteks Spark Streaming, spark-submit adalah perintah untuk mengirim dan menjalankan aplikasi PySpark Streaming. Parameter master pada perintah tersebut digunakan untuk menentukan master atau manajer cluster yang akan digunakan, seperti local untuk menjalankan aplikasi Streaming pada satu mesin lokal. Nilai local[*] pada master menunjukkan penggunaan semua core yang tersedia pada mesin lokal, sehingga memungkinkan pemrosesan paralel. Dengan menggunakan spark-submit dan pengaturan master sebagai local[*], aplikasi Streaming dapat dijalankan secara lokal dengan pemanfaatan semua core yang tersedia untuk pemrosesan paralel.</td>
  </tr>
  <tr>
    <td align="center">4</td>
    <td align="center">ssc.checkpoint, parallelize, updateStateByKey, flatMap</td>
    <td align="justify">
Dalam konteks Spark Streaming, ssc.checkpoint digunakan untuk mengatur checkpoint directory yang menyimpan status streaming untuk pemulihan setelah kegagalan. parallelize digunakan untuk membuat RDD dari koleksi data di dalam program dan dapat digunakan dalam operasi-transformasi pada DStream. updateStateByKey adalah operasi untuk menghitung stateful stream dengan mempertahankan dan memperbarui state berdasarkan kunci dan batch data baru. flatMap digunakan untuk memetakan setiap elemen dalam DStream menjadi nol atau lebih elemen dalam DStream baru. Kesemuanya ini berguna dalam pengaturan checkpoint, pembuatan RDD, perhitungan stateful, dan transformasi elemen dalam Spark Streaming.</td>
  </tr>
  <tr>
    <td align="center">5</td>
    <td align="center">rdd.take(5), transform, rdd.sortByKey(False)</td>
    <td align="justify">
Dalam konteks Spark Streaming, rdd.take(5) adalah metode yang digunakan untuk mengambil 5 elemen teratas dari RDD batch saat ini dalam bentuk list. transform adalah metode pada DStream yang digunakan untuk menerapkan transformasi pada data streaming, menghasilkan DStream baru dengan perubahan yang diterapkan pada setiap elemen dalam setiap batch data streaming. rdd.sortByKey(False) adalah metode yang digunakan untuk mengurutkan elemen RDD batch saat ini berdasarkan kunci dengan urutan menurun. Dalam Spark Streaming, elemen-elemen ini digunakan untuk mengambil sejumlah elemen teratas dari RDD, menerapkan transformasi pada DStream, dan mengurutkan elemen RDD berdasarkan kunci dalam batch data streaming.</td>
  </tr>
</table>
