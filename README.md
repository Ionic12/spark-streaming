# Spark Streaming
<div align="justify">
Tugas ini merupakan bagian dari mata kuliah Big Data dan berfokus pada topik Spark Streaming pada Apache Spark.
</div>

## Metode 1: Mode Stateless Stream Processing
<div align="justify">
Pada Terminal 1, perintah nc -lk 9999 digunakan untuk membuka netcat dalam mode listening pada port 9999. Netcat adalah utilitas jaringan yang digunakan untuk membaca dan menulis data melalui koneksi jaringan.
<img src="Terminal 1.1.png"/>
</div>
<div>
<pre>
<code>
from pyspark import *
from pyspark.sql import *
spark = SparkSession.builder.appName("metode1").getOrCreate()
sc = spark.sparkContext
mylist = [(50, "DataFrame"),(60, "pandas")]
myschema = ['col1', 'col2']
df1 = spark.createDataFrame(mylist, myschema)
df1.show()
</code>
</pre>
<p align="justify">
PySpark untuk membuat sebuah DataFrame pada Spark. Proses yang terjadi meliputi impor modul-modul PySpark, pembuatan objek SparkSession dengan nama aplikasi "metode1", pembuatan objek SparkContext untuk menghubungkan Spark dengan cluster, pembuatan list yang berisi tuple data, pembuatan list yang berisi nama kolom, pembuatan objek DataFrame dengan metode createDataFrame(), dan terakhir memanggil metode show() pada objek DataFrame untuk menampilkan isi dari DataFrame.
</p>
</div>
