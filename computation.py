from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import FloatType
import numpy as np
import pyspark.sql.functions as F

def from_csv(csv_path):

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()


    df = spark.read.csv(csv_path, header=True, sep=",")

    #df = df.select(df.columns[3:]).cast('float')

    for col in df.columns[4:]:
        df = df.withColumn(col, df[col].cast(FloatType()))

    return df

df_12 = from_csv('csv files/df_12.csv')
df_345 = from_csv('csv files/df_345.csv')

def correspondence_y_n(df, c1, c2, c_name):
    return df.withColumn(c_name, F.when((F.col(c1) == F.col(c2)), 'Y').otherwise('N'))

df_12 = correspondence_y_n(df_12, 'id_prec_int', 'prec_dati', 'compare_pioggia')
df_12 = correspondence_y_n(df_12, 'id_vento_val', 'intensita_vento_dati', 'compare_vento_vel')
df_12 = correspondence_y_n(df_12, 'id_vento_dir_val', 'direzione_vento_dati', 'compare_vento_dir')

df_345 = correspondence_y_n(df_345, 'id_prec_int', 'prec_dati', 'compare_pioggia')
df_345 = correspondence_y_n(df_345, 'id_vento_val', 'intensita_vento_dati', 'compare_vento_vel')
df_345 = correspondence_y_n(df_345, 'id_vento_dir_val', 'direzione_vento_dati', 'compare_vento_dir')

df_12.show()
df_345.show()

# todo filter none when doing compu