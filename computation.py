from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import FloatType, StringType
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

def def_accuracy_range(index_1, index_2):
    if (index_1 == None or index_2 == None):
        return None
    if (index_2 == (index_1 + 1) or index_2 == (index_1 - 1)):
        return 'medium'
    elif index_1 == index_2:
        return 'high'
    else:
        return 'inaccurate'

def_accuracy_range_udf = udf(def_accuracy_range, StringType())

def correspondance_dati_prev(df, c1, c2, c_name):
    return df.withColumn(c_name, def_accuracy_range_udf(c1, c2))

'''def correspondence_y_n(df, c1, c2, c_name):
    return df.withColumn(c_name, F.when(((col(c1) == col(c2)) & (col(c1).isNotNull()) & (col(c2).isNotNull())), 'Y').\
                         when(((col(c1) != col(c2)) & (col(c1).isNull()) & (col(c2).isNull())), 'Y').otherwise('N'))'''

df_12 = correspondance_dati_prev(df_12, df_12.prec_dati, df_12.id_prec_int, 'compare_piogge')
df_12 = correspondance_dati_prev(df_12, df_12.intensita_vento_dati, df_12.id_vento_val, 'compare_vento_vel')
df_12 = correspondance_dati_prev(df_12,  df_12.direzione_vento_dati, df_12.id_vento_dir_val,'compare_vento_dir')

df_345 = correspondance_dati_prev(df_345, df_345.prec_dati, df_345.id_prec_int, 'compare_pioggia')
df_345 = correspondance_dati_prev(df_345, df_345.intensita_vento_dati, df_345.id_vento_val, 'compare_vento_vel')
df_345 = correspondance_dati_prev(df_345, df_345.direzione_vento_dati, df_345.id_vento_dir_val, 'compare_vento_dir')

df_12.show()
df_345.show()

# todo filter none when doing compu / if prec < 0
# todo range temp precis

spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

df_previsioni = spark.read.csv('csv files/df_12.csv', header=True, sep=",")
df_previsioni.show()