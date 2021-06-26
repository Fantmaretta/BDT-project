from modify_previsioni import *
from modify_dati_reali import *

df_previsioni = initialize_df_p("csv files/df_previsioni.csv")
df_12_p = df_12_p(df_previsioni)
df_345_p = df_345_p(df_previsioni)
df_345_p = df_345_p.withColumnRenamed('fascia', 'fascia_extended')
df_345_p.show()

df_dati = initialize_df_d("csv files/dati_reali_.csv")
df_12_d = df_12(df_dati)
df_345_d = df_345(df_12_d)


df_12_d = df_12_d.withColumn('avg(vento_velocita)', df_12_d['avg(vento_velocita)'].cast('float'))
df_12_d = df_12_d.withColumn('avg(vento_direzione)', df_12_d['avg(vento_direzione)'].cast('float'))
df_12_d = df_12_d.withColumn('avg(pioggia)', df_12_d['avg(pioggia)'].cast('float'))

df_345_d = df_345_d.withColumn('avg(avg(vento_velocita))', df_345_d['avg(avg(vento_velocita))'].cast('float'))
df_345_d = df_345_d.withColumn('avg(avg(vento_direzione))', df_345_d['avg(avg(vento_direzione))'].cast('float'))
df_345_d = df_345_d.withColumn('avg(avg(pioggia))', df_345_d['avg(avg(pioggia))'].cast('float'))


find_vento_int_udf = udf(find_vento_int, StringType())
find_vento_dir_udf = udf(find_vento_dir, StringType())
find_prec_int_udf = udf(find_prec_int, StringType())

df_12_d = df_12_d.withColumn('intensita_vento_dati', find_vento_int_udf(df_12_d['avg(vento_velocita)']))
df_12_d = df_12_d.withColumn('direzione_vento_dati', find_vento_dir_udf(df_12_d['avg(vento_direzione)']))
df_12_d = df_12_d.withColumn('prec_dati', find_prec_int_udf(df_12_d['avg(pioggia)']))

df_345_d = df_345_d.withColumn('intensita_vento_dati', find_vento_int_udf(df_345_d['avg(avg(vento_velocita))']))
df_345_d = df_345_d.withColumn('direzione_vento_dati', find_vento_dir_udf(df_345_d['avg(avg(vento_direzione))']))
df_345_d = df_345_d.withColumn('prec_dati', find_prec_int_udf(df_345_d['avg(avg(pioggia))']))



df_12 = df_12_d.join(df_12_p, ['localita', 'data', 'fascia'])
df_345 = df_345_d.join(df_345_p, ['localita', 'data', 'fascia_extended'])

# TODO y / n
# TODO probabilita prec ???
# TODO ec2 / docker
# TODO report inizio

df_12.show()
df_345.show()

columns_drop = ['desc_prec_prob', 'desc_prec_int', 'id_vento_alt', 'desc_vento_alt', 'id_vento_dir_alt', \
                'desc_vento_dir_alt', 'desc_vento_val', 'desc_vento_dir_val']

df_12 = df_12.drop(*columns_drop)
df_345 = df_345.drop(*columns_drop)

df_12.show()
df_345.show()

df_12.toPandas().to_csv('df_12.csv')
df_345.toPandas().to_csv('df_345.csv')
