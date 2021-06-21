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

df_12 = df_12_d.join(df_12_p, ['localita', 'data', 'fascia'])
df_345 = df_345_d.join(df_345_p, ['localita', 'data', 'fascia_extended'])

df_12.show()
df_345.show()