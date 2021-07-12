from pyspark.sql import SparkSession


# read csv file into dataframe pyspark

def initialize_df_p(df_path):
    '''
    Given the df of prediction data it modifies it to make it suitable for following analysis
    :param df_path:
    :return:
    '''

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    df_previsioni = spark.read.csv(df_path, header=True, sep=",")
    df_previsioni = df_previsioni.orderBy('localita', 'data', 'id_previsione_giorno')

    df_previsioni.show()

    return df_previsioni

def df_12_p(df_previsioni):
    '''
    Given the df of prediction data, it extracts only the observations of day 1 2
    :param df_previsioni:
    :return:
    '''

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
    '''
    Given the df of prediction data, it extracts only the observations of day 3 4 5
    :param df_previsioni:
    :return:
    '''

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

