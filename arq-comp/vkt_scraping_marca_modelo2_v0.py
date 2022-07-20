from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import numpy as np

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
driver = webdriver.Chrome(executable_path='C:\\WebDriver\\bin\\chromedriver.exe', options=options)

marcas_modelos = pd.read_csv('marca_modelo_lista.csv')
print(marcas_modelos)
marcas_modelos.drop_duplicates(subset=['Marca Código'], inplace=True)
print(marcas_modelos)

marca_modelo_lista = []
i = 0
for row in marcas_modelos.itertuples():
    i += 1
    print(row[5])
    #Scraping de Modelos do Veículo
    driver.get(row[5]+'/ficha-tecnica')

    #Clicando no botão alterar
    modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[1]/a'))).click()

    #Lendo menu de modelos
    modelos = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltModelMenuCatalog"]')))
    modelos_drpd = Select(modelos)
    modelos_drpd_opts = modelos_drpd.options

    print(modelos_drpd_opts)
    for m in modelos_drpd_opts:
        print(m.get_attribute('value'))
        if(int(m.get_attribute('value')) != 0):
            #Lendo menu de anos do modelo atual
            anos = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltYearMenuCatalog"]')))
            anos_drpd = Select(anos)
            anos_drpd_opts = anos_drpd.options

            for a in anos_drpd_opts:
                if(int(a.get_attribute('value')) != 0):
                    marca_modelo_lista.append([row[1],row[2],int(m.get_attribute('value')), m.get_attribute('label'),int(a.get_attribute('value'))])
    
    if(i > 9):
        break

data = pd.DataFrame(marca_modelo_lista, columns=['Marca Código', 'Marca', 'Modelo Código', 'Modelo', 'Ano'])
print(data)
data.drop_duplicates(inplace=True)
print(data)
data.sort_values(by=['Modelo Código'],inplace=True)

data.to_csv('marca_modelo_lista2.csv', index=False)

'''
#Scraping de Marcas
driver.get("https://www.icarros.com.br/catalogo")

marca = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltMake"]')))
marca_drpd = Select(marca)
marca_drpd_opts = marca_drpd.options

marcas_lista = []
for opt in marca_drpd_opts:
    if(int(opt.get_attribute('value')) != 0):
        temp = [int(opt.get_attribute('value')), opt.get_attribute('label')]
        marcas_lista.append(temp)

#Scraping de Modelos por Marca
marca_modelo_lista = []
for opt in marcas_lista:
    j=1
    driver.get("https://www.icarros.com.br/"+opt[1].lower().replace(' ','-'))
    while True:
        try:
            modelo_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-card__item')))
            modelo_id = driver.find_elements_by_class_name('list-card__item')
            modelo_nome = driver.find_elements_by_class_name('title--brand__highlight')
            modelo_link = driver.find_elements_by_class_name('card--review__cta')
            modelo_id_lista = [li.get_attribute('id') for li in modelo_id]
            modelo_nome_lista = [strong.text for strong in modelo_nome]
            modelo_link_lista = [a.get_attribute('href') for a in modelo_link]
            for id, nome, link in zip(modelo_id_lista, modelo_nome_lista, modelo_link_lista):
                marca_modelo_lista.append([opt[0], opt[1], id, nome, link])
        except:
            print(opt[1]+' - nenhum veículo encontrado para scraping de dados')
        j += 1    
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[onmousedown="b_Pag(this,{});"]'.format(j)))).click()
        except:
            break

data = pd.DataFrame(marca_modelo_lista, columns=['Marca Código', 'Marca', 'Modelo Código', 'Modelo', 'Link Modelo'])
print(data)

data.to_csv('marca_modelo_lista.csv', index=False)
'''