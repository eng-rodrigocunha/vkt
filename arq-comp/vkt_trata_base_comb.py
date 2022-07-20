import pandas as pd

'''df = pd.concat(pd.read_excel('datasets/base_combustiveis_precos.xlsx', sheet_name=None), ignore_index=True)

print(df)

df.to_csv('datasets/base_combustiveis_precos.csv', index=False)'''

'''df_comb_2013_1 = pd.read_csv('datasets/ca-2013-01.csv', sep=';')
df_comb_2013_2 = pd.read_csv('datasets/ca-2013-02.csv', sep=';')
print(df_comb_rm)

df_comb_rm = pd.concat([df_comb_2013_1, df_comb_2013_2, df_comb_rm])
print(df_comb_rm)

df_comb_rm.to_csv('datasets/base_combustiveis_precos.csv', index=False)'''

'''df_comb_rm.rename(columns={'Estado - Sigla': 'UF', 'Valor de Venda': 'Valor_Venda', 'Data da Coleta': 'Data'}, inplace = True)
print(df_comb_rm)

df_rms = pd.read_csv('datasets/rms_uf_resumida_rev02.csv')

df_comb_rm = df_comb_rm[df_comb_rm[['UF', 'Municipio']].apply(tuple, axis=1).isin(df_rms[['UF','Municipio']].apply(tuple, axis=1))]
df_comb_rm = pd.merge(df_comb_rm, df_rms[['Municipio', 'UF', 'RM']], on=['Municipio', 'UF'], how='left')
print(df_comb_rm)
print(df_comb_rm.dtypes)

df_comb_rm['Data'] = pd.to_datetime(df_comb_rm['Data'])
print(df_comb_rm)
print(df_comb_rm.dtypes)

df_comb_rm['Valor_Venda'] = df_comb_rm['Valor_Venda'].apply(lambda x: x.replace(',', '.'))
print(df_comb_rm)
print(df_comb_rm.dtypes)

df_comb_rm['Valor_Venda'] = pd.to_numeric(df_comb_rm['Valor_Venda'])
print(df_comb_rm)
print(df_comb_rm.dtypes)

df_comb_rm['Ano'] = pd.DatetimeIndex(df_comb_rm['Data']).year
print(df_comb_rm)
print(df_comb_rm.dtypes)

df_comb_rm_g = df_comb_rm.groupby(['RM', 'Ano', 'Produto',])['Valor_Venda'].mean()
#df_comb_rm_g = df_comb_rm_g.reset_index()

print(df_comb_rm_g)
print(df_comb_rm_g.dtypes)

df_comb_rm_g.to_csv('datasets/base_combustiveis_precos_rm.csv')'''

df_comb_rm = pd.read_csv('datasets/base_combustiveis_precos_rm.csv')
#df_comb_rm['Produto'] = df_comb_rm['Produto'].apply(lambda x: x.replace('ETANOL'
