from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType, StringType
import pyspark.sql.functions as F
from pyspark.sql.functions import col


# file to compute statistics and save them


def from_csv(csv_path):
    '''
    Given a csv it returns a pyspark dataframe
    :param csv_path:
    :return:
    '''

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()


    df = spark.read.csv(csv_path, header=True, sep=",")

    for col in df.columns[4:]:
        df = df.withColumn(col, df[col].cast(FloatType()))

    return df


def def_accuracy_range(index_1, index_2):
    '''
    Given the index of real data and the one of prediction, it returns the accuracy of the prediction (1 2 3)
    :param index_1:
    :param index_2:
    :return:
    '''

    if (index_1 == None or index_2 == None or index_1 == -1 or index_2 == -1):
        return None
    if (index_2 == (index_1 + 1) or index_2 == (index_1 - 1)):
        return 2 #'medium'
    elif index_1 == index_2:
        return 3 #'high'
    else:
        return 1 #'inaccurate'

def def_accuracy_range_temp(index_1, index_2):
    '''
    Given the real and predicted temprature, it returns the accuracy of the prediction (1 2 3)
    :param index_1:
    :param index_2:
    :return:
    '''

    if (index_1 == None or index_2 == None or index_1 == -1 or index_2 == -1):
        return None
    if (index_2 <= (index_1 + 1) and index_2 >= (index_1 - 1)):
        return 3#'high'
    elif (index_2 <= (index_1 + 3) and index_2 >= (index_1 - 3)):
        return 2#'medium'
    else:
        return 1#'inaccurate'


def correspondance_dati_prev(df, c1, c2, c_name):
    '''
    Given 2 columns, it compare them to get the accuracy between predictions and real data
    :param df:
    :param c1:
    :param c2:
    :param c_name:
    :return:
    '''

    def_accuracy_range_udf = udf(def_accuracy_range, StringType())
    return df.withColumn(c_name, def_accuracy_range_udf(c1, c2).cast('int'))

def correspondance_dati_prev_temp(df, c1, c2, c_name):
    '''
    Given 2 columns, it compare them to get the accuracy between predictions and real data for tmeperature
    :param df:
    :param c1:
    :param c2:
    :param c_name:
    :return:
    '''

    def_accuracy_range_temp_udf = udf(def_accuracy_range_temp, StringType())
    return df.withColumn(c_name, def_accuracy_range_temp_udf(c1, c2).cast('int'))

'''def correspondence_y_n(df, c1, c2, c_name):
    return df.withColumn(c_name, F.when(((col(c1) == col(c2)) & (col(c1).isNotNull()) & (col(c2).isNotNull())), 'Y').\
                         when(((col(c1) != col(c2)) & (col(c1).isNull()) & (col(c2).isNull())), 'Y').otherwise('N'))'''


def acc_prev(df, column, df_name, exclude_null):
    '''
    It computes the accuracy for one particular measure, so saves the computed accuracies with all the data in a csv file
    :param df:
    :param column:
    :param df_name:
    :param exclude_null:
    :return:
    '''

    if exclude_null:
        df = df.na.drop(subset=[column])

    total = df.count()
    res = (df.groupBy(column).count()
                      .withColumn('total', F.lit(total))
                      .withColumn('fraction', F.expr('count/total')))
    res.show()

    if exclude_null:
        res.toPandas().to_csv('results/' + df_name + column + '.csv')
    else:
        res.toPandas().to_csv('results/NULL_' + df_name + column + '.csv')
    return res

def acc_prev_giorno(df, column, id_giorno_prev_col, id_giorno_prev, exclude_null):
    '''
    It computes the accuracy for one particular measure for a particular day (1 2 3 4 5), so saves the computed accuracies
    with all the data in a csv file
    :param df:
    :param column:
    :param id_giorno_prev_col:
    :param id_giorno_prev:
    :param exclude_null:
    :return:
    '''

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

    if exclude_null:
        x = 'results/' + str(id_giorno_prev) + column + '.csv'
        print(x)
        res.toPandas().to_csv('results/' + str(id_giorno_prev) + column + '.csv')
    else:
        x = 'results/NULL_' + str(id_giorno_prev) + column + '.csv'
        print(x)
        res.toPandas().to_csv('results/NULL_' + str(id_giorno_prev) + column + '.csv')

    return res

def acc_prev_giorno_loc(df, column, localita_col, localita, id_giorno_prev_col, id_giorno_prev, giorno, exclude_null):
    '''
    It computes the accuracy for one particular measure for a particular day (1 2 3 4 5) for one particular station,
    so saves the computed accuracies with all the data in a csv file
    :param df:
    :param column:
    :param localita_col:
    :param localita:
    :param id_giorno_prev_col:
    :param id_giorno_prev:
    :param giorno:
    :param exclude_null:
    :return:
    '''

    if exclude_null:
        df = df.na.drop(subset=[column])

    df = df.where(col(id_giorno_prev_col) == id_giorno_prev)
    df = df.where(col(localita_col) == localita)

    df.show()

    total = df.count()
    res = (df.groupBy(column).count()
                      .withColumn('total', F.lit(total))
                      .withColumn('fraction', F.expr('count/total')))
    res.show()

    if exclude_null:
        x = 'results_localita/' + localita + giorno + column + '.csv'
        print(x)
        res.toPandas().to_csv('results_localita/' + localita + giorno + column + '.csv')
    else:
        x = 'results_localita/NULL_' + localita + giorno + column + '.csv'
        print(x)
        res.toPandas().to_csv('results_localita/NULL_' + localita + giorno + column + '.csv')

    return res


def avg_by_date(df, el, giorni):
    '''
    It computes the avg accuracy for a particular measure for each observed day (from may to july), so saves results into
    csv file
    :param df:
    :param el:
    :param giorni:
    :return:
    '''

    df = df.groupBy('data').avg(el).orderBy('data')  # .orderBy(d, l, f)
    #df = df.select("*", round(col('avg(' + el + ')')))
    df.show()
    df.toPandas().to_csv('data_plots/' + el + '_' + giorni + '.csv')

    return df



if __name__ == "__main__":


    # read df
    df_12 = from_csv('csv files/df_12.csv')
    df_345 = from_csv('csv files/df_345.csv')

    # function to compute accuracies
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

    columns_to_drop = ['_c0']
    df_12 = df_12.drop(*columns_to_drop)
    df_345 = df_345.drop(*columns_to_drop)

    # save df with computed accuracies
    df_12.toPandas().to_csv('csv files/accuracy_12.csv')
    df_345.toPandas().to_csv('csv files/accuracy_345.csv')


    # compute accuracies fractions on overall days

    # no NaN, df_12
    acc_prev(df_12, 'compare_pioggia', '_12_', True)
    acc_prev(df_12, 'compare_vento_vel', '_12_', True)
    acc_prev(df_12, 'compare_vento_dir', '_12_', True)
    acc_prev(df_12, 'compare_temp_max', '_12_', True)
    acc_prev(df_12, 'compare_temp_min', '_12_', True)

    # with Nan , df_12
    acc_prev(df_12, 'compare_pioggia', '_12_null', False)
    acc_prev(df_12, 'compare_vento_vel', '_12_null', False)
    acc_prev(df_12, 'compare_vento_dir', '_12_null', False)
    acc_prev(df_12, 'compare_temp_max', '_12_null', False)
    acc_prev(df_12, 'compare_temp_min', '_12_null', False)

    # no NaN, df_345
    acc_prev(df_345, 'compare_pioggia', '_345_', True)
    acc_prev(df_345, 'compare_vento_vel', '_345_', True)
    acc_prev(df_345, 'compare_vento_dir', '_345_', True)
    acc_prev(df_345, 'compare_temp_max', '_345_', True)
    acc_prev(df_345, 'compare_temp_min', '_345_', True)

    # with Nan, df_345
    acc_prev(df_345, 'compare_pioggia', '_345_null', False)
    acc_prev(df_345, 'compare_vento_vel', '_345_null', False)
    acc_prev(df_345, 'compare_vento_dir', '_345_null', False)
    acc_prev(df_345, 'compare_temp_max', '_345_null', False)
    acc_prev(df_345, 'compare_temp_min', '_345_null', False)


    # compute accuracies for day type

    # day 1 2
    for i in range(1, 3):
        acc_prev_giorno(df_12, 'compare_pioggia', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_12, 'compare_pioggia', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_12, 'compare_vento_vel', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_12, 'compare_vento_vel', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_12, 'compare_vento_dir', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_12, 'compare_vento_dir', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_12, 'compare_temp_max', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_12, 'compare_temp_max', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_12, 'compare_temp_min', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_12, 'compare_temp_min', 'id_previsione_giorno', float(i), False)

    # day 3 4 5
    for i in range(3, 6):
        acc_prev_giorno(df_345, 'compare_pioggia', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_345, 'compare_pioggia', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_345, 'compare_vento_vel', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_345, 'compare_vento_vel', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_345, 'compare_vento_dir', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_345, 'compare_vento_dir', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_345, 'compare_temp_max', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_345, 'compare_temp_max', 'id_previsione_giorno', float(i), False)
        acc_prev_giorno(df_345, 'compare_temp_min', 'id_previsione_giorno', float(i), True)
        acc_prev_giorno(df_345, 'compare_temp_min', 'id_previsione_giorno', float(i), False)


    # compute statitstics for plot with dates may-july

    # df_12
    elements = ['compare_pioggia', 'compare_vento_vel', 'compare_vento_dir', 'compare_temp_max', 'compare_temp_min']
    for i in range(0, 5):
        avg_by_date(df_12, elements[i], '12')

    # df_345
    for i in range(0, 5):
        avg_by_date(df_345, elements[i], '345')



    # code to compute on single stations -> for web

    df_12_acc = from_csv('csv files/accuracy_12.csv')
    df_345_acc = from_csv('csv files/accuracy_345.csv')
    x = df_12_acc.select('localita').distinct().show()

    elements = ['compare_pioggia', 'compare_vento_vel', 'compare_vento_dir', 'compare_temp_max', 'compare_temp_min']

    for i in range(0, 5):
        acc_prev_giorno_loc(df_12_acc, elements[i], 'localita', 'castello tesino', 'id_previsione_giorno', 1, '12',
                            True)

    for i in range(0, 5):
        acc_prev_giorno_loc(df_345_acc, elements[i], 'localita', 'trento', 'id_previsione_giorno',  1, '345', True)

