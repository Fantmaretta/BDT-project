#from pyspark.python.pyspark.shell import sqlContext
#from pyspark.sql import SparkSession
#import findspark
#import os
#from pyspark import SparkConf, SparkContext
#import numpy
#import java.util.Properties import org.apache.spark.sql.{Row,SparkSession} import org.apache.spark.sql.SaveMode



'''#findspark.add_packages('mysql:mysql-connector-java:8.0.11')
SUBMIT_ARGS = "--packages mysql:mysql-connector-java:5.1.39 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
conf = SparkConf()
sc = SparkContext.getOrCreate(conf=conf)
'''
#spark = SparkSession.builder.config("spark.driver.extraClassPath", "/home/veror/Desktop/mysql-connector-java-8.0.25")


#findspark.init()

import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
#spark = SparkSession.builder.getOrCreate()

#os.environ['SPARK_CLASSPATH'] = "/usr/share/java/mysql-connector-java-5.1.34-bin.jar"

sparkConnector = SparkSession.builder.appName("Connector_to_MySQL_BDT")\
        .config("spark.driver.extraClassPath",
                "JDBC_connector/mysql-connector-java-8.0.25.jar")\
        .master('local[*]') \
        .enableHiveSupport()\
        .getOrCreate()


'''connect_mysql = sqlContext.read.format("jdbc") \
    .format("jdbc") \
    .option(
        url = f"jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306/") \
    .option("dbtable", "bdt_db_mysql.dati_reali") \
    .option("user", "root_bdt") \
    .option("password", "bdt_mysql") \
    .option("driver", 'com.mysql.jdbc.Driver') \
    .load()'''

#jdbc:mysql://to-rds-1174404209-cA37siB6.datasource.com:3306



connect_mysql = sparkConnector.read\
    .format("jdbc") \
    .option("url", "jdbc:mysql:bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306") \
    .option("dbtable", "bdt_db_mysql.dati_reali") \
    .option("user", "root_bdt") \
    .option("password", "bdt_mysql") \
    .option("driver", 'com.mysql.jdbc.Driver') \
    .load()




