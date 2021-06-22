import pandas as pd
import numpy as np
from unidecode import unidecode
from difflib import get_close_matches

def get_tipo (modelo):
    motocicleta = ['CG']
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

df_marca_modelo_denatran = pd.read_csv('datasets/2020/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Dezembro_2020.txt', sep=';')
df_marca_modelo_denatran.rename(columns={'Município': 'Municipio', 'Marca Modelo': 'Marca_Modelo', 'Ano Fabricação Veículo CRV': 'Ano', 'Qtd. Veículos': 'Quantidade'}, inplace = True)

df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran[['UF', 'Municipio']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
df_marca_modelo_denatran.reset_index(drop=True, inplace=True)
df_marca_modelo_denatran[['Marca','Modelo']] = df_marca_modelo_denatran['Marca_Modelo'].str.split('/', n=1, expand=True)
df_marca_modelo_denatran[['Modelo_A','Modelo_B']] = df_marca_modelo_denatran['Modelo'].str.split(' ', n=1, expand=True)
#df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['Municipio', 'Modelo_A', 'Ano']).sum().sort_values(by=['Quantidade'], ascending=False)
#df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Quantidade'] > np.percentile(df_marca_modelo_denatran['Quantidade'],95)]

df_marca_modelo5 = pd.read_csv('datasets/marca_modelo_lista5_priority.csv')
#print(df_marca_modelo_denatran)
#print(df_marca_modelo5)
df_marca_modelo_denatran['Modelo_DENATRAN'] = df_marca_modelo_denatran['Modelo_A'].map(lambda x: get_first_list(get_close_matches(x, df_marca_modelo5['Modelo']), n=1))
#df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran.index.get_level_values('Ano')
print('df_marca_modelo_denatran')
print(df_marca_modelo_denatran)
df_marca_modelo_denatran2 = df_marca_modelo_denatran[~df_marca_modelo_denatran['Ano'].apply(lambda x: x.isnumeric())]
print('df_marca_modelo_denatran2')
print(df_marca_modelo_denatran2)
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Ano'].apply(lambda x: x.isnumeric())]
print('df_marca_modelo_denatran')
print(df_marca_modelo_denatran)

df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].astype(np.int64)
df_marca_modelo_denatran['Tipo'] = df_marca_modelo_denatran.index.get_level_values('Modelo_A').map(lambda x: get_tipo(x))

df_marca_modelo_denatran['VKT'] = df_marca_modelo_denatran[['Ano', 'Combustivel']]

df_marca_modelo_denatran.to_csv('datasets/2020/vkt_v0.csv', index=False)