import pandas as pd
import numpy as np
from unidecode import unidecode

df_consumo = pd.read_csv('datasets/base_consumo.csv')
#df_consumo['Tipo'] = df_consumo['Tipo'].str.upper()
#df_consumo['Subtipo'] = df_consumo['Subtipo'].str.upper() 
#df_consumo['Combustivel'] = df_consumo['Combustivel'].str.replace('GASOLINA C','GASOLINA')

#print(df_consumo.dtypes)

#df_consumo['Tipo'] = df_consumo['Tipo'].convert_dtypes()
#df_consumo['Tipo'] = df_consumo['Tipo'].apply(unidecode)
#df_consumo['Combustivel'] = df_consumo['Combustivel'].convert_dtypes()
#df_consumo['Combustivel'] = df_consumo['Combustivel'].apply(unidecode)

df_consumo['Subtipo'] = df_consumo['Subtipo'].convert_dtypes()
#df_consumo['Subtipo'] = df_consumo['Subtipo'].apply(lambda x: unidecode(x) if(np.all(pd.notnull(x))) else x)

for index, sub in df_consumo['Subtipo'].iteritems():
    if(type(sub) == str):
        print(sub)
        df_consumo['Subtipo'][index] = unidecode(df_consumo['Subtipo'][index])

#df_marca_modelo_denatran = pd.read_csv('datasets/fator_ciclomotores.csv', sep=';', low_memory=False)
'''df_ciclomotores = pd.read_csv('datasets/fator_ciclomotores.csv')
df_ciclos = pd.read_csv('datasets/fator_ciclos.csv')
df_leves_d = pd.read_csv('datasets/fator_leves_apendice_d.csv')
df_leves_e = pd.read_csv('datasets/fator_leves_apendice_e.csv')
df_pesados = pd.read_csv('datasets/fator_pesados.csv')

df_consumo = pd.DataFrame(columns=['Ano', 'Tipo', 'Subtipo', 'Consumo', 'Combustivel'])

df_ciclomotores['Tipo'] = 'CICLOMOTOR'
df_ciclos['Tipo'] = 'MOTOCICLETA'
df_leves_d['Tipo'] = 'AUTOMOVEL'
df_leves_e['Tipo'] = 'AUTOMOVEL'
df_pesados['Combustivel'] = 'Diesel'

df_consumo = pd.concat([df_consumo, df_ciclomotores, df_ciclos, df_leves_d, df_leves_e, df_pesados])'''


#df_marca_modelo_denatran[df_marca_modelo_denatran['Categoria'] == ""] = np.NaN
#df_marca_modelo_denatran['Categoria'] = df_marca_modelo_denatran['Categoria'].fillna(method='ffill')

'''df_marca_modelo_denatran[df_marca_modelo_denatran['Combustivel'] == ""] = np.NaN
df_marca_modelo_denatran['Combustivel'] = df_marca_modelo_denatran['Combustivel'].fillna(method='ffill')

df_marca_modelo_denatran[df_marca_modelo_denatran['Ano'] == ""] = np.NaN
df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].fillna(method='ffill')'''

#df_marca_modelo_denatran['Consumo'] = df_marca_modelo_denatran['Consumo'].str.replace(',','.')
#df_marca_modelo_denatran['Consumo'] = df_marca_modelo_denatran['Consumo'].astype(float)

#df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].astype(int)

#df_marca_modelo_denatran = df_marca_modelo_denatran.drop(['Unnamed: 3'], axis=1)

df_consumo.to_csv('datasets/base_consumo.csv', index=False)


'''

df_marca_modelo_denatran = pd.read_csv('datasets/base_denatran_classificacao.csv')
#df_marca_modelo_denatran = df_marca_modelo_denatran.drop_duplicates(subset=['Marca_Modelo', 'Tipo', 'Combustivel' ,'Ano'])
df_marca_modelo_denatran['Quantidade'] = df_marca_modelo_denatran['Quantidade'].astype(np.int64)
df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].astype(np.int64)
df_marca_modelo_denatran = df_marca_modelo_denatran.sort_values(by=['Quantidade', 'Ano', 'Marca_Modelo'], ascending=False)
df_marca_modelo_denatran.to_csv('datasets/base_denatran_classificacao.csv', index=False)

df_marca_modelo_denatran = df_marca_modelo_denatran[(df_marca_modelo_denatran['Tipo'] != 'Sem Informação') & (df_marca_modelo_denatran['Combustivel'] != 'Sem Informação')]
df_marca_modelo_denatran.to_csv('datasets/base_denatran_classificacao.csv', index=False)'''


'''df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(by=['Tipo'])['Quantidade'].sum()
print(df_marca_modelo_denatran)
df_marca_modelo_denatran.to_csv('datasets/base_denatran_tipos.csv')'''


#df_denatran_gp = df_marca_modelo_denatran.groupby(by=['Combustivel'])['Quantidade'].sum()

'''
df_denatran_gp.to_csv('datasets/base_denatran_comb.csv')
'''

'''
df_marca_modelo_denatran = pd.read_csv('datasets/base_conv_comb.csv', sep=';')
df_marca_modelo_denatran.to_csv('datasets/base_conv_comb.csv', index=False)
'''