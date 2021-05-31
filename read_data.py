from pyspark.sql import SparkSession
import findspark


findspark.init()


sparkConnector = SparkSession.builder.appName("Connector_to_MySQL_BDT")\
        .config("spark.driver.extraClassPath",
                "JDBC_connector/mysql-connector-java-8.0.25.jar")\
        .master('local[*]') \
        .enableHiveSupport()\
        .getOrCreate()


connect_mysql = sparkConnector.read\
    .format("jdbc") \
    .option("url", "jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306") \
    .option("dbtable", "bdt_db_mysql.dati_reali") \
    .option("user", "root_bdt") \
    .option("password", "bdt_mysql") \
    .option("driver", 'com.mysql.cj.jdbc.Driver') \
    .load()

