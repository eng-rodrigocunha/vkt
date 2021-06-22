import pandas as pd

marcas_modelos3 = pd.read_csv('datasets/marca_modelo_lista3_priority.csv')
marcas_modelos4 = pd.read_csv('datasets/marca_modelo_lista4_priority.csv')

marcas_modelos5 = pd.concat([marcas_modelos3, marcas_modelos4])
marcas_modelos5 = marcas_modelos5.sort_values(['Consumo_Cidade_Gasolina'], ascending=False)
marcas_modelos5.drop_duplicates(subset=['Chave_B'], inplace=True)

marcas_modelos5 = marcas_modelos5[marcas_modelos5['Consumo_Cidade_Gasolina'].notnull()]
marcas_modelos5 = marcas_modelos5.query("Consumo_Cidade_Gasolina != 'N/D' | Consumo_Cidade_Alcool != 'N/D'")
marcas_modelos5.reset_index(drop=True, inplace=True)
print(marcas_modelos5)

marcas_modelos5.to_csv('datasets/marca_modelo_lista5_priority.csv', index=False)