from pyspark.python.pyspark.shell import sqlContext
from pyspark.sql import SparkSession
import findspark
import os
from pyspark import SparkConf, SparkContext



#findspark.add_packages('mysql:mysql-connector-java:8.0.11')
SUBMIT_ARGS = "--packages mysql:mysql-connector-java:5.1.39 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
conf = SparkConf()
sc = SparkContext.getOrCreate(conf=conf)

spark = SparkSession.builder.config("spark.driver.extraClassPath", "/home/veror/Desktop/mysql-connector-java-8.0.25")

connect_mysql = sqlContext.read.format("jdbc") \
    .format("jdbc") \
    .option("url", "jdbc:mysql:bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com") \
    .option("dbtable", "bdt_db_mysql.dati_reali") \
    .option("user", "root_bdt") \
    .option("password", "bdt_mysql") \
    .option("driver", 'com.mysql.jdbc.Driver') \
    .load()

