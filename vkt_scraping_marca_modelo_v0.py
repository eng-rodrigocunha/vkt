from selenium import webdriver
# from selenium.webdriver import Opera
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

# driver = Opera(executable_path='C:\\WebDriver\\bin\\operadriver.exe', service_args='-test-type')
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
i = 0
marca_modelo_lista = []
for opt in marcas_lista:
    i += 1
    if(i < 10):
        j=1
        driver.get("https://www.icarros.com.br/"+opt[1].lower().replace(' ','-'))
        while True:
            try:
                modelo_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-card__item')))
                modelo_id = driver.find_elements_by_class_name('list-card__item')
                #print(modelo_id)
                #modelo_nome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title--brand__highlight'))).getText()
                modelo_nome = driver.find_elements_by_class_name('title--brand__highlight')
                #print(modelo_nome)
                #modelo_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card--review__cta')))
                modelo_link = driver.find_elements_by_class_name('card--review__cta')
                #print(modelo_link)
                modelo_id_lista = [li.get_attribute('id') for li in modelo_id]
                #print(modelo_id_lista)
                modelo_nome_lista = [strong.text for strong in modelo_nome]
                #print(modelo_nome_lista)
                modelo_link_lista = [a.get_attribute('href') for a in modelo_link]
                #print(modelo_link_lista)
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
#Teste de Scraping de Modelos por Marca
driver.get("https://www.icarros.com.br/bmw")

marca_modelo_lista = []
j = 1
while True:
    modelo_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-card__item')))
    modelo_id = driver.find_elements_by_class_name('list-card__item')
    #print(modelo_id)
    #modelo_nome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title--brand__highlight'))).getText()
    modelo_nome = driver.find_elements_by_class_name('title--brand__highlight')
    #print(modelo_nome)
    #modelo_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card--review__cta')))
    modelo_link = driver.find_elements_by_class_name('card--review__cta')
    #print(modelo_link)
    modelo_id_lista = [li.get_attribute('id') for li in modelo_id]
    print(modelo_id_lista)
    modelo_nome_lista = [strong.text for strong in modelo_nome]
    print(modelo_nome_lista)
    modelo_link_lista = [a.get_attribute('href') for a in modelo_link]
    print(modelo_link_lista)
    for id, nome, link in zip(modelo_id_lista, modelo_nome_lista, modelo_link_lista):
        marca_modelo_lista.append(['[opt[0]', 'opt[1]', id, nome, link])

    j += 1
    #try:
    print('a[onmousedown="b_Pag(this,{});"]'.format(j))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[onmousedown="b_Pag(this,{});"]'.format(j)))).click()
    #except:
        #break

    if(j > 2):
        break

print(marca_modelo_lista)
'''

'''
marca_modelo_lista = []
for opt_marca in marca_drpd_opts:
    if(int(opt_marca.get_attribute('value')) != 0):
        print(opt_marca.get_attribute('value'))
        marca2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sltMake [value='{}']".format(opt_marca.get_attribute('value')))))
        modelo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#sltModel")))
        #marca_drpd.select_by_value(opt_marca.get_attribute('value'))
        #modelo = WebDriverWait(driver, 10).until(EC.element_located_to_be_selected((By.XPATH, '//*[@id="sltModel"]')))
        #modelo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltModel"]')))
        modelo_drpd = Select(modelo)
        modelo_drpd_opts = modelo_drpd.options

        for opt_modelo in modelo_drpd_opts:
            temp = [int(opt_marca.get_attribute('value')), opt_marca.get_attribute('label'), int(opt_modelo.get_attribute('value')), opt_modelo.get_attribute('label')]
            marca_modelo_lista.append(temp)

print(marca_modelo_lista)

'''


'''
for opt_marca in marcas_lista:
    print(opt_marca[1])
    marca_drpd.select_by_visible_text(opt_marca[1]).click()


    modelo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sltModel"]')))
    modelo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltModel"]')))
    modelo_drpd = Select(modelo)
    modelo_drpd_opts = modelo_drpd.options

    marca_modelo_lista = []
    for opt_modelo in modelo_drpd_opts:
#        if(int(opt.get_attribute('value')) != 0):
            temp = [opt_marca[0], opt_marca[1], int(opt_modelo.get_attribute('value')), opt_modelo.get_attribute('label')]
            marca_modelo_lista.append(temp)

print(marca_modelo_lista)
'''