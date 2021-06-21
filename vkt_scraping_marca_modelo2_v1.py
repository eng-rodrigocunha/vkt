from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--incognito")
options.headless = True
driver = webdriver.Chrome(executable_path='C:\\WebDriver\\bin\\chromedriver.exe', options=options)

marcas_modelos = pd.read_csv('datasets/marca_modelo_lista.csv')
marcas_modelos.drop_duplicates(subset=['Marca_Cod'], inplace=True)
marcas_modelos2 = pd.read_csv('datasets/marca_modelo_lista2.csv')
marcas_modelos2.drop_duplicates(subset=['Modelo_Cod'], inplace=True)
marcas_modelos2.to_csv('datasets/marca_modelo_lista2.csv', index=False)
marcas_modelos2.drop_duplicates(subset=['Marca_Cod'], inplace=True)
marcas_modelos2 = marcas_modelos2.head(len(marcas_modelos2)-1)
marcas_modelos2_lista = marcas_modelos2['Marca_Cod'].tolist()
#print(marcas_modelos2_lista)

marcas_modelos = marcas_modelos[~marcas_modelos['Marca_Cod'].isin(marcas_modelos2_lista)]

#print(marcas_modelos)

try:
    marca_modelo_lista = []
    for row in marcas_modelos.itertuples():
        #Scraping de Modelos do Veículo
        driver.get(row[5]+'/ficha-tecnica')

        #Carregamento completo da Página
        #WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located)
        #time.sleep(5)

        #Clicando no botão alterar
        modelos = WebDriverWait(driver, 30, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[1]/a'))).click()

        #Lendo menu de modelos
        modelos = WebDriverWait(driver, 30, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltModelMenuCatalog"]')))
        modelos_drpd = Select(modelos)
        modelos_drpd_opts = modelos_drpd.options

        #print(modelos_drpd_opts)
        print('{} {}'.format(row[2], row[4]))
        for m in modelos_drpd_opts:
            #time.sleep(1)
            if(int(m.get_attribute('value')) != 0):
                #Lendo menu de anos do modelo
                anos = WebDriverWait(driver, 30, ignored_exceptions=[NoSuchElementException,StaleElementReferenceException]).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltYearMenuCatalog"]')))
                anos_drpd = Select(anos)
                anos_drpd_opts = anos_drpd.options

                for a in anos_drpd_opts:
                    if(int(a.get_attribute('value')) != 0):
                        marca_modelo_lista.append([row[1],row[2],int(m.get_attribute('value')), m.get_attribute('label'),int(a.get_attribute('value'))])

    driver.close()
    data = pd.DataFrame(marca_modelo_lista, columns=['Marca_Cod', 'Marca', 'Modelo_Cod', 'Modelo', 'Ano'])
    #print(data)

    data.to_csv('datasets/marca_modelo_lista2.csv', index=False, mode='a', header=False)

except:
    driver.close()
    data = pd.DataFrame(marca_modelo_lista, columns=['Marca_Cod', 'Marca', 'Modelo_Cod', 'Modelo', 'Ano'])
    #print(data)

    data.to_csv('datasets/marca_modelo_lista2.csv', index=False, mode='a', header=False)