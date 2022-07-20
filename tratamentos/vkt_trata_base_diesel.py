import pandas as pd

df_diesel_anual = pd.DataFrame()

for ano in range(2013, 2020, 1):
    if(ano in [2013, 2015]):
        df_diesel = pd.read_excel(f'datasets/diesel_2013-2019/αleo Diesel {ano}.xls', sheet_name='Rel. Ativ. Econ.', header=6)
    else:
        df_diesel = pd.read_excel(f'datasets/diesel_2013-2019/αleo Diesel {ano}.xlsx', sheet_name='Rel. Ativ. Econ.', header=6)
    
    df_diesel.rename(columns={'LOCALIDADE': 'Municipio'}, inplace = True)

    df_rms = pd.read_csv('datasets/rms_uf_resumida_rev02.csv')

    df_diesel = df_diesel[df_diesel[['UF', 'Municipio']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
    df_diesel = pd.merge(df_diesel, df_rms[['Municipio', 'UF', 'RM']], on=['Municipio', 'UF'], how='left')

    df_diesel['Volume_Real'] = df_diesel['POSTO REVENDEDOR']+df_diesel['RODOVIÁRIO']
    df_diesel['Fator'] = df_diesel['Volume_Real']/df_diesel['TOTAL']
    df_diesel['Volume_Rodoviario'] = df_diesel['Fator']*df_diesel['Volume_Real']

    df_diesel_g_fator_pesado = df_diesel.groupby(['RM'])['Volume_Rodoviario'].sum()
    df_diesel_g_fator_volume_real = df_diesel.groupby(['RM'])['Volume_Real'].sum()
    df_diesel_g_fator = df_diesel_g_fator_pesado/df_diesel_g_fator_volume_real
    df_diesel_g_fator = df_diesel_g_fator.reset_index()
    df_diesel_g_fator['Ano'] = ano
    #print(df_diesel_g_fator)

    df_diesel_anual = pd.concat([df_diesel_anual, df_diesel_g_fator])

df_diesel_anual = df_diesel_anual.rename(columns={0: 'Fator_Ajuste_Diesel'})
print(df_diesel_anual)
df_diesel_anual.to_csv('datasets/base_diesel_rm_rev02.csv', index=False)