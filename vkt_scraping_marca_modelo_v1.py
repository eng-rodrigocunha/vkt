from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='C:\\WebDriver\\bin\\chromedriver.exe', options=options)

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