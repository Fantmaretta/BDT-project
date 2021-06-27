from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType, StringType
import pyspark.sql.functions as F
from pyspark.sql.functions import col


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

def def_accuracy_range(index_1, index_2):
    if (index_1 == None or index_2 == None or index_1 == -1 or index_2 == -1):
        return None
    if (index_2 == (index_1 + 1) or index_2 == (index_1 - 1)):
        return 'medium'
    elif index_1 == index_2:
        return 'high'
    else:
        return 'inaccurate'

def def_accuracy_range_temp(index_1, index_2):
    if (index_1 == None or index_2 == None or index_1 == -1 or index_2 == -1):
        return None
    if (index_2 <= (index_1 + 1) and index_2 >= (index_1 - 1)):
        return 'high'
    elif (index_2 <= (index_1 + 3) and index_2 >= (index_1 - 3)):
        return 'medium'
    else:
        return 'inaccurate'


def correspondance_dati_prev(df, c1, c2, c_name):
    def_accuracy_range_udf = udf(def_accuracy_range, StringType())
    return df.withColumn(c_name, def_accuracy_range_udf(c1, c2))

def correspondance_dati_prev_temp(df, c1, c2, c_name):
    def_accuracy_range_temp_udf = udf(def_accuracy_range_temp, StringType())
    return df.withColumn(c_name, def_accuracy_range_temp_udf(c1, c2))

'''def correspondence_y_n(df, c1, c2, c_name):
    return df.withColumn(c_name, F.when(((col(c1) == col(c2)) & (col(c1).isNotNull()) & (col(c2).isNotNull())), 'Y').\
                         when(((col(c1) != col(c2)) & (col(c1).isNull()) & (col(c2).isNull())), 'Y').otherwise('N'))'''

def acc_prev(df, column, df_name, exclude_null):

    if exclude_null:
        df = df.na.drop(subset=[column])

    total = df.count()
    res = (df.groupBy(column).count()
                      .withColumn('total', F.lit(total))
                      .withColumn('fraction', F.expr('count/total')))
    res.show()
    x = 'results/' + df_name + column + '.csv'
    print(x)
    res.toPandas().to_csv('results/' + df_name + column + '.csv')
    return res

def acc_prev_giorno(df, column, id_giorno_prev_col, id_giorno_prev, exclude_null):

    if exclude_null:
        df = df.na.drop(subset=[column])

    df = df.where(col(id_giorno_prev_col) == id_giorno_prev)
    print("----")
    df.show()

    total = df.count()
    res = (df.groupBy(column).count()
                      .withColumn('total', F.lit(total))
                      .withColumn('fraction', F.expr('count/total')))
    res.show()
    x = 'results/' + str(id_giorno_prev) + column + '.csv'
    print(x)
    res.toPandas().to_csv('results/' + str(id_giorno_prev) + column + '.csv')
    return res

if __name__ == "__main__":

    df_12 = from_csv('csv files/df_12.csv')
    df_345 = from_csv('csv files/df_345.csv')

    def_accuracy_range_udf = udf(def_accuracy_range, StringType())

    df_12 = correspondance_dati_prev(df_12, df_12.prec_dati, df_12.id_prec_int, 'compare_pioggia')
    df_12 = correspondance_dati_prev(df_12, df_12.intensita_vento_dati, df_12.id_vento_val, 'compare_vento_vel')
    df_12 = correspondance_dati_prev(df_12,  df_12.direzione_vento_dati, df_12.id_vento_dir_val, 'compare_vento_dir')
    df_12 = correspondance_dati_prev_temp(df_12, df_12['max(temperatura)'], df_12['temp_max'], 'compare_temp_max')
    df_12 = correspondance_dati_prev_temp(df_12, df_12['min(temperatura)'], df_12['temp_min'], 'compare_temp_min')


    df_345 = correspondance_dati_prev(df_345, df_345.prec_dati, df_345.id_prec_int, 'compare_pioggia')
    df_345 = correspondance_dati_prev(df_345, df_345.intensita_vento_dati, df_345.id_vento_val, 'compare_vento_vel')
    df_345 = correspondance_dati_prev(df_345, df_345.direzione_vento_dati, df_345.id_vento_dir_val, 'compare_vento_dir')
    df_345 = correspondance_dati_prev_temp(df_345, df_345['max(max(temperatura))'], df_345['temp_max'], 'compare_temp_max')
    df_345 = correspondance_dati_prev_temp(df_345, df_345['min(min(temperatura))'], df_345['temp_min'], 'compare_temp_min')


    df_12.show()
    df_345.show()

    '''acc_prev(df_12, 'compare_pioggia', '_12_', True)
    acc_prev(df_12, 'compare_vento_vel', '_12_', True)
    acc_prev(df_12, 'compare_vento_dir', '_12_', True)
    acc_prev(df_12, 'compare_temp_max', '_12_', True)
    acc_prev(df_12, 'compare_temp_min', '_12_', True)

    acc_prev(df_12, 'compare_pioggia', '_12_null', False)
    acc_prev(df_12, 'compare_vento_vel', '_12_null', False)
    acc_prev(df_12, 'compare_vento_dir', '_12_null', False)
    acc_prev(df_12, 'compare_temp_max', '_12_null', False)
    acc_prev(df_12, 'compare_temp_min', '_12_null', False)

    acc_prev(df_345, 'compare_pioggia', '_345_', True)
    acc_prev(df_345, 'compare_vento_vel', '_345_', True)
    acc_prev(df_345, 'compare_vento_dir', '_345_', True)
    acc_prev(df_345, 'compare_temp_max', '_345_', True)
    acc_prev(df_345, 'compare_temp_min', '_345_', True)

    acc_prev(df_345, 'compare_pioggia', '_345_null', False)
    acc_prev(df_345, 'compare_vento_vel', '_345_null', False)
    acc_prev(df_345, 'compare_vento_dir', '_345_null', False)
    acc_prev(df_345, 'compare_temp_max', '_345_null', False)
    acc_prev(df_345, 'compare_temp_min', '_345_null', False)'''



    acc_prev_giorno(df_12, 'compare_pioggia', 'id_previsione_giorno', 1.0, True)
