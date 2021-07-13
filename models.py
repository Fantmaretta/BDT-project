import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pyspark.sql import SparkSession
import pickle


class Model:


    def get_df_spark(self):
        '''
        It connect to database, retrieve the table and convert it into pandas df
        :return:
        '''

        sparkConnector = SparkSession.builder.appName("Connector_to_MySQL_BDT") \
            .config("spark.driver.extraClassPath",
                    "JDBC_connector/mysql-connector-java-8.0.25.jar") \
            .master('local[*]') \
            .enableHiveSupport() \
            .getOrCreate()

        query = """SELECT * FROM bdt_db_mysql.results_12"""

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

        pandasDF = df.toPandas()

        return pandasDF


    def prepare_df(self, dataset): # df_path -> 'csv files/accuracy_12.csv'
        '''
        Given the df, it selects the needed columns and removes NaN/incorrect valus
        :param df_path:
        :return:
        '''

        df = dataset[["fascia", "avg(pioggia)", "temp_min", "temp_max", "id_prec_prob", "id_prec_int", "id_vento_val",
                      "id_vento_dir_val"]]
        df = df.dropna()
        indexDel = df[(df['id_prec_prob'] == -1) | (df['id_prec_int'] == -1)].index

        df.drop(indexDel, inplace=True)

        return df


    def prepare_df_path(self, df_path): # df_path -> 'csv files/accuracy_12.csv'
        '''
        Given the df path, it selects the needed columns and removes NaN/incorrect valus
        :param df_path:
        :return:
        '''

        df = pd.read_csv(df_path)

        return self.prepare_df(df)


    def regr_dummies(self, df, file_regr, file_coeff):
        '''
        Given a df, it create X, y for the regression and perform multiple regression with dummy variables if qualitative,
        it returns the regression coefficients and the trained model
        :param df:
        :return:
        '''

        df_1 = df[["fascia", "id_prec_prob", "id_prec_int", "id_vento_val"]]

        col_names = list(df_1)
        for col in col_names:
            df_1[col] = df_1[col].astype('category',copy=False)

        df_1 = pd.get_dummies(df_1)
        df_1["temp_min"] = df["temp_min"]
        df_1["temp_max"] = df["temp_max"]

        print(df_1)
        print(df_1.columns)

        # data preprocessing
        X = df_1.iloc[:, :].values
        y = df.iloc[:, 1].values

        # X, y for regression
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.00000000000000001, random_state=0)

        # Fitting the model
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        # Save the model
        #filename = 'models/regr_model_dummies.sav'
        pickle.dump(regressor, open(file_regr, 'wb'))

        # Coefficients
        coeff = regressor.coef_
        # Save coefficients
        pickle.dump(coeff, open(file_coeff, 'wb'))

        return regressor.coef_, regressor


    def regr_dummies_pred(self, filename, X):
        '''
        Given the regression model and the new X, it predicts the y (avg of rain)
        :param regressor:
        :param X:
        :return:
        '''

        regressor = pickle.load(open(filename, 'rb'))

        # predicting the test set results
        y_pred = regressor.predict(X)
        if y_pred < 0:
            y_pred = 0

        return y_pred


if __name__ == "__main__":

    mod = Model()
    df_spark = mod.get_df_spark()
    df = mod.prepare_df(df_spark)
    # fit the model
    regr = mod.regr_dummies(df, 'models/regr_model_dummies.sav', 'models/coeff.pickle')









# TODO scegliere modello -> predire quantita di pioggia? accuratezza? oppure probabilità che piova? -> qualli variabili usare?
# TODO quale modello usare? regressione? se abbiamo classi? regressione logistca ok solo su due classi'''

