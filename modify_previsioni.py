from pyspark.sql import SparkSession

# todo from 2021-05-08 to 2021-20-06 ?
# todo 11 e 14 giugno hanno meno cose!! perché con ala almeno
# come gestire queste cose
# todo issue to put in the report

# read csv file into dataframe pyspark

def initialize_df_p(df_path):

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    df_previsioni = spark.read.csv(df_path, header=True, sep=",")
    df_previsioni = df_previsioni.orderBy('localita', 'data', 'id_previsione_giorno')

    #find_prec_udf = udf(find_prec, StringType())
    #df_previsioni = df_previsioni.withColumn('precipitazioni', find_prec_udf(df_previsioni.id_prec_int))

    #find_vento_udf = udf(find_vento, StringType())
    #df_previsioni = df_previsioni.withColumn('intensita_vento', find_vento_udf(df_previsioni.id_vento_val))

    df_previsioni.show()

    return df_previsioni


'''def find_prec(x):
    if x == '-1':
        return None
    elif x == '1':
        return '0-5'
    elif x == '2':
        return '5-15'
    elif x == '3':
        return '15-40'
    else:
        return '> 40'

def find_vento(x):
    if x == '1':
        return '0-0.5'
    elif x == '2':
        return '0.5-4'
    elif x == '3':
        return '4-8'
    elif x == '4':
        return '8-14'
    else:
        return '> 14'
'''

def df_12_p(df_previsioni):

    # create df with only 1 2 giorni
    df_previsioni_12 = df_previsioni.filter(df_previsioni['id_previsione_giorno'] != 3)\
        .filter(df_previsioni['id_previsione_giorno'] != 4)\
        .filter(df_previsioni['id_previsione_giorno'] != 5)\
        .filter(df_previsioni['id_previsione_giorno'] != 0)\
        .drop('_c0')\
        .distinct()\
        .filter(df_previsioni['data'] > '2021-05-07')
    df_previsioni_12.show()

    return df_previsioni_12

def df_345_p(df_previsioni):

    # create df with only 3 4 5 giorni
    df_previsioni_345 = df_previsioni.filter(df_previsioni['id_previsione_giorno'] != 0)\
        .filter(df_previsioni['id_previsione_giorno'] != 1)\
        .filter(df_previsioni['id_previsione_giorno'] != 2)\
        .filter(df_previsioni['data'] > '2021-05-07')\
        .drop('_c0')\
        .distinct()\
        .orderBy('localita', 'data', 'id_previsione_giorno', 'fascia')
    df_previsioni_345.show()

    return df_previsioni_345

