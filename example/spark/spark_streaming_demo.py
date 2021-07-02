# 第一种创建方式
# from pyspark import SparkContext
# 第二种创建方式
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

# 第一种创建方式
# sc = SparkContext("local[2]", "SparkStreamingWordCountPython")
# 第二种创建方式
spark = SparkSession.builder.master("local[2]").appName("SparkStreamingWordCountPython").config("spark.logConf", "true").getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("INFO")
ssc = StreamingContext(sc, 1)
lines = ssc.socketTextStream("127.0.0.1", 9999)
words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts.pprint()
ssc.start()
ssc.awaitTermination()
