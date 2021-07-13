from pyspark import SparkContext, SparkConf, SQLContext



# file to write elaborated data (df_12, df_345 with accuracies computed for days 1 2 or 3 4 5)  on two new tables in the database


if __name__ == "__main__":

    # connection
    appName = "PySpark SQL write - via JDBC"
    master = "local[*]"
    conf = SparkConf() \
        .setAppName(appName) \
        .setMaster(master) \
        .set("spark.driver.extraClassPath", "JDBC_connector/mysql-connector-java-8.0.25.jar")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    spark = sqlContext.sparkSession

    # set configuration
    database = "bdt_db_mysql"
    user = "root_bdt"
    password  = "bdt_mysql"
    dbtable_12 = "results_12"
    dbtable_345 = "results_345"
    dbtable_fin_loc = "results_fin_loc"

    jdbcUrl = "jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306/bdt_db_mysql"
    jdbcDriver = "com.mysql.cj.jdbc.Driver"


    # save df_12 into table dbtable_12 in the database
    df_12 = spark.read.csv('csv files/accuracy_12.csv', header=True, sep=",")
    df_12.show()

    df_12.select("*").write.format("jdbc") \
      .mode("overwrite") \
      .option("url", jdbcUrl) \
      .option("dbtable", dbtable_12) \
      .option("user", user) \
      .option("password", password) \
      .save()


    # save df_345 into table dbtable_345 in the database

    df_345 = spark.read.csv('csv files/accuracy_345.csv', header=True, sep=",")
    df_345.show()

    df_345.select("*").write.format("jdbc") \
      .mode("overwrite") \
      .option("url", jdbcUrl) \
      .option("dbtable", dbtable_345) \
      .option("user", user) \
      .option("password", password) \
      .save()



    # save df with final results on localities into table dbtable_fin_loc in the database

    df_loc = spark.read.csv('csv files/res_final_loc.csv', header=True, sep=",")
    df_loc.show()

    df_loc.select("*").write.format("jdbc") \
        .mode("overwrite") \
        .option("url", jdbcUrl) \
        .option("dbtable", dbtable_fin_loc) \
        .option("user", user) \
        .option("password", password) \
        .save()



    '''# Create a data frame by reading data from SQL Server via JDBC
    jdbcDF = spark.read.format("jdbc") \
        .option("url", jdbcUrl) \
        .option("dbtable", dbtable_345) \
        .option("user", user) \
        .option("password", password) \
        .option("driver", jdbcDriver) \
        .load()

    jdbcDF.show()'''