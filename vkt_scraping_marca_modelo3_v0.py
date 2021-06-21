from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--incognito")
options.headless = True
driver = webdriver.Chrome(executable_path='C:\\WebDriver\\bin\\chromedriver.exe', options=options)

marcas_modelos2 = pd.read_csv('datasets/priority_v1.csv')
marcas_modelos2['Chave_A'] = marcas_modelos2.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)
marcas_modelos2.drop_duplicates(subset=['Chave_A'], inplace=True)
print(marcas_modelos2)

marcas_modelos3 = pd.read_csv('datasets/marca_modelo_lista3_priority.csv')
#marcas_modelos3.drop_duplicates(subset=['Chave_B'], inplace=True)
#print(marcas_modelos3)
#marcas_modelos3 = marcas_modelos3.head(len(marcas_modelos3)-1)
marcas_chaveA_modelos3_lista = marcas_modelos3['Chave_A'].tolist()
marcas_chaveA_modelos3_lista = list(set(marcas_chaveA_modelos3_lista))
#print(marcas_chaveA_modelos3_lista)

df_exc = pd.read_csv('datasets/marca_modelo_lista2_exc_priority.csv')
df_exc.drop_duplicates(subset=['Chave_A'], inplace=True)
exc_chaveA_lista = df_exc['Chave_A'].tolist()
#print(exc_chaveA_lista)

marcas_modelos2 = marcas_modelos2[~marcas_modelos2['Chave_A'].isin(exc_chaveA_lista)]
marcas_modelos2 = marcas_modelos2[~marcas_modelos2['Chave_A'].isin(marcas_chaveA_modelos3_lista)]
marcas_modelos2.reset_index(drop=True, inplace=True)
#marcas_modelos3 = marcas_modelos3[~marcas_modelos3['Chave_A'].isin(exc_chaveA_lista)]
#marcas_modelos3.reset_index(drop=True, inplace=True)
print(marcas_modelos2)

marca_modelo_lista = []
cadastro_excecao = []
erro = []
chave_temp = ''

for index, row in marcas_modelos2.iterrows():
    #Scraping de Modelos do Veículo
    try:
        if(index > 5):
            break

        print('Faltam ' + str(len(marcas_modelos2)-index))

        print('https://www.icarros.com.br/catalogo/fichatecnica.jsp?modelo={}&anomodelo={}'.format(row['Modelo_Cod'], row['Ano']))
        driver.get('https://www.icarros.com.br/catalogo/fichatecnica.jsp?modelo={}&anomodelo={}'.format(row['Modelo_Cod'], row['Ano']))

        #Carregamento completo da Página
        #WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located)
        #time.sleep(5)

        #Clicando no botão alterar
        #modelos = WebDriverWait(driver, 30, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[1]/a'))).click()

        #Lendo menu de versões
        versoes = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '//*[@id="versaoForm"]/select')))
        versoes_drpd = Select(versoes)
        versoes_drpd_opts = versoes_drpd.options

        #Clicando no botão alterar
        modelos = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[1]/a'))).click()

        #print(versoes_drpd_opts)
        print('{} {} {}'.format(row['Marca'], row['Modelo'], row['Ano']))
        chave_temp = row['Chave_A']
        i = 0
        for v in versoes_drpd_opts:
            print(v.get_attribute('label'))

            #Lendo menu de anos do modelo
            anos = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltYearMenuCatalog"]')))
            comb_g = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[2]/td[2]')))
            comb_a = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[2]/td[3]')))
            cons_c_g = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[7]/td[2]')))
            cons_c_a = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[7]/td[3]')))
            cons_e_g = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[8]/td[2]')))
            cons_e_a = WebDriverWait(driver, 15, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[4]/div/table/tbody/tr[8]/td[3]')))
            if(i == 0):
                marca_modelo_lista.append([row['Marca_Cod'], row['Marca'], row['Modelo_Cod'], row['Modelo'], row['Ano'], v.get_attribute('label'), int(v.get_attribute('value')), comb_g.text, comb_a.text, cons_c_g.text.replace(',','.'), cons_c_a.text.replace(',','.'), cons_e_g.text.replace(',','.'), cons_e_a.text.replace(',','.')])

            i += 1

            anos_drpd = Select(anos)
            anos_drpd_opts = anos_drpd.options

            for a in anos_drpd_opts:
                marca_modelo_lista.append([row['Marca_Cod'], row['Marca'], row['Modelo_Cod'], row['Modelo'], int(a.get_attribute('value')), v.get_attribute('label'), int(v.get_attribute('value')), '', '', '', '', '', ''])

    except Exception as e:
        if (chave_temp == row['Chave_A']):
            print('Erro de scraping')
            erro.append([row['Marca_Cod'], row['Modelo_Cod'], row['Ano']])
        else:
            print('Erro de carregamento, insere na lista de exceções')
            print(str(e))        
            cadastro_excecao.append([row['Marca_Cod'], row['Modelo_Cod'], row['Ano']])
        continue

driver.close()
marcas_modelos3 = marcas_modelos3.append(pd.DataFrame(marca_modelo_lista, columns=['Marca_Cod', 'Marca', 'Modelo_Cod', 'Modelo', 'Ano', 'Versao', 'Versao_Cod', 'Combustivel_Gasolina', 'Combustivel_Alcool', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool', 'Consumo_Estrada_Gasolina', 'Consumo_Estrada_Alcool']))
#df_lista3 = pd.DataFrame(marca_modelo_lista, columns=['Marca_Cod', 'Marca', 'Modelo_Cod', 'Modelo', 'Ano', 'Versao', 'Versao_Cod', 'Combustivel_Gasolina', 'Combustivel_Alcool', 'Consumo_Cidade_Gasolina', 'Consumo_Cidade_Alcool', 'Consumo_Estrada_Gasolina', 'Consumo_Estrada_Alcool'])
marcas_modelos3['Chave_A'] = marcas_modelos3.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)
marcas_modelos3['Chave_B'] = marcas_modelos3.apply(lambda x: '{}-{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Versao_Cod'], x['Ano']), axis=1)
marcas_modelos3 = marcas_modelos3.query("Ano != 0")
#df_exc = df_exc.append(pd.DataFrame(cadastro_excecao, columns=['Marca_Cod', 'Modelo_Cod', 'Ano']))
df_exc = df_exc.append(pd.DataFrame(cadastro_excecao, columns=['Marca_Cod', 'Modelo_Cod', 'Ano']))
df_exc['Chave_A'] = df_exc.apply(lambda x: '{}-{}-{}'.format(x['Marca_Cod'], x['Modelo_Cod'], x['Ano']), axis=1)

# Criar csv erro
# Substituir linhas que não sejam modelo raiz e estejam preenchidas com consumo

marcas_modelos3.to_csv('datasets/marca_modelo_lista3_priority.csv', index=False)
df_exc.to_csv('datasets/marca_modelo_lista2_exc_priority.csv', index=False)