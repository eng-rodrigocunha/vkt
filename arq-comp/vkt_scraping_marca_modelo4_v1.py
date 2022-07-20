from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time
import random

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--incognito")
options.headless = True
driver = webdriver.Chrome(executable_path='C:\\WebDriver\\bin\\chromedriver.exe', options=options)

marcas_modelos3 = pd.read_csv('datasets/marca_modelo_lista3_priority.csv')
marcas_modelos3 = marcas_modelos3.sort_values(['Consumo_Cidade_Gasolina'], ascending=False)
#marcas_modelos4 = marcas_modelos4.query("Consumo_Cidade_Gasolina == ''")
marcas_modelos3.drop_duplicates(subset=['Chave_A'], inplace=True)

marcas_modelos4 = pd.read_csv('datasets/marca_modelo_lista4_priority.csv')
m4_chaveA_lista = list(set(marcas_modelos4['Chave_A'].tolist()))

df_exc = pd.read_csv('datasets/marca_modelo_lista2_exc_priority.csv')
df_exc.drop_duplicates(subset=['Chave_A'], inplace=True)
exc_chaveA_lista = df_exc['Chave_A'].tolist()

#df_exc2 = pd.read_csv('datasets/marca_modelo_lista4_exc_priority.csv')
#df_exc2.drop_duplicates(subset=['Chave_B'], inplace=True)
#exc_chaveB_lista = df_exc2['Chave_B'].tolist()

df_priority = pd.read_csv('datasets/priority_v3.csv')
#df_priority['Chave_A'] = df_priority.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)
df_priority.drop_duplicates(subset=['Chave_A'], inplace=True)
priority_chaveA_lista = df_priority['Chave_A'].tolist()

#df_erro = pd.read_csv('datasets/marca_modelo_lista4_erro_priority.csv')

print(marcas_modelos3)
marcas_modelos3 = marcas_modelos3[~marcas_modelos3['Consumo_Cidade_Gasolina'].notnull()]
marcas_modelos3 = marcas_modelos3[~marcas_modelos3['Chave_A'].isin(exc_chaveA_lista)]
marcas_modelos3 = marcas_modelos3[~marcas_modelos3['Chave_A'].isin(m4_chaveA_lista)]
#marcas_modelos3 = marcas_modelos3[~marcas_modelos3['Chave_B'].isin(exc_chaveB_lista)]
marcas_modelos3 = marcas_modelos3[marcas_modelos3['Chave_A'].isin(priority_chaveA_lista)]
marcas_modelos3.reset_index(drop=True, inplace=True)
print(marcas_modelos3)

marca_modelo_lista = []
cadastro_excecao = []
erro = []
chave_temp = ''

for index, row in marcas_modelos3.iterrows():
    #Scraping de Modelos do Veículo
    try:
        if(index > 110):
            break

        print('Faltam ' + str(len(marcas_modelos3)-index))

        time.sleep(random.randint(0,3))

        print('https://www.icarros.com.br/catalogo/fichatecnica.jsp?modelo={}&anomodelo={}&versao={}'.format(row['Modelo_Cod'], row['Ano'], row['Versao_Cod']))
        driver.get('https://www.icarros.com.br/catalogo/fichatecnica.jsp?modelo={}&anomodelo={}&versao={}'.format(row['Modelo_Cod'], row['Ano'], row['Versao_Cod']))

        print('{} {} {} {}'.format(row['Marca'], row['Modelo'], row['Versao'], row['Ano']))
        chave_temp = row['Chave_B']
        
        comb_g = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[2]/td[2]')))
        comb_a = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[2]/td[3]')))
        cons_c_g = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[7]/td[2]')))
        cons_c_a = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[7]/td[3]')))
        cons_e_g = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[8]/td[2]')))
        cons_e_a = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[8]/td[3]')))
        marca_modelo_lista.append([row['Marca_Cod'], row['Marca'], row['Modelo_Cod'], row['Modelo'], row['Ano'], row['Versao'], row['Versao_Cod'], comb_g.text, comb_a.text, cons_c_g.text.replace(',','.'), cons_c_a.text.replace(',','.'), cons_e_g.text.replace(',','.'), cons_e_a.text.replace(',','.')])

    except Exception as e:
        if (chave_temp == row['Chave_B']):
            print('Erro de scraping')
            erro.append([row['Marca_Cod'], row['Modelo_Cod'], row['Versao_Cod'], row['Ano']])
        else:
            print('Erro de carregamento, insere na lista de exceções')
            print(str(e))        
            cadastro_excecao.append([row['Marca_Cod'], row['Modelo_Cod'], row['Versao_Cod'], row['Ano']])
        continue

driver.close()
marcas_modelos4 = marcas_modelos4.append(pd.DataFrame(marca_modelo_lista, columns=['Marca_Cod', 'Marca', 'Modelo_Cod', 'Modelo', 'Ano', 'Versao', 'Versao_Cod', 'Combustivel_Gasolina', 'Combustivel_Alcool', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool', 'Consumo_Estrada_Gasolina', 'Consumo_Estrada_Alcool']))
marcas_modelos4['Chave_A'] = marcas_modelos4.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)
marcas_modelos4['Chave_B'] = marcas_modelos4.apply(lambda x: '{}-{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Versao_Cod'], x['Ano']), axis=1)

#df_exc2 = df_exc2.append(pd.DataFrame(cadastro_excecao, columns=['Marca_Cod', 'Modelo_Cod', 'Versao_Cod', 'Ano']))
df_exc2 = pd.DataFrame(cadastro_excecao, columns=['Marca_Cod', 'Modelo_Cod', 'Versao_Cod', 'Ano'])
#df_exc2['Chave_A'] = df_exc2.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)
#df_exc2['Chave_B'] = df_exc2.apply(lambda x: '{}-{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Versao_Cod'], x['Ano']), axis=1)

#df_erro = df_erro.append(pd.DataFrame(erro, columns=['Marca_Cod', 'Modelo_Cod', 'Versao_Cod', 'Ano']))
df_erro = pd.DataFrame(erro, columns=['Marca_Cod', 'Modelo_Cod', 'Versao_Cod', 'Ano'])
#df_erro['Chave_A'] = df_erro.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)
#df_erro['Chave_B'] = df_erro.apply(lambda x: '{}-{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Versao_Cod'], x['Ano']), axis=1)

df_erro.to_csv('datasets/marca_modelo_lista4_erro_priority.csv', index=False)
marcas_modelos4.to_csv('datasets/marca_modelo_lista4_priority.csv', index=False)
df_exc2.to_csv('datasets/marca_modelo_lista4_exc_priority.csv', index=False)