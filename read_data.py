from pyspark.sql import SparkSession
import findspark
import pandas as pd
import datetime as dt


# code to save database content into csv file to have it to read it as dataframe pyspark

if __name__ == "__main__":

    findspark.init()

    # initiate spark session
    sparkConnector = SparkSession.builder.appName("Connector_to_MySQL_BDT")\
            .config("spark.driver.extraClassPath",
                    "JDBC_connector/mysql-connector-java-8.0.25.jar")\
            .master('local[*]') \
            .enableHiveSupport()\
            .getOrCreate()


    # retrieve previsioni

    query_previsioni = """SELECT * FROM bdt_db_mysql.previsioni """

    df_previsioni = sparkConnector.read\
        .format("jdbc") \
        .option("url", "jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306") \
        .option("user", "root_bdt") \
        .option("password", "bdt_mysql") \
        .option("driver", 'com.mysql.cj.jdbc.Driver') \
        .option("query", query_previsioni)\
        .load()
    # .option("dbtable", "bdt_db_mysql.dati_reali")
    df_previsioni.show()

    # save into csv
    df_previsioni.toPandas().to_csv('csv files/df_previsioni.csv')


    # retrieve dati_reali

    query_dati_reali = """SELECT * FROM bdt_db_mysql.dati_reali"""

    df_dati_reali = sparkConnector.read\
        .format("jdbc") \
        .option("url", "jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306") \
        .option("user", "root_bdt") \
        .option("password", "bdt_mysql") \
        .option("driver", 'com.mysql.cj.jdbc.Driver') \
        .option("query", query_dati_reali)\
        .load()
    df_dati_reali.show()

    # keep only observations with 0-5 type of days
    df_dati_reali = df_dati_reali.filter(df_dati_reali.data >= "2021-05-07")

    # save into csv
    df_dati_reali.toPandas().to_csv('csv files/df_dati_reali.csv')


    # add column containing corresponding time range
    df_dati_reali_ok = pd.read_csv('csv files/df_dati_reali.csv')
    df_dati_reali_ok['time'] = pd.to_datetime(df_dati_reali_ok['time'])
    df_dati_reali_ok['time'] = [time.time() for time in df_dati_reali_ok['time']]


    # create column containing corresponding fascia oraria
    df_dati_reali_ok['fascia'] = 0

    for index, row in df_dati_reali_ok.iterrows():
        if row['time'] >= dt.time(0,0,0) and row['time'] < dt.time(6,0,0):
            df_dati_reali_ok['fascia'][index] = '00-06'
        elif row['time']  >= dt.time(6,0,0) and row['time'] < dt.time(12,0,0):
            df_dati_reali_ok['fascia'][index] = '06-12'
        elif row['time']  >= dt.time(12,0,0) and row['time']  < dt.time(18,0,0):
            df_dati_reali_ok['fascia'][index] = '12-18'
        else:
            df_dati_reali_ok['fascia'][index] = '18-24'

    df_dati_reali_ok.to_csv('csv files/df_dati_reali_ok.csv')
