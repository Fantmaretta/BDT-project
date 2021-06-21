from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# todo from 05-05 to 20-06 ?

# read csv file into dataframe pyspark


def initialize_df_d(df_path):
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    #dati_reali

    df_dati_reali = spark.read.csv(df_path, header=True, sep=",")
    df_dati_reali.show()

    # cast type of temperatura, pioggia, vento_velocita, vento_direzione column from string into float
    df_dati = df_dati_reali.withColumn('temperatura', df_dati_reali['temperatura'].cast('float'))
    df_dati = df_dati.withColumn('pioggia', df_dati_reali['pioggia'].cast('float'))
    df_dati = df_dati.withColumn('vento_velocita', df_dati_reali['vento_velocita'].cast('float'))
    df_dati = df_dati.withColumn('vento_direzione', df_dati_reali['vento_direzione'].cast('float'))

    return(df_dati)

    # drop rows with temperature = null -> not necessary since wgen doing avg it does it by itself
    #df_dati = df_dati.na.drop(subset=["temperatura"])

def compute_avg(df, l, d, f, var):
    return df.groupBy(l, d, f).avg(var).orderBy(d, l, f)

def compute_min(df, l, d, f, var):
    return df.groupBy(l, d, f).min(var).orderBy(d, l, f)

def compute_max(df, l, d, f, var):
    return df.groupBy(l, d, f).max(var).orderBy(d, l, f)


def df_12(df_dati):

    # df containing localita, data, fascia, avg temperatura
    d_avg_temp = compute_avg(df_dati, 'localita', 'data', 'fascia', 'temperatura')
    #d_avg_temp.show()

    # df containing localita, data, fascia, avg pioggia
    d_avg_pioggia = compute_avg(df_dati, 'localita', 'data', 'fascia', 'pioggia')
    #d_avg_pioggia.show()

    # df containing localita, data, fascia, avg vento_velocita
    d_avg_vento_velocita = compute_avg(df_dati, 'localita', 'data', 'fascia', 'vento_velocita')
    #d_avg_vento_velocita.show()

    # df containing localita, data, fascia, avg vento_direzione
    d_avg_vento_direzione = compute_avg(df_dati, 'localita', 'data', 'fascia', 'vento_direzione')
    #d_avg_vento_direzione.show()

    # df containing localita, data, fascia, temperatura min
    d_temp_min = compute_min(df_dati, 'localita', 'data', 'fascia', 'temperatura')
    #d_temp_min.show()

    # df containing localita, data, fascia, temperatura max
    d_temp_max = compute_max(df_dati, 'localita', 'data', 'fascia', 'temperatura')
    #d_temp_max.show()

    # joined df for fascia 1 2
    joined_df = d_avg_temp.join(d_avg_pioggia, ['localita', 'data', 'fascia'])\
        .join(d_avg_vento_velocita, ['localita', 'data', 'fascia'])\
        .join(d_avg_vento_direzione, ['localita', 'data', 'fascia'])\
        .join(d_temp_min, ['localita', 'data', 'fascia'])\
        .join(d_temp_max, ['localita', 'data', 'fascia'])\
        .orderBy('data', 'localita', 'fascia')
    joined_df.show()

    return joined_df


# define fascia to match with previsioni on day 3 4 5
def find_fascia(x):
    if x == '00-06' or x == '06-12':
        return '00-12'
    else:
        return '12-24'

def df_345(joined_df):

    find_fascia_udf = udf(find_fascia, StringType())
    joined_df_extension = joined_df.withColumn('fascia_extended', find_fascia_udf(joined_df.fascia))
    #joined_df_extension.show()

    # df containing localita, data, fascia, avg temperatura
    d_avg_temp = compute_avg(joined_df_extension, 'localita', 'data', 'fascia_extended', 'avg(temperatura)')
    #d_avg_temp.show()

    # df containing localita, data, fascia, avg pioggia
    d_avg_pioggia = compute_avg(joined_df_extension, 'localita', 'data', 'fascia_extended', 'avg(pioggia)')
    #d_avg_pioggia.show()

    # df containing localita, data, fascia, avg vento_velocita
    d_avg_vento_velocita = compute_avg(joined_df_extension, 'localita', 'data', 'fascia_extended', 'avg(vento_velocita)')
    #d_avg_vento_velocita.show()

    # df containing localita, data, fascia, avg vento_direzione
    d_avg_vento_direzione = compute_avg(joined_df_extension, 'localita', 'data', 'fascia_extended', 'avg(vento_direzione)')
    #d_avg_vento_direzione.show()

    # df containing localita, data, fascia, temperatura min
    d_temp_min = compute_min(joined_df_extension, 'localita', 'data', 'fascia_extended', 'min(temperatura)')
    #d_temp_min.show()

    # df containing localita, data, fascia, temperatura max
    d_temp_max = compute_max(joined_df_extension, 'localita', 'data', 'fascia_extended', 'max(temperatura)')
    #d_temp_max.show()

    # joined df for fascia 3 4 5
    joined_df_tot = d_avg_temp.join(d_avg_pioggia, ['localita', 'data', 'fascia_extended'])\
        .join(d_avg_vento_velocita, ['localita', 'data', 'fascia_extended'])\
        .join(d_avg_vento_direzione, ['localita', 'data', 'fascia_extended'])\
        .join(d_temp_min, ['localita', 'data', 'fascia_extended'])\
        .join(d_temp_max, ['localita', 'data', 'fascia_extended'])\
        .orderBy('data', 'localita', 'fascia_extended')
    joined_df_tot.show()

    return(joined_df_tot)

