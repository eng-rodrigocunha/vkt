import pandas as pd
#import numpy as np

df_vkt = pd.read_csv('datasets/2020/vkt_v1.csv', usecols=['Modelo_iCarros_A', 'Modelo_iCarros_B', 'Tipo', 'Marca_Modelo', 'Ano', 'Quantidade'], low_memory=False)
print(df_vkt)
df_vkt = df_vkt.query("Tipo != 'MOTOCICLETA'")
df_vkt = df_vkt.query("Tipo != 'PESADO'")
print(df_vkt)
print(df_vkt[df_vkt[['Modelo_iCarros_A','Modelo_iCarros_B']].isnull().all(axis=1)])
df_vkt = df_vkt[df_vkt[['Modelo_iCarros_A','Modelo_iCarros_B']].isnull().all(axis=1)]
print(df_vkt)
df_vkt = df_vkt.groupby(['Marca_Modelo', 'Ano'])['Quantidade'].sum().sort_values(ascending=False)
print(df_vkt)
df_vkt.to_csv('datasets/2020/vkt_classificacao.csv')

#print(np.percentile(df_vkt2,95))
#df_vkt3 = df_vkt2[df_vkt2 > np.percentile(df_vkt2,95)]
#print(np.percentile(df_vkt['VKT'],95))
#print(df_vkt3)