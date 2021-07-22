import pandas as pd
import numpy as np

'''df_marca_modelo_denatran = pd.read_csv('datasets/base_denatran_classificacao.csv', sep=';', low_memory=False)

df_marca_modelo_denatran[df_marca_modelo_denatran['Marca Modelo'] == ""] = np.NaN
df_marca_modelo_denatran['Marca Modelo'] = df_marca_modelo_denatran['Marca Modelo'].fillna(method='ffill')

df_marca_modelo_denatran[df_marca_modelo_denatran['Tipo Veículo'] == ""] = np.NaN
df_marca_modelo_denatran['Tipo Veículo'] = df_marca_modelo_denatran['Tipo Veículo'].fillna(method='ffill')

df_marca_modelo_denatran[df_marca_modelo_denatran['Combustível Veiculo'] == ""] = np.NaN
df_marca_modelo_denatran['Combustível Veiculo'] = df_marca_modelo_denatran['Combustível Veiculo'].fillna(method='ffill')

df_marca_modelo_denatran = df_marca_modelo_denatran.melt(id_vars=['Marca Modelo', 'Tipo Veículo', 'Combustível Veiculo'], var_name='Ano', value_name='Quantidade')

df_marca_modelo_denatran = df_marca_modelo_denatran.dropna(subset=['Quantidade'])

df_marca_modelo_denatran.rename(columns={'Marca Modelo': 'Marca_Modelo', 'Tipo Veículo': 'Tipo', 'Combustível Veiculo': 'Combustivel'}, inplace = True)

df_marca_modelo_denatran.to_csv('datasets/base_denatran_classificacao_v1.csv', index=False)
#df_denatrna_gp = df_marca_modelo_denatran.groupby(by=['Marca Modelo'])['Quantidade'].sum()

'''

df_marca_modelo_denatran = pd.read_csv('datasets/base_denatran_classificacao.csv')
#df_marca_modelo_denatran = df_marca_modelo_denatran.drop_duplicates(subset=['Marca_Modelo', 'Tipo', 'Combustivel' ,'Ano'])
df_marca_modelo_denatran['Quantidade'] = df_marca_modelo_denatran['Quantidade'].astype(np.int64)
df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].astype(np.int64)
df_marca_modelo_denatran = df_marca_modelo_denatran.sort_values(by=['Quantidade', 'Ano', 'Marca_Modelo'], ascending=False)
df_marca_modelo_denatran.to_csv('datasets/base_denatran_classificacao.csv', index=False)

'''df_marca_modelo_denatran = df_marca_modelo_denatran[(df_marca_modelo_denatran['Tipo'] != 'Sem Informação') & (df_marca_modelo_denatran['Combustivel'] != 'Sem Informação')]
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