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

def compute_avg(df, l, d, f, var): # on fascia
    return df.groupBy(l, d, f).avg(var).orderBy(d, l, f)

def compute_min(df, l, d, var): # on total day, not fascia
    return df.groupBy(l, d).min(var).orderBy(d, l)

def compute_max(df, l, d, var): # on total day, not fascia
    return df.groupBy(l, d).max(var).orderBy(d, l)


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
    d_temp_min = compute_min(df_dati, 'localita', 'data', 'temperatura')
    d_temp_min.show()

    # df containing localita, data, fascia, temperatura max
    d_temp_max = compute_max(df_dati, 'localita', 'data', 'temperatura')
    d_temp_max.show()

    # joined df for fascia 1 2
    joined_df = d_avg_temp.join(d_avg_pioggia, ['localita', 'data', 'fascia'])\
        .join(d_avg_vento_velocita, ['localita', 'data', 'fascia'])\
        .join(d_avg_vento_direzione, ['localita', 'data', 'fascia'])\
        .join(d_temp_min, ['localita', 'data'])\
        .join(d_temp_max, ['localita', 'data'])\
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
    d_temp_min = compute_min(joined_df_extension, 'localita', 'data', 'min(temperatura)')
    #d_temp_min.show()

    # df containing localita, data, fascia, temperatura max
    d_temp_max = compute_max(joined_df_extension, 'localita', 'data', 'max(temperatura)')
    #d_temp_max.show()

    # joined df for fascia 3 4 5
    joined_df_tot = d_avg_temp.join(d_avg_pioggia, ['localita', 'data', 'fascia_extended'])\
        .join(d_avg_vento_velocita, ['localita', 'data', 'fascia_extended'])\
        .join(d_avg_vento_direzione, ['localita', 'data', 'fascia_extended'])\
        .join(d_temp_min, ['localita', 'data'])\
        .join(d_temp_max, ['localita', 'data'])\
        .orderBy('data', 'localita', 'fascia_extended')
    joined_df_tot.show()

    return(joined_df_tot)


def find_prec_int(x):
        if x == None:
            return None
        elif x >= 0 and x < 5:
            return '1'
        elif x >= 5 and x < 15:
            return '2'
        elif x >= 15 and x <= 40:
            return '3'
        elif x >= 40:
            return '4'
        else:
            return None

def find_vento_dir(x):
    if x == None:
        return None
    elif x >= 348.76 or x <= 11.25:
        return '1'
    elif x >= 11.26 and x <= 33.75:
        return '2'
    elif x >= 33.76 and x <= 56.25:
        return '3'
    elif x >= 56.26 and x <= 78.75:
        return '4'
    elif x >= 78.76 and x <= 101.25:
        return  '5'
    elif x >= 101.26 and x <= 123.75:
        return '6'
    elif x >= 123.76 and x <= 146.25:
        return '7'
    elif x >= 146.26 and x <= 169.75:
        return '8'
    elif x >= 169.76 and x <= 191.25:
        return '9'
    elif x >= 191.26 and x <= 213.75:
        return '10'
    elif x >= 213.76 and x <= 236.25:
        return  '11'
    elif x >= 236.26 and x < 258.75:
        return '12'
    elif x >= 258.76 and x <= 281.25:
        return '13'
    elif x >= 281.26 and x <= 303.75:
        return  '14'
    elif x >= 303.76 and x <= 326.25:
        return '15'
    elif x >= 326.26 and x <= 348.75:
        return '16'
    else:
        return None

def find_vento_int(x):
    if x == None:
        return None
    elif x >= 0 and x < 0.5:
        return '1'
    elif x >= 0.5 and x < 4:
        return '2'
    elif x >= 4 and x < 8:
        return '3'
    elif x >= 8 and x < 14:
        return '4'
    elif x >= 14:
        return '5'
    else:
        return None

