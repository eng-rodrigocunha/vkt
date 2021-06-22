import pandas as pd

df_marcas_modelos3 = pd.read_csv('datasets/marca_modelo_lista3_priority.csv')
df_marcas_modelos4 = pd.read_csv('datasets/marca_modelo_lista4_priority.csv')

df_marcas_modelos5 = pd.concat([df_marcas_modelos3, df_marcas_modelos4])
df_marcas_modelos5 = df_marcas_modelos5.sort_values(['Consumo_Cidade_Gasolina'], ascending=False)
df_marcas_modelos5.drop_duplicates(subset=['Chave_B'], inplace=True)

df_marcas_modelos5 = df_marcas_modelos5[df_marcas_modelos5['Consumo_Cidade_Gasolina'].notnull()]
df_marcas_modelos5 = df_marcas_modelos5.query("Consumo_Cidade_Gasolina != 'N/D' | Consumo_Cidade_Alcool != 'N/D'")
df_marcas_modelos5['Modelo'] = df_marcas_modelos5['Modelo'].str.upper()
df_marcas_modelos5.reset_index(drop=True, inplace=True)
print(df_marcas_modelos5)

df_marcas_modelos5.to_csv('datasets/marca_modelo_lista5_priority.csv', index=False)