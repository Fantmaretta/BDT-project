from models import Model
import pyspark.sql.functions as F
import argparse
import mysql.connector
import pandas as pd



def acc_prev(df, columns, localita):
    '''
    Given the df containing the comparisons between observations and predictions, it returns the total accuracy for one
    / more types of measures for one stetion
    :param df:
    :param columns:
    :param localita:
    :return:
    '''

    print("The accuracy's fractions for the locality of \"" + localita + "\" follows, with 1.0 = inaccurate, 2.0 = medium accuracy, 3.0 = high accuracy")

    for i in range(0, len(columns)):
        df1 = df.na.drop(subset=columns[i])
        total = df1.count()
        res = (df1.groupBy(columns[i]).count()
               .withColumn('total', F.lit(total))
               .withColumn('fraction', F.expr('count/total')))

        res.show()




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Results from analysis')
    parser.add_argument('-rain_acc',
                        type=int,
                        default=0,
                        help='compute rain\'s prediction (0) or accuracy (1)')
    parser.add_argument('-fascia',
                        type=float,
                        default=0,
                        help='choose time range: 00-06 (0), 06-12 (1), 12-18 (2), 18-24 (3)')
    parser.add_argument('-temp_min',
                        type=float,
                        default=0,
                        help='min temperature')
    parser.add_argument('-temp_max',
                        type=float,
                        default=0,
                        help='max temperature')
    parser.add_argument('-rain_prob',
                        type=float,
                        default=0,
                        help='rain probability: <25% (0), 25-50% (1), 50-75% (2), >75% (3)')
    parser.add_argument('-rain_int',
                        type=float,
                        default=0,
                        help='rain intensity: light (0), moderate (1), heavy (2)')
    parser.add_argument('-wind_speed',
                        type=float,
                        default=0,
                        help='wind speed: <0.5 m/s (0), 0.5-4 m/s (1), 4-8 m/s (2)')
    parser.add_argument('-localita',
                        type=str,
                        default='total',
                        help='locality for accuracy')
    '''parser.add_argument('-days',
                        type=str,
                        default='1-2',
                        help='accuracy on following day 1-2 or 3-4-5')'''
    parser.add_argument('-type',
                        type=int,
                        default='0',
                        help='accuracy on everything (0), rain (1), wind\'s intensity/direction (2), max/min temperature (3)')

    args = parser.parse_args()


    if args.rain_acc == 0:

        input = [0] * 16

        if args.fascia == 0:
            input[0] = 1
            input[1] = 0
            input[2] = 0
            input[3] = 0
        elif args.fascia == 1:
            input[0] = 0
            input[1] = 1
            input[2] = 0
            input[3] = 0
        elif args.fascia == 2:
            input[0] = 0
            input[1] = 0
            input[2] = 1
            input[3] = 0
        else:
            input[0] = 0
            input[1] = 0
            input[2] = 0
            input[3] = 1

        if args.rain_prob == 0:
            input[4] = 1
            input[5] = 0
            input[6] = 0
            input[7] = 0
        elif args.rain_prob == 1:
            input[4] = 0
            input[5] = 1
            input[6] = 0
            input[7] = 0
        elif args.rain_prob == 2:
            input[4] = 0
            input[5] = 0
            input[6] = 1
            input[7] = 0
        else:
            input[4] = 0
            input[5] = 0
            input[6] = 0
            input[7] = 1

        if args.rain_int == 0:
            input[8] = 1
            input[9] = 0
            input[10] = 0
        elif args.rain_int == 1:
            input[8] = 0
            input[9] = 1
            input[10] = 0
        else:
            input[8] = 0
            input[9] = 0
            input[10] = 1

        if args.wind_speed == 0:
            input[11] = 1
            input[12] = 0
            input[13] = 0
        elif args.wind_speed == 1:
            input[11] = 0
            input[12] = 1
            input[13] = 0
        else:
            input[11] = 0
            input[12] = 0
            input[13] = 1

        input[14] = args.temp_min
        input[15] = args.temp_max

        X = [input]

        mod = Model()
        print("The predicted quantity of rain in the selected time range for tomorrow is:",
              mod.regr_dummies_pred('models/regr_model_dummies.sav', X), 'mm')


    else:

        connection = mysql.connector.connect(
            host="bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com",
            port=3306,
            database="bdt_db_mysql",
            user="root_bdt",
            password="bdt_mysql"
        )
        connection.autocommit = True

        cursor = connection.cursor()

        if args.type == 0:
            query = """SELECT * FROM bdt_db_mysql.results_fin_loc WHERE localita = '{}'""".format((args.localita).lower)
            cursor.execute(query)
        elif args.type == 1:
            query = """SELECT * FROM bdt_db_mysql.results_fin_loc WHERE localita = %s and measure = %s"""
            cursor.execute(query, (args.localita, 'compare_pioggia'))
        elif args.type == 2:
            query = """SELECT * FROM bdt_db_mysql.results_fin_loc WHERE localita = %s and (measure = %s or measure = %s)"""
            cursor.execute(query, (args.localita, 'compare_vento_vel', 'compare_vento_dir'))
        else:
            query = """SELECT * FROM bdt_db_mysql.results_fin_loc WHERE localita = %s and (measure = %s or measure = %s)"""
            cursor.execute(query, (args.localita, 'compare_temp_min', 'compare_temp_max'))


        d = {'localita': [], 'measure type': [], 'accuracy': [], 'observed': [], 'total': [], 'fraction': []}
        df = pd.DataFrame(data=d)

        row = cursor.fetchone()

        print("The accuracy levels:\n 1.0 = low accuracy\n 2.0 = medium accuracy\n 3.0 = high accuracy\n")
        while row is not None:
            new_row = {'localita': row[0], 'measure type': row[1], 'accuracy': row[2], 'observed': row[3], 'total': \
                row[4], 'fraction': row[5]}
            row = cursor.fetchone()
            df = df.append(new_row, ignore_index=True)

        df = df.sort_values(by=['measure type', 'accuracy'])

        print(df.to_string())

        cursor.close()