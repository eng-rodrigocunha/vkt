import pandas as pd
import numpy as np
from unidecode import unidecode
from difflib import get_close_matches
import itertools

def vkt_gasolina (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 40):
        return 6174
    else:
        return (0.6716*(idade**3) - 49.566*(idade**2) + 779.66*idade + 11266)

def vkt_etanol (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 28):
        return 8275
    else:
        return (-3.292*(idade**3) - 174.31*(idade**2) + 3083.6*idade + 31628)

def vkt_flex (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 10):
        return "ERRO"
    elif(idade > 8):
        return 15000
    else:
        return (-24.288*(idade**3) - 426.19*(idade**2) + 2360.4*idade + 19178)

df_rms = pd.read_csv('datasets/rms_bkp.csv')

df_rms['Capital'] = df_rms['Capital'].apply(unidecode).str.upper()
#df_rms['Municipio'] = df_rms['Municipio_Acentuado']
df_rms = df_rms.drop(['Municipio_Acentuado'], axis=1)
df_rms.to_csv('datasets/rms.csv', index=False)

'''
df_marca_modelo_denatran = pd.read_csv('datasets/2020/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Dezembro_2020.txt', sep=';')
df_marca_modelo_denatran.rename(columns={'Município': 'Municipio', 'Marca Modelo': 'Marca_Modelo', 'Ano Fabricação Veículo CRV': 'Ano', 'Qtd. Veículos': 'Quantidade'}, inplace = True)
#df_marca_modelo_denatran[['Marca','Modelo']] = df_marca_modelo_denatran['Marca_Modelo'].str.split("/", expand=True)

#print(df_marca_modelo_denatran)
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['UF'].isin(list(set(df_rms['UF'].tolist()))) & df_marca_modelo_denatran['Municipio'].isin(list(set(df_rms['Municipio'].tolist())))]
df_marca_modelo_denatran.reset_index(drop=True, inplace=True)
#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran['Marca_Modelo'] = df_marca_modelo_denatran['Marca_Modelo'].str.lower()
df_marca_modelo_denatran[['Marca','Modelo']] = df_marca_modelo_denatran['Marca_Modelo'].str.split('/', n=1, expand=True)
df_marca_modelo_denatran[['Modelo_A','Modelo_B']] = df_marca_modelo_denatran['Modelo'].str.split(' ', n=1, expand=True)
df_marca_modelo_denatran = df_marca_modelo_denatran[~df_marca_modelo_denatran['Modelo_A'].isin(list(set(df_marca_modelo_denatran['Marca'].tolist())))]
df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['Modelo_A']).sum().sort_values(by=['Quantidade'], ascending=False)
print(df_marca_modelo_denatran)
#print(df_marca_modelo_denatran['Quantidade'])
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Quantidade'] > np.percentile(df_marca_modelo_denatran['Quantidade'],95)]
print(df_marca_modelo_denatran)

#df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['Marca_Modelo','Ano','Municipio']).mean().sort_values(by=['Quantidade'], ascending=False).head(25)

#df_marca_modelo = pd.read_csv('marca_modelo_lista3.csv')
#marcas = ['BMW', 'Audi', 'Lexus', 'Volvo', 'Jaguar']
#df_marca_modelo = df_marca_modelo[~df_marca_modelo['Marca'].isin(marcas)]
#df_marca_modelo = df_marca_modelo.query("Marca != 'BMW'")
#df_marca_modelo = df_marca_modelo.query("Marca != 'Audi'")
#df_marca_modelo = df_marca_modelo.query("Marca != 'Lexus'")
#df_marca_modelo = df_marca_modelo.query("Marca != 'Volvo'")
#df_marca_modelo['Marca_Modelo'] = df_marca_modelo.apply(lambda x: '{}/{}'.format(x['Marca'], x['Modelo']), axis=1)
#df_marca_modelo.query("Combustivel_Gasolina != ''")
#df_marca_modelo.drop_duplicates(subset=['Versao'], inplace=True)
#print(df_marca_modelo)
#print(df_marca_modelo)
#df_marca_modelo_denatran.drop_duplicates(subset=['Marca_Modelo'], inplace=True)
df_marca_modelo = pd.read_csv('marca_modelo_lista2.csv')
df_marca_modelo['Modelo'] = df_marca_modelo['Modelo'].str.upper()
df_marca_modelo[['Modelo_A','Modelo_B']] = df_marca_modelo['Modelo'].str.split(' ', n=1, expand=True)
#print(df_marca_modelo_denatran.index)
#print(df_marca_modelo_denatran.index)
df_marca_modelo_denatran_novo_index = df_marca_modelo_denatran.index.map(lambda x: get_close_matches(x, df_marca_modelo['Modelo_A'], n=1))
df_marca_modelo_denatran_novo_index = df_marca_modelo_denatran_novo_index.to_list()
df_marca_modelo_denatran_novo_index = list(itertools.chain.from_iterable(df_marca_modelo_denatran_novo_index))
#df_marca_modelo_denatran_novo_index = list(set(df_marca_modelo_denatran_novo_index))

#print(df_marca_modelo_denatran_novo_index)
#df_marca_modelo.query('Modelo_A == @')
#print(df_marca_modelo)
df_marca_modelo = df_marca_modelo[df_marca_modelo['Modelo_A'].isin(df_marca_modelo_denatran_novo_index)]
#print(df_marca_modelo)
df_marca_modelo.to_csv('datasets/priority_v1.csv', index=False)
#df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['Marca_Modelo2']).sum().sort_values(by=['Quantidade'], ascending=False)
#print(df_marca_modelo_denatran)

#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran.to_csv('datasets/priority.csv')

#df_marca_modelo_denatran = df_marca_modelo_denatran.sort_values(by=['Quantidade'])

#print(df_marca_modelo_denatran)
'''