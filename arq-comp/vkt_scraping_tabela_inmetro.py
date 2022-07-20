import tabula as tb
import pandas as pd
import numpy as np

#df = tb.read_pdf('http://www.inmetro.gov.br/consumidor/pbe/veiculos_leves_2020.pdf', stream=True)
df = tb.read_pdf_with_template('http://www.inmetro.gov.br/consumidor/pbe/veiculos_leves_2020.pdf', stream=True)

print(df)