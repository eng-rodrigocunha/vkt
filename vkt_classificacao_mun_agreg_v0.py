import pandas as pd
import numpy as np

df_classificacao_mun_agreg = pd.read_excel('datasets/2020/frota-reg-munic-tipo-modelo-07-dezembro2020.xls', header=3)

df_rms = pd.read_csv('datasets/rms_uf_resumida_rev02.csv')

df_classificacao_mun_agreg = df_classificacao_mun_agreg[df_classificacao_mun_agreg[['UF', 'MUNICIPIO']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
df_classificacao_mun_agreg.reset_index(drop=True, inplace=True)

df_classificacao_mun_agreg['AUTOMOVEL'] = df_classificacao_mun_agreg['AUTOMOVEL'] + df_classificacao_mun_agreg['UTILITARIO'] + df_classificacao_mun_agreg['CAMINHONETE'] + df_classificacao_mun_agreg['CAMIONETA']
df_classificacao_mun_agreg['MOTOCICLETA'] = df_classificacao_mun_agreg['MOTOCICLETA'] + df_classificacao_mun_agreg['CICLOMOTOR'] + df_classificacao_mun_agreg['MOTONETA'] + df_classificacao_mun_agreg['QUADRICICLO'] + df_classificacao_mun_agreg['TRICICLO']
df_classificacao_mun_agreg['PESADO'] = df_classificacao_mun_agreg['CAMINHAO'] + df_classificacao_mun_agreg['CAMINHAO TRATOR'] + df_classificacao_mun_agreg['MICRO-ONIBUS'] + df_classificacao_mun_agreg['ONIBUS']

df_classificacao_mun_agreg = df_classificacao_mun_agreg.drop(columns=['UTILITARIO', 'CICLOMOTOR', 'MOTONETA', 'QUADRICICLO', 'TRICICLO', 'CAMINHAO', 'CAMINHAO TRATOR', 'CAMINHONETE', 'CAMIONETA', 'MICRO-ONIBUS', 'ONIBUS', 'BONDE', 'CHASSI PLATAF', 'REBOQUE', 'SEMI-REBOQUE', 'SIDE-CAR', 'OUTROS', 'TRATOR ESTEI', 'TRATOR RODAS'])

df_rms = df_rms.rename(columns={'Municipio': 'MUNICIPIO'})
df_classificacao_mun_agreg = pd.merge(df_classificacao_mun_agreg, df_rms[['MUNICIPIO', 'UF', 'RM', 'Capital']], on=['MUNICIPIO', 'UF'], how='left')

df_classificacao_mun_agreg.to_csv('datasets/2020/vkt_classificacao_mun_agreg_v3.csv', index=False)

#BONDE	CHASSI PLATAF		REBOQUE	SEMI-REBOQUE	SIDE-CAR	OUTROS	TRATOR ESTEI	TRATOR RODAS	
