from pyspark.sql import SparkSession

# read csv file into dataframe pyspark

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# previsioni
df_previsioni = spark.read.csv("csv files/df_previsioni.csv",header=True,sep=",")
#df_previsioni.show()

#dati_reali
df_dati_reali = spark.read.csv("csv files/csv_dati_reali_ok.csv",header=True,sep=",")
df_dati_reali.show()

d = df_dati_reali.groupBy('localita', 'data').count().orderBy('localita')#.avg('temperatura').collect()
d.show()




