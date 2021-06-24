#from _typeshed import NoneType
import pandas as pd
import numpy as np
import math
from unidecode import unidecode
from difflib import get_close_matches

def get_tipo (modelo):
    #print(modelo)
    motocicleta = ['CG', 'YS', 'YBS', 'FAZER', 'CBX', 'BIZ', 'CB', 'XRE', 'YBR', 'NXR', 'SUZUKI', 'POP', 'PCX', 'SPEED', 'NMAX']
    #onibus = ['']
    #caminhao = ['']
    for m in modelo:
        if(m is None):
            continue
        if(any([x in m for x in motocicleta])):
            return 'MOTOCICLETA'
        #elif(any([x in modelo for x in onibus])):
        #    return 'ONIBUS'
        #elif(any([x in modelo for x in caminhao])):
        #    return 'CAMINHAO'
    return 'AUTOMOVEL'

def get_vkt (df, ano_base):
    if(df['Tipo'] == 'AUTOMOVEL'):
        if(df['Combustivel'] == 'FLEX'):
            return vkt_flex(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'GASOLINA'):
            return vkt_gasolina(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'ETANOL'):
            return vkt_gasolina(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'ETANOL'):
            return vkt_diesel(df['Ano'], ano_base)
        else:
            return vkt_gasolina(df['Ano'], ano_base)
    elif(df['Tipo'] == 'MOTOCICLETA'):
        return vkt_motocicleta(df['Ano'], ano_base)
    elif(df['Tipo'] == 'ONIBUS'):
        return vkt_onibus(df['Ano'], ano_base)
    elif(df['Tipo'] == 'CAMINHAO'):
        return vkt_caminhao(df['Ano'], ano_base)
    else:
        return 'ERRO'

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
        return (-3.292*(idade**3) + 174.31*(idade**2) - 3083.6*idade + 31628)

def vkt_flex (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 10):
        return "ERRO"
    elif(idade > 8):
        return 15000
    else:
        return (-24.288*(idade**3) + 426.19*(idade**2) - 2360.4*idade + 19178)

def vkt_diesel (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 8):
        return 13040
    else:
        return (-64.592*(idade**3) + 720.31*(idade**2) - 2280.8*idade + 19242)


def vkt_motocicleta (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 17):
        return 9050
    else:
        return (1.3392*(idade**3) - 60.492*(idade**2) + 442.92*idade + 12423)

def vkt_caminhao (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 60):
        return "ERRO"
    elif(idade > 40):
        return 21804
    else:
        return (0.0774*(idade**4) - 7.3952*(idade**3) + 249.38*(idade**2) - 3664*idade + 44505)

def vkt_onibus (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 15):
        return 64108*math.exp(-0.046*idade)
    else:
        return (-8.8551*(idade**3) + 263.41*(idade**2) - 4219.4*idade + 66435)

def get_close_model_a (df_denatran):
    #print(df_denatran)
    if(df_denatran['Tipo'] != 'AUTOMOVEL'):
        return ''
    
    model = get_close_matches(df_denatran.name[0], df_marca_modelo5['Modelo_A'], n=1)

    if(len(model) > 0):
        return model[0]
    else:
        return ''

def get_close_model_b (df_denatran):
    #print(df_denatran)
    #print(df_denatran.name[0])
    #print(df_denatran.name[1])
    if(df_denatran['Tipo'] != 'AUTOMOVEL' or df_denatran.name[0] != ''):
        return ''
    
    model = get_close_matches(df_denatran.name[1], df_marca_modelo5['Modelo_A'], n=1)

    if(len(model) > 0):
        return model[0]
    else:
        return ''

df_rms = pd.read_csv('datasets/rms.csv')

df_marca_modelo_denatran = pd.read_csv('datasets/2020/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Dezembro_2020.txt', sep=';')
df_marca_modelo_denatran.rename(columns={'Município': 'Municipio', 'Marca Modelo': 'Marca_Modelo', 'Ano Fabricação Veículo CRV': 'Ano', 'Qtd. Veículos': 'Quantidade'}, inplace = True)

df_marca_modelo5 = pd.read_csv('datasets/marca_modelo_lista5_priority.csv')
df_marca_modelo5.rename(columns={'Modelo': 'Modelo_A'}, inplace = True)
df_marca_modelo5['Ano'] = df_marca_modelo5['Ano'].astype(np.int64)

df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran[['UF', 'Municipio']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
df_marca_modelo_denatran.reset_index(drop=True, inplace=True)
df_marca_modelo_denatran[['Marca','Modelo']] = df_marca_modelo_denatran['Marca_Modelo'].str.split('/', n=1, expand=True)
df_marca_modelo_denatran[['Modelo_A','Modelo_B','Modelo_C']] = df_marca_modelo_denatran['Modelo'].str.split(' ', n=2, expand=True)
df_marca_modelo_denatran_null = df_marca_modelo_denatran[df_marca_modelo_denatran['Modelo_A'].isnull()]
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Modelo_A'].notnull()]
df_marca_modelo_denatran['Tipo'] = df_marca_modelo_denatran[['Modelo_A', 'Modelo_B']].apply(lambda x: get_tipo(x), axis=1)

df_marca_modelo_denatran_modelos = df_marca_modelo_denatran.groupby(['Modelo_A', 'Modelo_B']).sum().sort_values(by=['Quantidade'], ascending=False)
#print(df_marca_modelo_denatran_modelos)
df_marca_modelo_denatran_modelos = df_marca_modelo_denatran_modelos[df_marca_modelo_denatran_modelos['Quantidade'] > np.percentile(df_marca_modelo_denatran_modelos['Quantidade'],95)]
#print(df_marca_modelo_denatran_modelos)

df_marca_modelo_denatran_modelos['Tipo'] = df_marca_modelo_denatran_modelos.index.map(lambda x: get_tipo(x))
#df_marca_modelo_denatran_modelos['Modelo_iCarros_A'] = df_marca_modelo_denatran_modelos[['Ano', 'Combustivel', 'Tipo']].apply(lambda x: get_vkt(x, 2020), axis=1)
df_marca_modelo_denatran_modelos['Modelo_iCarros_A'] = df_marca_modelo_denatran_modelos.apply(get_close_model_a, axis=1)
df_marca_modelo_denatran_modelos['Modelo_iCarros_B'] = df_marca_modelo_denatran_modelos.apply(get_close_model_b, axis=1)

df_marca_modelo_denatran_sem_ano = df_marca_modelo_denatran[~df_marca_modelo_denatran['Ano'].map(lambda x: x.isnumeric())]
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['Ano'].map(lambda x: x.isnumeric())]
df_marca_modelo_denatran['Ano'] = df_marca_modelo_denatran['Ano'].astype(np.int64)

df_marca_modelo_denatran = pd.merge(df_marca_modelo_denatran, df_marca_modelo_denatran_modelos['Modelo_iCarros_A'], on='Modelo_A', how='outer')
df_marca_modelo_denatran = pd.merge(df_marca_modelo_denatran, df_marca_modelo_denatran_modelos['Modelo_iCarros_B'], on='Modelo_B', how='outer')
df_marca_modelo_denatran = pd.merge(df_marca_modelo_denatran, df_marca_modelo5[['Modelo_A', 'Ano', 'Combustivel', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']], on=['Modelo_A', 'Ano'], how='outer')
df_marca_modelo_denatran = pd.merge(df_marca_modelo_denatran, df_rms[['Municipio', 'RM', 'Capital']], on='Municipio', how='outer')

#print(df_marca_modelo_denatran)
df_marca_modelo_denatran['VKT'] = df_marca_modelo_denatran[['Ano', 'Combustivel', 'Tipo']].apply(lambda x: get_vkt(x, 2020), axis=1)
#df_marca_modelo_denatran = df_marca_modelo_denatran.query("'VKT' != 'ERRO'")
df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['VKT'] != 'ERRO']
#print(df_marca_modelo_denatran)
df_marca_modelo_denatran['VKT'] = df_marca_modelo_denatran['VKT']*df_marca_modelo_denatran['Quantidade']
#print(df_marca_modelo_denatran)
#df_marca_modelo_denatran = df_marca_modelo_denatran[df_marca_modelo_denatran['VKT'] < 0]

df_marca_modelo_denatran.to_csv('datasets/2020/vkt_v1.csv', index=False)

df_marca_modelo_denatran = df_marca_modelo_denatran.groupby(['RM'])['VKT'].sum()
df_marca_modelo_denatran.to_csv('datasets/2020/vkt_v1_rm.csv')