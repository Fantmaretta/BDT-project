import pyspark.sql.functions as F
from pyspark.sql.functions import col
from pyspark.sql import SparkSession
import argparse

# todo decide what to return
def acc_prev(df, columns, localita_col, localita): # df_12/df_345 , compare_pioggia..., localita, nome_loc -> columns is a list of columns

    '''if localita == "total": # todo maybe delete this one
        total = df.count()
        res = (df.groupBy(column).count()
                          .withColumn('total', F.lit(total))
                          .withColumn('fraction', F.expr('count/total')))'''
    #df1 = df.where(col(localita_col) == localita)
    #df1.show()

    print("The accuracy's fractions for the locality of \"" + localita + "\" follows, with 1.0 = inaccurate, 2.0 = medium accuracy, 3.0 = high accuracy")

    for i in range(0, len(columns)):
        df1 = df.na.drop(subset=columns[i])
        total = df1.count()
        res = (df1.groupBy(columns[i]).count()
               .withColumn('total', F.lit(total))
               .withColumn('fraction', F.expr('count/total')))

        res.show()

    #return res


parser = argparse.ArgumentParser(description='Results from analysis')
parser.add_argument('-localita',
                    type=str,
                    default='total',
                    help='locality for accuracy')
parser.add_argument('-days',
                    type=str,
                    default='1-2',
                    help='accuracy on following day 1-2 or 3-4-5')
parser.add_argument('-type',
                    type=int,
                    default='0',
                    help='accuracy on everything (0), rain (1), wind\'s intensity/direction (2), max/min temperature (3)')

args = parser.parse_args()


if args.days == '1-2':
    query = """SELECT * FROM bdt_db_mysql.results_12 WHERE localita = '{}'""".format(args.localita)
else:
    query = """SELECT * FROM bdt_db_mysql.results_345 WHERE localita = '{}'""".format(args.localita)

if args.type == 0:
    columns = ['compare_pioggia', 'compare_vento_vel', 'compare_vento_dir', 'compare_temp_max', 'compare_temp_min']
elif args.type == 1:
    columns = ['compare_pioggia']
elif args.type == 2:
    columns = ['compare_vento_vel', 'compare_vento_dir']
else:
    columns = ['compare_temp_max', 'compare_temp_min']


sparkConnector = SparkSession.builder.appName("Connector_to_MySQL_BDT") \
    .config("spark.driver.extraClassPath",
            "JDBC_connector/mysql-connector-java-8.0.25.jar") \
    .master('local[*]') \
    .enableHiveSupport() \
    .getOrCreate()


df = sparkConnector.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306") \
    .option("user", "root_bdt") \
    .option("password", "bdt_mysql") \
    .option("driver", 'com.mysql.cj.jdbc.Driver') \
    .option("query", query) \
    .load()
# .option("dbtable", "bdt_db_mysql.dati_reali")
df.show()

# compute accuracy on the requested
acc_prev(df, columns, 'localita', args.localita)
