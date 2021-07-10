from pyspark import SparkContext, SparkConf, SQLContext


if __name__ == "__main__":
    appName = "PySpark SQL write - via JDBC"
    master = "local[*]"
    conf = SparkConf() \
        .setAppName(appName) \
        .setMaster(master) \
        .set("spark.driver.extraClassPath", "JDBC_connector/mysql-connector-java-8.0.25.jar")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    spark = sqlContext.sparkSession

    database = "bdt_db_mysql"
    src_table = "results_12"
    user = "root_bdt"
    password  = "bdt_mysql"
    dbtable_12 = "results_12"
    dbtable_345 = "results_345"


    jdbcUrl = "jdbc:mysql://bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com:3306/bdt_db_mysql"
    jdbcDriver = "com.mysql.cj.jdbc.Driver"
    # Create a data frame by reading data from SQL Server via JDBC
    jdbcDF = spark.read.format("jdbc") \
        .option("url", jdbcUrl) \
        .option("dbtable", dbtable_345) \
        .option("user", user) \
        .option("password", password) \
        .option("driver", jdbcDriver) \
        .load()

    jdbcDF.show()


    df_12 = spark.read.csv('csv files/accuracy_12.csv', header=True, sep=",")
    df_12.show()

    df_12.select("*").write.format("jdbc") \
      .mode("overwrite") \
      .option("url", jdbcUrl) \
      .option("dbtable", dbtable_12) \
      .option("user", user) \
      .option("password", password) \
      .save()


    df_345 = spark.read.csv('csv files/accuracy_345.csv', header=True, sep=",")
    df_345.show()

    df_345.select("*").write.format("jdbc") \
      .mode("overwrite") \
      .option("url", jdbcUrl) \
      .option("dbtable", dbtable_345) \
      .option("user", user) \
      .option("password", password) \
      .save()

