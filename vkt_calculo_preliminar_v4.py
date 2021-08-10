import pandas as pd
import numpy as np
import math
from unidecode import unidecode
from difflib import get_close_matches

def get_vkt_preliminar (df, ano_base):
    if(df['Tipo'] == 'AUTOMOVEL'):
        if(df['Combustivel'] == 'FLEX'):
            return vkt_flex(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'GASOLINA'):
            return vkt_gasolina(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'ALCOOL'):
            return vkt_alcool(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'GASOLINA/GNV'):
            return vkt_gasolina_gnv(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'FLEX/GNV'):
            return vkt_flex_gnv(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'DIESEL'):
            return vkt_util_diesel(df['Ano'], ano_base)
    elif(df['Tipo'] in ['UTILITARIO', 'CAMIONETA']):
        if(df['Combustivel'] == 'GASOLINA'):
            return vkt_util_gasolina(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'FLEX'):
            return vkt_util_flex(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'DIESEL'):
            return vkt_util_diesel(df['Ano'], ano_base)
        elif(df['Combustivel'] == 'ALCOOL'):
            return vkt_alcool(df['Ano'], ano_base)
    elif(df['Tipo'] == 'CAMINHAO'):
        return vkt_caminhao(df['Ano'], ano_base)
    elif(df['Tipo'] == 'CAMINHONETE'):
        return vkt_caminhonete(df['Ano'], ano_base)
    elif(df['Tipo'] == 'ONIBUS'):
        return vkt_onibus(df['Ano'], ano_base)
    elif(df['Tipo'] == 'MICROONIBUS'):
        return vkt_microonibus(df['Ano'], ano_base)
    elif(df['Tipo'] == 'CAMINHAO TRATOR'):
        return vkt_caminhao_trator(df['Ano'], ano_base)
    elif(df['Tipo'] in ['MOTOCICLETA', 'CICLOMOTOR', 'TRICICLO', 'QUADRICICLO']):
        return vkt_motociclo(df['Ano'], ano_base)
    elif(df['Tipo'] == 'MOTONETA'):
        return vkt_motoneta(df['Ano'], ano_base)
    else:
        return np.nan

def vkt_gasolina (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 40):
        return 6174
    else:
        return (0.6716*(idade**3) - 49.566*(idade**2) + 779.66*idade + 11266)

def vkt_alcool (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 28):
        return 8275
    else:
        return (-3.292*(idade**3) + 174.31*(idade**2) - 3083.6*idade + 31628)

def vkt_flex (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 10):
        return np.nan
    elif(idade > 8):
        return 15000
    elif(idade == 1):
        return 17220
    else:
        return (-24.288*(idade**3) + 426.19*(idade**2) - 2360.4*idade + 19178)

def vkt_util_gasolina (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 36):
        return 7862
    else:
        return (0.3623*(idade**3) - 13.828*(idade**2)- 255.77*idade + 18202)

def vkt_util_flex (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 36):
        return 7862
    else:
        return (107.39*(idade**3) - 1687.3*(idade**2) + 7200.5*idade + 12599)

def vkt_caminhao (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 60):
        return np.nan
    elif(idade > 40):
        return 21804
    else:
        return (0.0774*(idade**4) - 7.3952*(idade**3) + 249.38*(idade**2) - 3664*idade + 44505)

def vkt_caminhonete (ano_fab, ano_base):
    # Modelo ajustado para a intensidade de uso das Caminhonetes diesel
    idade = ano_base - ano_fab
    if (idade > 10):
        return 15950
    else:
        return (-10.399*(idade**3) + 86.398*(idade**2) - 1271.3*idade + 29638)

def vkt_onibus (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 15):
        return 64108*math.exp(-0.046*idade)
    else:
        return (-8.8551*(idade**3) + 263.41*(idade**2) - 4219.4*idade + 66435)

def vkt_util_diesel (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 8):
        return 13040
    else:
        return (-64.592*(idade**3) + 720.31*(idade**2) - 2280.8*idade + 19242)

def vkt_microonibus (ano_fab, ano_base):
    idade = ano_base - ano_fab
    #Realizado ajuste para idade == 0
    if (idade > 15):
        return 18680
    elif (idade == 0):
        return 35578
    else:
        return (-5661*(math.log(idade)) + 35578)

def vkt_caminhao_trator (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if(idade > 52):
        return np.nan
    else:
        return (-1023.7*idade + 57247)

def vkt_motociclo (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 17):
        return 9050
    else:
        return (1.3392*(idade**3) - 60.492*(idade**2) + 442.92*idade + 12423)

def vkt_motoneta (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 10):
        return (951491.4958*(idade**(-1.9209)))
    else:
        return (-35.147*(idade**3) + 620.87*(idade**2) - 2970.3*idade + 11431)

def vkt_gasolina_gnv (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade == 0):
        return np.nan
    else:
        return (37958*(idade**(-0.291)))

def vkt_flex_gnv (ano_fab, ano_base):
    idade = ano_base - ano_fab
    if (idade > 8):
        return 10370
    else:
        return (962.27*(idade**2) - 14191*idade + 76436)

def get_close_model (df_denatran):
    model = df_marca_modelo5[df_denatran == df_marca_modelo5['Modelo_A']].head(1)

    if(len(model) > 0):
        return model['Modelo_A'].item()

    model = get_close_matches(df_denatran, df_marca_modelo5['Modelo_A'], n=1, cutoff=0.7)

    if(len(model) > 0):
        return model[0]
    else:
        return np.nan

def get_comb (df_denatran):
    gasolina = np.nan
    alcool = np.nan
    diesel = np.nan

    if((np.isnan(df_denatran['Consumo_Cidade_Gasolina_A'])) & (np.isnan(df_denatran['Consumo_Cidade_Gasolina_B'])) & (np.isnan(df_denatran['Consumo_Cidade_Gasolina_C'])) & (np.isnan(df_denatran['Consumo_Cidade_Alcool_A'])) & (np.isnan(df_denatran['Consumo_Cidade_Alcool_B'])) & (np.isnan(df_denatran['Consumo_Cidade_Alcool_C']))):
        return [gasolina, alcool, diesel]

    if((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_A'])) & (df_denatran['Combustivel_Gasolina_A'] == 'Gasolina')):
        gasolina = df_denatran['Consumo_Cidade_Gasolina_A']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_B'])) & (df_denatran['Combustivel_Gasolina_B'] == 'Gasolina')):
        gasolina = df_denatran['Consumo_Cidade_Gasolina_B']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_C'])) & (df_denatran['Combustivel_Gasolina_C'] == 'Gasolina')):
        gasolina = df_denatran['Consumo_Cidade_Gasolina_C']

    if((~np.isnan(df_denatran['Consumo_Cidade_Alcool_A'])) & (df_denatran['Combustivel_Alcool_A'] == 'Alcool')):
        alcool = df_denatran['Consumo_Cidade_Alcool_A']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Alcool_B'])) & (df_denatran['Combustivel_Alcool_B'] == 'Alcool')):
        alcool = df_denatran['Consumo_Cidade_Alcool_B']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Alcool_C'])) & (df_denatran['Combustivel_Alcool_C'] == 'Alcool')):
        alcool = df_denatran['Consumo_Cidade_Alcool_C']

    if((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_A'])) & (df_denatran['Combustivel_Gasolina_A'] == 'Alcool')):
        alcool = df_denatran['Consumo_Cidade_Gasolina_A']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_B'])) & (df_denatran['Combustivel_Gasolina_B'] == 'Alcool')):
        alcool = df_denatran['Consumo_Cidade_Gasolina_B']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_C'])) & (df_denatran['Combustivel_Gasolina_C'] == 'Alcool')):
        alcool = df_denatran['Consumo_Cidade_Gasolina_C']

    if((~np.isnan(df_denatran['Consumo_Cidade_Alcool_A'])) & (df_denatran['Combustivel_Alcool_A'] == 'Gasolina')):
        gasolina = df_denatran['Consumo_Cidade_Alcool_A']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Alcool_B'])) & (df_denatran['Combustivel_Alcool_B'] == 'Gasolina')):
        gasolina = df_denatran['Consumo_Cidade_Alcool_B']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Alcool_C'])) & (df_denatran['Combustivel_Alcool_C'] == 'Gasolina')):
        gasolina = df_denatran['Consumo_Cidade_Alcool_C']

    if((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_A'])) & (df_denatran['Combustivel_Gasolina_A'] == 'Diesel')):
        diesel = df_denatran['Consumo_Cidade_Gasolina_A']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_B'])) & (df_denatran['Combustivel_Gasolina_B'] == 'Diesel')):
        diesel = df_denatran['Consumo_Cidade_Gasolina_B']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Gasolina_C'])) & (df_denatran['Combustivel_Gasolina_C'] == 'Diesel')):
        diesel = df_denatran['Consumo_Cidade_Gasolina_C']

    if((~np.isnan(df_denatran['Consumo_Cidade_Alcool_A'])) & (df_denatran['Combustivel_Alcool_A'] == 'Diesel')):
        diesel = df_denatran['Consumo_Cidade_Alcool_A']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Alcool_B'])) & (df_denatran['Combustivel_Alcool_B'] == 'Diesel')):
        diesel = df_denatran['Consumo_Cidade_Alcool_B']
    elif((~np.isnan(df_denatran['Consumo_Cidade_Alcool_C'])) & (df_denatran['Combustivel_Alcool_C'] == 'Diesel')):
        diesel = df_denatran['Consumo_Cidade_Alcool_C']

    return [gasolina, alcool, diesel]

'''
def fill_comb_gasolina(g):
    gNotNull = g.dropna()

    #if(len(gNotNull.index) == 0):
    #    return #g['Consumo_Gasolina']

    #if((sum(gNotNull['Quantidade']) == 0) | (sum(gNotNull['Consumo_Gasolina']) == 0)):
    #    return #g['Consumo_Gasolina']

    #print(g)
    #print(gNotNull)

    try:
        wtAvg = np.average(gNotNull['Consumo_Gasolina'], weights=gNotNull['Quantidade'])
        return g['Consumo_Gasolina'].fillna(wtAvg)
    except:
        return g['Consumo_Gasolina']
'''

def get_consumo(comb, df):
    #idade = ano_base - df['Ano']
    ano = df['Ano']
    consumo = []

    '''print(type(comb))
    print(type(df['Combustivel']))'''

    if((comb not in df['Combustivel']) & (df['Combustivel'] != 'FLEX')):
        return np.nan

    elif((df['Tipo'] in ['AUTOMOVEL', 'UTILITARIO', 'CAMINHONETE', 'CAMIONETA']) & (comb in ['FLEX', 'ALCOOL', 'GASOLINA'])):
        if(ano < 1982):
            ano = 1982

        consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'AUTOMOVEL') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']

    elif((df['Tipo'] in ['AUTOMOVEL', 'UTILITARIO', 'CAMINHONETE', 'CAMIONETA']) & (comb == 'DIESEL')):
        if(ano < 1999):
            ano = 1999

        consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'CAMINHAO') & (df_base_consumo['Subtipo'] == 'SEMILEVES') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']

    elif((df['Tipo'] == 'CAMINHAO') | (df['Tipo'] == 'CAMINHAO TRATOR')):
        if(ano < 1999):
            ano = 1999

        consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'CAMINHAO') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']
        #print(consumo)

    elif(df['Tipo'] == 'CICLOMOTOR'):
        consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'CICLOMOTOR') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']        

    elif(df['Tipo'] in ['MOTOCICLETA', 'MOTONETA', 'QUADRICICLO', 'TRICICLO']):
        consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'MOTOCICLETA') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']        

    elif(df['Tipo'] == 'MICROONIBUS'):
        if(ano < 1999):
            ano = 1999

        consumo = df_base_consumo[(df_base_consumo['Subtipo'] == 'MICROONIBUS') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']        

    elif(df['Tipo'] == 'ONIBUS'):
        if(ano < 1999):
            ano = 1999
            
        consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'ONIBUS') & (df_base_consumo['Subtipo'] != 'MICROONIBUS') & (df_base_consumo['Ano'] == ano) & (df_base_consumo['Combustivel'].str.contains(comb))]['Consumo']        

    if (len(consumo) == 0):
        consumo = np.nan
    else:
        consumo = consumo.mean()

    return consumo

'''def get_flex(df):
    #preco_gasolina = df_preco_comb_rm[((df_preco_comb_rm['Produto'] == 'GASOLINA') & (df_preco_comb_rm['Ano'] == ano) & (df_preco_comb_rm['RM'] == df['RM']))]['Preco_Venda']
    #preco_alcool = df_preco_comb_rm[((df_preco_comb_rm['Produto'] == 'ALCOOL') & (df_preco_comb_rm['Ano'] == ano) & (df_preco_comb_rm['RM'] == df['RM']))]['Preco_Venda']

    rel = df_preco_comb_rm_anual[((df_preco_comb_rm_anual['RM'] == df['RM']))]['Relacao']

    alcool = df['VKT_Preliminar']*rel/df['Consumo_Alcool']
    gasolina = df['VKT_Preliminar']*(1-rel)/df['Consumo_Gasolina']

    return [gasolina, alcool]'''

def get_vkt (df):
    #df_denatran[['VKT_Preliminar', 'Combustivel', 'Fator_Alcool', 'Fator_Gasolina', 'Fator_Diesel']]
    if(df['Combustivel'] == 'ALCOOL'):
        vkt = df['VKT_Preliminar']*df['Fator_Alcool']

    elif(df['Combustivel'] == 'GASOLINA'):
        vkt = df['VKT_Preliminar']*df['Fator_Gasolina']
    
    elif(df['Combustivel'] == 'DIESEL'):
        vkt = df['VKT_Preliminar']*df['Fator_Diesel']

    elif(df['Combustivel'] == 'FLEX'):
        vkt = df['VKT_Preliminar']*df['Relacao']*df['Fator_Alcool'] + df['VKT_Preliminar']*(1-df['Relacao'])*df['Fator_Gasolina']

    return vkt

def get_sucat (df, ano_base):
    idade = ano_base - df['Ano']

    if((df['Tipo'] == 'AUTOMOVEL') & (df['Combustivel'] != 'DIESEL')):
        return ((1-math.exp(-math.exp(1.798+(-0.137*idade))))*df['Quantidade'])
    
    elif((df['Tipo'] in ['UTILITARIO', 'CAMIONETA']) & (df['Combustivel'] != 'DIESEL')):
        return ((1-math.exp(-math.exp(1.618+(-0.141*idade))))*df['Quantidade'])

    elif((df['Tipo'] in ['AUTOMOVEL', 'UTILITARIO', 'CAMIONETA']) & (df['Combustivel'] == 'DIESEL')):
        return (((1/(1+math.exp(0.17*(idade-15.3))))+(1/(1+math.exp(0.17*(idade+15.3)))))*df['Quantidade'])

    elif((df['Tipo'] in ['CAMINHAO', 'CAMINHONETE', 'CAMINHAO TRATOR']) & (df['Combustivel'] == 'DIESEL')):
        return (((1/(1+math.exp(0.10*(idade-17))))+(1/(1+math.exp(0.10*(idade+17)))))*df['Quantidade'])

    elif((df['Tipo'] in ['ONIBUS', 'MICROONIBUS']) & (df['Combustivel'] == 'DIESEL')):
        return (((1/(1+math.exp(0.16*(idade-19.1))))+(1/(1+math.exp(0.16*(idade+19.1)))))*df['Quantidade'])

    elif(df['Tipo'] in ['MOTOCICLETA', 'CICLOMOTOR', 'TRICICLO', 'QUADRICICLO', 'MOTONETA']):
        #Ajustar
        return (math.exp(-0.085*idade)*df['Quantidade'])

    return np.nan

def vkt_fase1 (ano, versao):
    df_rms = pd.read_csv('datasets/rms_rev02.csv')
    df_base_class_denatran = pd.read_csv('datasets/base_denatran_classificacao.csv')

    #consumo = df_base_consumo[(df_base_consumo['Tipo'] == 'CAMINHAO') & (df_base_consumo['Ano'] == 2012) & (df_base_consumo['Combustivel'].str.contains('DIESEL'))]
    #print(consumo)

    #print('datasets/{}/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Dezembro_{}.txt'.format(ano, ano))

    df_denatran = pd.read_csv('datasets/{}/I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Dezembro_{}.txt'.format(ano, ano), sep=';')
    print(df_denatran)
    df_denatran.rename(columns={'Município': 'Municipio', 'Marca Modelo': 'Marca_Modelo', 'Ano Fabricação Veículo CRV': 'Ano', 'Qtd. Veículos': 'Quantidade'}, inplace = True)

    df_denatran = df_denatran[df_denatran[['UF', 'Municipio']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
    df_denatran = pd.merge(df_denatran, df_rms[['Municipio', 'UF', 'RM', 'Capital']], on=['Municipio', 'UF'], how='left')

    #df_denatran_sem_ano = df_denatran[~df_denatran['Ano'].map(lambda x: x.isnumeric())]
    #print(df_denatran)
    df_denatran = df_denatran[df_denatran['Ano'].map(lambda x: x.isnumeric())]
    df_denatran['Ano'] = df_denatran['Ano'].astype(np.int64)
    df_denatran['Marca_Modelo'] = df_denatran['Marca_Modelo'].convert_dtypes()
    df_denatran['Marca_Modelo'] = df_denatran['Marca_Modelo'].astype(str)

    #df_base_class_denatran = df_base_class_denatran[df_base_class_denatran['Ano'].map(lambda x: x.isnumeric())]
    df_base_class_denatran['Ano'] = df_base_class_denatran['Ano'].astype(np.int64)
    df_base_class_denatran['Marca_Modelo'] = df_base_class_denatran['Marca_Modelo'].convert_dtypes()
    df_base_class_denatran['Marca_Modelo'] = df_base_class_denatran['Marca_Modelo'].astype(str)
    df_base_class_denatran = df_base_class_denatran.drop_duplicates(subset=['Marca_Modelo', 'Ano'])

    df_denatran = pd.merge(df_denatran, df_base_class_denatran[['Marca_Modelo', 'Ano', 'Tipo', 'Combustivel']], on=['Marca_Modelo', 'Ano'], how='left')
    df_denatran['Tipo'] = df_denatran['Tipo'].astype(str)

    #Excluir antes?

    tipos_exc = ['BICICLETA', 	'BONDE', 	'CARRO DE MAO', 	'CARROCA', 	'CHARRETE', 	'CHASSI/PLATAFORMA', 	'MOTOR-CASA', 	'Não Identificado', 	'REBOQUE', 	'SEMI-REBOQUE', 	'SIDE-CAR', 	'Sem Informação', 	'TRATOR DE ESTEIRAS', 	'TRATOR DE RODAS', 	'TRATOR MISTO']
    #df_denatran_tipos_exc = df_denatran[df_denatran['Tipo'].isin(tipos_exc)]
    df_denatran = df_denatran[~df_denatran['Tipo'].isin(tipos_exc)]

    df_denatran.reset_index(drop=True, inplace=True)
    df_denatran[['Marca','Modelo']] = df_denatran['Marca_Modelo'].str.split('/', n=1, expand=True)
    marcas_exc = ['SR', 'REB', 'R', 'MO', 'M.A.', 'MA', 'MR', 'M.AGRICOLA', 'SE', 'CASE', 'SRM', 'REBOQUE', 'F.PROPRIA']
    df_denatran = df_denatran[~df_denatran['Marca'].isin(marcas_exc)]
    #df_denatran_marca = df_denatran.groupby(['Marca']).sum().sort_values(by=['Quantidade'], ascending=False)
    df_denatran[['Modelo_A','Modelo_B','Modelo_C']] = df_denatran['Modelo'].str.split(' ', n=2, expand=True)
    #df_denatran_null = df_denatran[df_denatran['Modelo_A'].isnull()]
    df_denatran = df_denatran[df_denatran['Modelo_A'].notnull()]

    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)
    return

def vkt_fase2 (ano, versao):
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)

    tipos = ['AUTOMOVEL', 'CAMINHONETE', 'CAMIONETA', 'UTILITARIO']

    df_denatran_modelos_a = df_denatran[df_denatran['Tipo'].isin(tipos)]
    df_denatran_modelos_a = df_denatran_modelos_a.groupby(['Modelo_A', 'Tipo'])['Quantidade'].sum().sort_values(ascending=False)
    df_denatran_modelos_b = df_denatran[df_denatran['Tipo'].isin(tipos)]
    df_denatran_modelos_b = df_denatran_modelos_b.groupby(['Modelo_B', 'Tipo'])['Quantidade'].sum().sort_values(ascending=False)
    df_denatran_modelos_c = df_denatran[df_denatran['Tipo'].isin(tipos)]
    df_denatran_modelos_c = df_denatran_modelos_c.groupby(['Modelo_C', 'Tipo'])['Quantidade'].sum().sort_values(ascending=False)
    df_denatran_modelos_a = df_denatran_modelos_a[df_denatran_modelos_a > np.percentile(df_denatran_modelos_a,95)]
    df_denatran_modelos_b = df_denatran_modelos_b[df_denatran_modelos_b > np.percentile(df_denatran_modelos_b,95)]
    df_denatran_modelos_c = df_denatran_modelos_c[df_denatran_modelos_c > np.percentile(df_denatran_modelos_c,95)]

    df_denatran_modelos_a = df_denatran_modelos_a.reset_index()
    df_denatran_modelos_b = df_denatran_modelos_b.reset_index()
    df_denatran_modelos_c = df_denatran_modelos_c.reset_index()

    df_denatran_modelos_a['Modelo_iCarros_A'] = df_denatran_modelos_a['Modelo_A'].map(lambda x: get_close_model(x))
    df_denatran_modelos_b['Modelo_iCarros_B'] = df_denatran_modelos_b['Modelo_B'].map(lambda x: get_close_model(x))
    df_denatran_modelos_c['Modelo_iCarros_C'] = df_denatran_modelos_c['Modelo_C'].map(lambda x: get_close_model(x))
    
    df_denatran = pd.merge(df_denatran, df_denatran_modelos_a[['Modelo_A', 'Modelo_iCarros_A']], on='Modelo_A', how='left')
    df_denatran = pd.merge(df_denatran, df_denatran_modelos_b[['Modelo_B', 'Modelo_iCarros_B']], on='Modelo_B', how='left')
    df_denatran = pd.merge(df_denatran, df_denatran_modelos_c[['Modelo_C', 'Modelo_iCarros_C']], on='Modelo_C', how='left')

    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)
    return

def vkt_fase3 (ano, versao):
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)

    df_marca_modelo5 = pd.read_csv('datasets/marca_modelo_lista5_priority.csv')
    df_marca_modelo5.rename(columns={'Modelo': 'Modelo_A'}, inplace = True)
    df_marca_modelo5['Ano'] = df_marca_modelo5['Ano'].astype(np.int64)
    df_marca_modelo5[['Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']] = df_marca_modelo5[['Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    df_marca_modelo5['Combustivel_Gasolina'] = df_marca_modelo5['Combustivel_Gasolina'].apply(unidecode)
    df_marca_modelo5['Combustivel_Alcool'] = df_marca_modelo5['Combustivel_Alcool'].apply(unidecode)

    df_denatran = df_denatran.rename(columns={'Modelo_iCarros_A': 'Modelo_iCarros_A_t', 'Modelo_iCarros_B': 'Modelo_iCarros_B_t', 'Modelo_iCarros_C': 'Modelo_iCarros_C_t'})
    df_denatran['Modelo_iCarros_A'] = df_denatran['Modelo_iCarros_A_t'].where(df_denatran['Modelo_iCarros_A_t'].isnull(), df_denatran['Modelo_A'])
    df_denatran['Modelo_iCarros_B'] = df_denatran['Modelo_iCarros_B_t'].where(df_denatran['Modelo_iCarros_B_t'].isnull(), df_denatran['Modelo_B'])
    df_denatran['Modelo_iCarros_C'] = df_denatran['Modelo_iCarros_C_t'].where(df_denatran['Modelo_iCarros_C_t'].isnull(), df_denatran['Modelo_C'])
    df_denatran = df_denatran.drop(['Modelo_iCarros_A_t','Modelo_iCarros_B_t','Modelo_iCarros_C_t'], axis=1)

    df_marca_modelo5 = df_marca_modelo5.rename(columns={'Modelo_A': 'Modelo_iCarros_A'})
    df_denatran = pd.merge(df_denatran, df_marca_modelo5[['Modelo_iCarros_A', 'Ano', 'Combustivel_Gasolina', 'Combustivel_Alcool', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']], on=['Modelo_iCarros_A', 'Ano'], how='left')
    df_marca_modelo5 = df_marca_modelo5.rename(columns={'Modelo_iCarros_A': 'Modelo_iCarros_B'})
    df_denatran = pd.merge(df_denatran, df_marca_modelo5[['Modelo_iCarros_B', 'Ano', 'Combustivel_Gasolina', 'Combustivel_Alcool', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']], on=['Modelo_iCarros_B', 'Ano'], how='left', suffixes=['_A', None])
    df_marca_modelo5 = df_marca_modelo5.rename(columns={'Modelo_iCarros_B': 'Modelo_iCarros_C'})
    df_denatran = pd.merge(df_denatran, df_marca_modelo5[['Modelo_iCarros_C', 'Ano', 'Combustivel_Gasolina', 'Combustivel_Alcool', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']], on=['Modelo_iCarros_C', 'Ano'], how='left', suffixes=['_B', '_C'])

    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)
    return

def vkt_fase4 (ano, versao):
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)
    df_base_conv_comb = pd.read_csv('datasets/base_conv_comb_v1.csv')
    df_base_conv_comb.rename(columns={'Comb_Ant': 'Combustivel'}, inplace = True)

    df_denatran['Combustivel'] = df_denatran['Combustivel'].convert_dtypes()
    df_base_conv_comb['Combustivel'] = df_base_conv_comb['Combustivel'].convert_dtypes()
    df_base_conv_comb['Comb_Novo'] = df_base_conv_comb['Comb_Novo'].convert_dtypes()

    df_denatran = pd.merge(df_denatran, df_base_conv_comb[['Combustivel', 'Comb_Novo']], on='Combustivel', how='left')
    df_denatran.rename(columns={'Combustivel': 'Comb_Ant', 'Comb_Novo': 'Combustivel'}, inplace = True)
    df_denatran['Combustivel'] = df_denatran['Combustivel'].astype(str)

    comb_exc = ['GNV', 'ELETRICO', 'GAS METANO', 'GASOGENIO', 'Não Identificado', 'Sem Informação', 'VIDE/CAMPO/OBSERVACAO']
    #df_denatran_comb_exc = df_denatran[df_denatran['Combustivel'].isin(comb_exc)]
    df_denatran = df_denatran[~df_denatran['Combustivel'].isin(comb_exc)]

    df_denatran[['Consumo_Gasolina', 'Consumo_Alcool', 'Consumo_Diesel']] = df_denatran[['Consumo_Cidade_Gasolina_A', 'Combustivel_Gasolina_A', 'Consumo_Cidade_Gasolina_B', 'Combustivel_Gasolina_B', 'Consumo_Cidade_Gasolina_C', 'Combustivel_Gasolina_C', 'Consumo_Cidade_Alcool_A', 'Combustivel_Alcool_A', 'Consumo_Cidade_Alcool_B', 'Combustivel_Alcool_B', 'Consumo_Cidade_Alcool_C', 'Combustivel_Alcool_C', 'Combustivel', 'Comb_Ant']].apply(lambda x: get_comb(x), axis=1, result_type='expand')

    df_denatran = df_denatran.drop(['Marca', 'Modelo', 'Modelo_A', 'Modelo_B', 'Modelo_C', 'Modelo_iCarros_A', 'Modelo_iCarros_B', 'Modelo_iCarros_C', 'Consumo_Cidade_Gasolina_A', 'Combustivel_Gasolina_A', 'Consumo_Cidade_Gasolina_B', 'Combustivel_Gasolina_B', 'Consumo_Cidade_Gasolina_C', 'Combustivel_Gasolina_C', 'Consumo_Cidade_Alcool_A', 'Combustivel_Alcool_A', 'Consumo_Cidade_Alcool_B', 'Combustivel_Alcool_B', 'Consumo_Cidade_Alcool_C', 'Combustivel_Alcool_C', 'Comb_Ant'], axis=1)

    df_denatran['Tipo'] = df_denatran['Tipo'].convert_dtypes()
    df_denatran['RM'] = df_denatran['RM'].convert_dtypes()

    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)
    return

def vkt_fase5 (ano, versao):
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)

    #df_denatran['Consumo_Gasolina'] = df_denatran['Consumo_Gasolina'].fillna(df_denatran.groupby(['RM', 'Tipo'])[['Consumo_Gasolina', 'Quantidade']].apply(lambda x: np.average(x['Consumo_Gasolina'], weights=x['Quantidade'])))
    #df_denatran['Consumo_Gasolina'] = df_denatran['Consumo_Gasolina'].fillna(df_denatran.groupby(['RM', 'Tipo'])[['Consumo_Gasolina', 'Quantidade']].transform(lambda x: np.average(x['Consumo_Gasolina'], weights=x['Quantidade'])))
    '''df_test = df_denatran.groupby(by=['RM', 'Tipo'], group_keys=False)[['Consumo_Gasolina', 'Quantidade']]
    print(df_test)
    print(df_test.value)
    print(df_test.weight)
    #df_denatran['Consumo_Gasolina'] = df_denatran.groupby(by=['RM', 'Tipo'], group_keys=False)[['Consumo_Gasolina', 'Quantidade']].apply(lambda x: x['Consumo_Gasolina'].fillna(np.average(x['Consumo_Gasolina'], weights=x['Quantidade'])))
    df_denatran['Consumo_Gasolina'] = df_denatran.groupby(by=['RM', 'Tipo'], group_keys=False)[['Consumo_Gasolina', 'Quantidade']].apply(fill_comb_gasolina)
    #df_denatran['Consumo_Gasolina'] = df_denatran.groupby(by=['RM', 'Tipo']).pipe(lambda grp: grp.fillna(np.average(grp['Consumo_Gasolina'], weights=grp['Quantidade'])))
    df_denatran['Consumo_Alcool'] = df_denatran['Consumo_Alcool'].fillna(df_denatran.groupby(['RM', 'Tipo'])[['Consumo_Alcool', 'Quantidade']].apply(lambda x: np.average(x['Consumo_Alcool'], weights=x['Quantidade'])))
    df_denatran['Consumo_Diesel'] = df_denatran['Consumo_Diesel'].fillna(df_denatran.groupby(['RM', 'Tipo'])[['Consumo_Diesel', 'Quantidade']].apply(lambda x: np.average(x['Consumo_Diesel'], weights=x['Quantidade'])))'''
    #Média Ponderada não funcionou
    df_denatran['Combustivel'] = df_denatran['Combustivel'].convert_dtypes()
    df_denatran['Combustivel'] = df_denatran['Combustivel'].astype(str)

    #print(df_denatran.dtypes)

    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran.groupby(['Combustivel', 'RM', 'Tipo', 'Ano'])['Consumo_Gasolina'].transform('mean'))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran.groupby(['Combustivel', 'RM', 'Tipo', 'Ano'])['Consumo_Alcool'].transform('mean'))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran.groupby(['Combustivel', 'RM', 'Tipo', 'Ano'])['Consumo_Diesel'].transform('mean'))

    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran.groupby(['Combustivel', 'Tipo', 'Ano'])['Consumo_Gasolina'].transform('mean'))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran.groupby(['Combustivel', 'Tipo', 'Ano'])['Consumo_Alcool'].transform('mean'))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran.groupby(['Combustivel', 'Tipo', 'Ano'])['Consumo_Diesel'].transform('mean'))

    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran.groupby(['Combustivel', 'Tipo'])['Consumo_Gasolina'].transform('mean'))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran.groupby(['Combustivel', 'Tipo'])['Consumo_Alcool'].transform('mean'))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran.groupby(['Combustivel', 'Tipo'])['Consumo_Diesel'].transform('mean'))

    #print(df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')])
    #print(df_denatran[df_denatran['Combustivel'].isna()][['Combustivel', 'Tipo', 'Ano']])
    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran[['Combustivel', 'Tipo', 'Ano']].apply(lambda x: get_consumo('GASOLINA', x), axis=1))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran[['Combustivel', 'Tipo', 'Ano']].apply(lambda x: get_consumo('ALCOOL', x), axis=1))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran[['Combustivel', 'Tipo', 'Ano']].apply(lambda x: get_consumo('DIESEL', x), axis=1))

    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran.groupby(['Combustivel', 'RM', 'Tipo', 'Ano'])['Consumo_Gasolina'].transform('mean'))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran.groupby(['Combustivel', 'RM', 'Tipo', 'Ano'])['Consumo_Alcool'].transform('mean'))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran.groupby(['Combustivel', 'RM', 'Tipo', 'Ano'])['Consumo_Diesel'].transform('mean'))

    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran.groupby(['Combustivel', 'Tipo', 'Ano'])['Consumo_Gasolina'].transform('mean'))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran.groupby(['Combustivel', 'Tipo', 'Ano'])['Consumo_Alcool'].transform('mean'))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran.groupby(['Combustivel', 'Tipo', 'Ano'])['Consumo_Diesel'].transform('mean'))

    df_denatran['Consumo_Gasolina'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'GASOLINA')]['Consumo_Gasolina'].fillna(df_denatran.groupby(['Combustivel', 'Tipo'])['Consumo_Gasolina'].transform('mean'))
    df_denatran['Consumo_Alcool'] = df_denatran[(df_denatran['Combustivel'] == 'FLEX') | (df_denatran['Combustivel'] == 'ALCOOL')]['Consumo_Alcool'].fillna(df_denatran.groupby(['Combustivel', 'Tipo'])['Consumo_Alcool'].transform('mean'))
    df_denatran['Consumo_Diesel'] = df_denatran[(df_denatran['Combustivel'] == 'DIESEL')]['Consumo_Diesel'].fillna(df_denatran.groupby(['Combustivel', 'Tipo'])['Consumo_Diesel'].transform('mean'))

    #df_denatran_comb_media = df_denatran.groupby([['RM', 'Tipo']])[['Consumo_Gasolina', 'Consumo_Alcool', 'Consumo_Diesel']].mean()
    #df_denatran_comb_media = df_denatran_comb_media.reset_index()

    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)
    return

def vkt_fase6 (ano, versao):
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)
    df_denatran['VKT_Preliminar'] = df_denatran[['Ano', 'Combustivel', 'Tipo']].apply(lambda x: get_vkt_preliminar(x, ano), axis=1)
    #df_denatran_vkt_erro = df_denatran[df_denatran['VKT_Preliminar'].map(lambda x: np.isnan(x))]
    df_denatran = df_denatran[~df_denatran['VKT_Preliminar'].map(lambda x: np.isnan(x))]
    df_denatran['Quantidade'] = df_denatran[['Ano', 'Tipo', 'Combustivel', 'Quantidade']].apply(lambda x: get_sucat(x, ano), axis=1)
    df_denatran['VKT_Preliminar'] = df_denatran['VKT_Preliminar']*df_denatran['Quantidade']
    df_denatran_vkt_neg = df_denatran[df_denatran['VKT_Preliminar'] <= 0]

    #df_denatran['Desempenho_Flex'] = df_denatran[df_denatran['Combustivel'] == 'FLEX'][['Consumo_Gasolina', 'Consumo_Alcool']].apply(lambda x: x['Consumo_Alcool']/x['Consumo_Gasolina'], axis=1)
    df_preco_comb_rm_anual = df_preco_comb_rm[df_preco_comb_rm['Ano'] == ano]
    
    df_denatran = pd.merge(df_denatran, df_preco_comb_rm_anual[['RM', 'Relacao']], on='RM', how='left')
    #df_denatran[df_denatran['Combustivel'] != 'FLEX']['Relacao'] = np.nan
    df_denatran.loc[df_denatran['Combustivel'] != 'FLEX', 'Relacao'] = np.nan
    #data.loc[data['name'] == 'fred', 'A'] = 0
    #df_denatran['Relacao'] = df_denatran[df_denatran['Combustivel'] != 'FLEX'].apply(np.nan)

    #df_denatran['Relacao'] = ''
    #df_denatran[((df_denatran['Relacao'] == '') & (df_denatran['Combustivel'] == 'FLEX'))]['Relacao'] = np.NaN
    #df_denatran['Relacao'] = df_denatran[df_denatran['Combustivel'] == 'FLEX'][['RM', 'VKT_Preliminar', 'Consumo_Gasolina', 'Consumo_Alcool']].apply()
    #df_denatran = pd.merge(df_denatran, df_preco_comb_rm[['RM', 'Relacao']], on=['RM'], how='left')

    df_denatran['Volume_Gasolina'] = df_denatran[df_denatran['Combustivel'] == 'GASOLINA'][['VKT_Preliminar', 'Consumo_Gasolina']].apply(lambda x: x['VKT_Preliminar']/x['Consumo_Gasolina'], axis=1)
    df_denatran['Volume_Gasolina'] = df_denatran[df_denatran['Combustivel'] == 'FLEX'][['VKT_Preliminar', 'Consumo_Gasolina', 'Relacao']].apply(lambda x: (x['VKT_Preliminar']*(1-x['Relacao']))/x['Consumo_Gasolina'], axis=1)
    df_denatran['Volume_Alcool'] = df_denatran[df_denatran['Combustivel'] == 'ALCOOL'][['VKT_Preliminar', 'Consumo_Alcool']].apply(lambda x: x['VKT_Preliminar']/x['Consumo_Alcool'], axis=1)
    df_denatran['Volume_Alcool'] = df_denatran[df_denatran['Combustivel'] == 'FLEX'][['VKT_Preliminar', 'Consumo_Alcool', 'Relacao']].apply(lambda x: (x['VKT_Preliminar']*x['Relacao'])/x['Consumo_Alcool'], axis=1)
    #df_denatran[['Volume_Gasolina', 'Volume_Alcool']] = df_denatran[df_denatran['Combustivel'] == 'FLEX'][['RM', 'VKT_Preliminar', 'Consumo_Gasolina', 'Consumo_Alcool']].apply(lambda x: get_flex(x), axis=1)
    df_denatran['Volume_Diesel'] = df_denatran[df_denatran['Combustivel'] == 'DIESEL'][['VKT_Preliminar', 'Consumo_Diesel']].apply(lambda x: x['VKT_Preliminar']/x['Consumo_Diesel'], axis=1)
    #print(df_denatran)

    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)

    #df_denatran_rm = df_denatran.groupby(['RM'])['VKT_Preliminar'].sum()
    #df_denatran_rm.to_csv('datasets/{}/vkt_v2_rm.csv'.format(ano))
    return

def vkt_fase7 (ano, versao):
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)
    df_denatran_rm = df_denatran.groupby(['RM'])[['Volume_Alcool', 'Volume_Gasolina', 'Volume_Diesel']].sum()
    df_denatran_rm = df_denatran_rm.reset_index()

    #print(df_base_volume_comb_rm)
    df_base_volume_comb_rm_anual = df_base_volume_comb_rm[df_base_volume_comb_rm['Ano'] == ano]
    #print(df_base_volume_comb_rm_anual)
    df_base_volume_comb_rm_anual = df_base_volume_comb_rm_anual.drop(['Ano'], axis=1)
    #print(df_base_volume_comb_rm_anual)

    df_base_volume_comb_rm_anual = df_base_volume_comb_rm_anual.pivot(index='RM', columns='Combustivel', values='Quantidade')
    df_base_volume_comb_rm_anual = pd.merge(df_base_volume_comb_rm_anual, df_base_diesel_rm, on='RM', how='left')

    #print(df_base_volume_comb_rm_anual)
    df_base_volume_comb_rm_anual[df_base_volume_comb_rm_anual['Volume_Venda_Diesel'].map(lambda x: np.isnan(x))]['Fator'] = np.nan
    #print(df_base_volume_comb_rm_anual)

    df_denatran_rm = pd.merge(df_denatran_rm, df_base_volume_comb_rm_anual, on='RM', how='left')
    #df_denatran = pd.merge(df_denatran, df_rms[['Municipio', 'UF', 'RM', 'Capital']], on=['Municipio', 'UF'], how='left')

    df_denatran_rm['Fator_Alcool'] = df_denatran_rm['Volume_Venda_Alcool']/df_denatran_rm['Volume_Alcool']
    df_denatran_rm['Fator_Gasolina'] = df_denatran_rm['Volume_Venda_Gasolina']/df_denatran_rm['Volume_Gasolina']
    df_denatran_rm['Fator_Diesel'] = (df_denatran_rm['Volume_Venda_Diesel']*df_denatran_rm['Fator_Ajuste_Diesel'])/df_denatran_rm['Volume_Diesel']

    df_denatran_rm = df_denatran_rm.drop(['Volume_Alcool', 'Volume_Gasolina', 'Volume_Diesel'], axis=1)
    #print(df_denatran_rm)

    df_denatran = pd.merge(df_denatran, df_denatran_rm, on='RM', how='left')

    df_denatran['VKT'] = df_denatran[['VKT_Preliminar', 'Combustivel', 'Fator_Alcool', 'Fator_Gasolina', 'Fator_Diesel', 'Relacao']].apply(lambda x: get_vkt(x), axis=1)

    #df_denatran = df_denatran.drop(['Quantidade', 'Volume_Alcool', 'Volume_Gasolina', 'Volume_Diesel'], axis=1)
    
    df_denatran.to_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), index=False)

    df_denatran_rm = df_denatran.groupby(['RM'])['VKT'].sum()
    df_denatran_rm.to_csv('datasets/{}/vkt_v{}_rm.csv'.format(ano, versao))
    return

df_marca_modelo5 = pd.read_csv('datasets/marca_modelo_lista5_priority.csv')
df_marca_modelo5.rename(columns={'Modelo': 'Modelo_A'}, inplace = True)
df_marca_modelo5['Ano'] = df_marca_modelo5['Ano'].astype(np.int64)
df_marca_modelo5[['Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']] = df_marca_modelo5[['Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool']].apply(lambda x: pd.to_numeric(x, errors='coerce'))
df_marca_modelo5['Combustivel_Gasolina'] = df_marca_modelo5['Combustivel_Gasolina'].apply(unidecode)
df_marca_modelo5['Combustivel_Alcool'] = df_marca_modelo5['Combustivel_Alcool'].apply(unidecode)

df_base_consumo = pd.read_csv('datasets/base_consumo.csv')
df_base_consumo = df_base_consumo[df_base_consumo['Consumo'] != 'nd']
df_base_consumo['Consumo'] = df_base_consumo['Consumo'].astype(np.float64)

df_preco_comb_rm = pd.read_csv('datasets/base_combustiveis_precos_rel_rm.csv')

df_base_volume_comb_rm = pd.read_csv('datasets/base_volume_comb_rm.csv')
df_base_diesel_rm = pd.read_csv('datasets/base_diesel_rm.csv')

versao = 4
for ano in range(2019, 2020, 1):
    print(f"Iniciando {ano}...")
    vkt_fase1(ano, versao)
    print('Fase 1 concluída')
    vkt_fase2(ano, versao)
    print('Fase 2 concluída')
    vkt_fase3(ano, versao)
    print('Fase 3 concluída')
    vkt_fase4(ano, versao)
    print('Fase 4 concluída')
    vkt_fase5(ano, versao)
    print('Fase 5 concluída')
    vkt_fase6(ano, versao)
    print('Fase 6 concluída')
    vkt_fase7(ano, versao)
    print('Fase 7 concluída')
    df_denatran = pd.read_csv('datasets/{}/vkt_v{}.csv'.format(ano, versao), low_memory=False)
    print(df_denatran)
