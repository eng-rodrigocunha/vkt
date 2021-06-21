import pandas as pd
import numpy as np
from unidecode import unidecode
from difflib import get_close_matches
import itertools

def get_tipo (modelo):
    motocicleta = ['CG']
    #print(modelo)
    #print(type(modelo))
    #modelo.contains(motocicleta)
    if(any([x in modelo for x in motocicleta])):
        return 'MOTOCICLETA'
    else:
        return 'AUTOMOVEL'

def get_first_list (list):
    if(len(list) > 0):
        return list[0]
    else:
        return ''


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

df_rms = pd.read_csv('datasets/rms.csv')

#df_rms['Municipio'] = df_rms['Municipio_Acentuado'].apply(unidecode)
#df_rms.to_csv('datasets/rms.csv', index=False)

df_marca_modelo_denatran = pd.read_csv('datasets/2020/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Dezembro_2020.txt', sep=';')
df_marca_modelo_denatran.rename(columns={'Município': 'Municipio', 'Marca Modelo': 'Marca_Modelo', 'Ano Fabricação Veículo CRV': 'Ano', 'Qtd. Veículos': 'Quantidade'}, inplace = True)
#df_marca_modelo_denatran[['Marca','Modelo']] = df_marca_modelo_denatran['Marca_Modelo'].str.split("/", expand=True)

#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['UF'].isin(list(set(df_rms['UF'].tolist()))) & df_marca_modelo_denatran['Municipio'].isin(list(set(df_rms['Municipio'].tolist())))]
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran[['UF', 'Municipio']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
df_marca_modelo_denatran.reset_index(drop=True, inplace=True)
#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran['Marca_Modelo'] = df_marca_modelo_denatran['Marca_Modelo'].str.lower()
df_marca_modelo_denatran[['Marca','Modelo']] = df_marca_modelo_denatran['Marca_Modelo'].str.split('/', n=1, expand=True)
df_marca_modelo_denatran[['Modelo_A','Modelo_B']] = df_marca_modelo_denatran['Modelo'].str.split(' ', n=1, expand=True)
#df_marca_modelo_denatran = df_marca_modelo_denatran[~df_marca_modelo_denatran['Modelo_A'].isin(list(set(df_marca_modelo_denatran['Marca'].tolist())))]
df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['Modelo_A', 'Ano']).sum().sort_values(by=['Quantidade'], ascending=False)
#print(df_marca_modelo_denatran)
#print(df_marca_modelo_denatran['Quantidade'])
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Quantidade'] > np.percentile(df_marca_modelo_denatran['Quantidade'],95)]
#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran = df_marca_modelo_denatran.head(25)
#print(df_marca_modelo_denatran)

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
df_marca_modelo = pd.read_csv('datasets/marca_modelo_lista3_priority.csv')
df_marca_modelo.drop_duplicates(subset=['Chave_B'], inplace=True)
#df_marca_modelo['Versao'] = df_marca_modelo['Versao'].str.upper()
df_marca_modelo['Modelo'] = df_marca_modelo['Modelo'].str.upper()
#df_marca_modelo[['Modelo_A','Modelo_B']] = df_marca_modelo['Modelo'].str.split(' ', n=1, expand=True)
#print(df_marca_modelo_denatran.index.names)
#print(df_marca_modelo_denatran.index.get_level_values('Modelo_A'))
#print(df_marca_modelo_denatran.index['Modelo_A'])
#print(df_marca_modelo_denatran.xs(level='Modelo_A'))
#print(df_marca_modelo_denatran['Modelo_A'])
#df_marca_modelo_denatran['Modelo_DENATRAN'] = df_marca_modelo_denatran.index['Modelo_A'].map(lambda x: get_close_matches(x, df_marca_modelo['Versao'], n=1))
#df_marca_modelo_denatran_novo_index = df_marca_modelo_denatran.index.get_level_values('Modelo_A').map(lambda x: get_close_matches(x, df_marca_modelo['Modelo'], n=1))
#print(df_marca_modelo_denatran_novo_index)
df_marca_modelo_denatran['Modelo_DENATRAN'] = df_marca_modelo_denatran.index.get_level_values('Modelo_A').map(lambda x: get_close_matches(x, df_marca_modelo['Modelo'], n=1))
df_marca_modelo_denatran['Modelo_DENATRAN'] = df_marca_modelo_denatran['Modelo_DENATRAN'].map(lambda x: get_first_list(x))
df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran.index.get_level_values('Ano')
#df_marca_modelo_denatran2 = df_marca_modelo_denatran[df_marca_modelo_denatran['Ano'].apply(lambda x: ~x.isnumeric())]
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Ano'].apply(lambda x: x.isnumeric())]
df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].astype(np.int64)
#marca_modelo_denatran_novo_index = df_marca_modelo_denatran_novo_index.to_list()
#marca_modelo_denatran_novo_index = list(itertools.chain.from_iterable(marca_modelo_denatran_novo_index))
#marca_modelo_denatran_novo_index = list(set(marca_modelo_denatran_novo_index))
#print(df_marca_modelo_denatran)

#print(df_marca_modelo_denatran_novo_index)
#df_marca_modelo_denatran = df_marca_modelo_denatran.append(pd.DataFrame(marca_modelo_denatran_novo_index))
#print(df_marca_modelo_denatran)
#df_marca_modelo.query('Modelo_A == @')
df_marca_modelo_denatran['Tipo'] = df_marca_modelo_denatran.index.get_level_values('Modelo_A').map(lambda x: get_tipo(x))
print(df_marca_modelo_denatran)
df_marca_modelo_denatran = df_marca_modelo_denatran.query("Tipo == 'AUTOMOVEL'")
print(df_marca_modelo_denatran)
print(df_marca_modelo)
#df_marca_modelo = df_marca_modelo[df_marca_modelo['Modelo'].isin(df_marca_modelo_denatran['Modelo_DENATRAN']) & df_marca_modelo['Ano'].isin(df_marca_modelo_denatran['Ano'])]
print(df_marca_modelo[['Modelo', 'Ano']].apply(tuple, axis=1))
print(df_marca_modelo_denatran[['Modelo_DENATRAN','Ano']].apply(tuple, axis=1))
df_marca_modelo = df_marca_modelo[df_marca_modelo[['Modelo', 'Ano']].apply(tuple, axis=1).isin(df_marca_modelo_denatran[['Modelo_DENATRAN','Ano']].apply(tuple, axis=1))]
#df_marca_modelo = df_marca_modelo[df_marca_modelo['Modelo'].isin(df_marca_modelo_denatran['Modelo_DENATRAN'])]
#print(df_marca_modelo)
#print(df_marca_modelo.dtypes)
#print(df_marca_modelo_denatran.dtypes)
#df_marca_modelo = df_marca_modelo[df_marca_modelo['Ano'].isin(df_marca_modelo_denatran['Ano'])]
print(df_marca_modelo)
df_marca_modelo.to_csv('datasets/priority_v3.csv', index=False)
#df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['Marca_Modelo2']).sum().sort_values(by=['Quantidade'], ascending=False)
#print(df_marca_modelo_denatran)

#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran.to_csv('datasets/priority.csv')

#df_marca_modelo_denatran = df_marca_modelo_denatran.sort_values(by=['Quantidade'])

#print(df_marca_modelo_denatran)