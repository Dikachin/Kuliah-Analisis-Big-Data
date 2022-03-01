import math
from pyspark import SparkContext
from pyspark.sql import SparkSession
import pandas as pd

#input data
df= pd.read_csv("general_medicine_mtsamples.csv",header=0)
df = df['medical report']

#preprocessing
df = df.str.replace('[^a-zA-Z0-9- ]', '')
df = df.str.replace('-',' ')
df = df.str.lower()
key = 1
data = []
for value in df :
  data.append((key,value))
  key += 1

sc =SparkContext()

#proses menghitung tf
lines=sc.parallelize(data)
map1=lines.flatMap(lambda x: [((x[0],i),1) for i in x[1].split()])
map1.collect()
reduce=map1.reduceByKey(lambda x,y:x+y)
reduce.collect()
tf=reduce.map(lambda x: (x[0][1],(x[0][0],x[1])))
tf.collect()

#menghitung idf
map2=reduce.map(lambda x: (x[0][1],(x[0][0],x[1],1)))
map2.collect()
map3=map2.map(lambda x:(x[0],x[1][2]))
map3.collect()
reduce2=map3.reduceByKey(lambda x,y:x+y)
reduce2.collect()
idf=reduce2.map(lambda x: (x[0],math.log10(len(data)/x[1])))
idf.collect()

#join tf dan idf
rdd=tf.join(idf)
rdd.collect()
rdd=rdd.map(lambda x: (x[1][0][0],(x[0],x[1][0][1],x[1][1],x[1][0][1]*x[1][1]))).sortByKey()
rdd.collect()

#output
spark = SparkSession(sc)
rdd=rdd.map(lambda x: (x[0],x[1][0],x[1][1],x[1][2],x[1][3]))
print(rdd.toDF(["DocumentId","Token","TF","IDF","TF-IDF"]).show())