#%%
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import plotly.express as px

# %%
# GET DATA FROM THE POWER MACHINES WEBSITE
url = 'https://power-m.ru/customers/references/'
r = requests.get(url)
r.text

# %%
soup = BeautifulSoup(r.text, 'html.parser')
txt = soup.find('div', class_="table-klientam-prom") \
          .find('table', class_="table-investor table-blue block-table-none mobile-bl-none") \
          .find_all('span')
    
# %%
columns = []
for t in txt:
    col = str(t)
    columns.append(col.strip('<span>').strip('</span>'))
    
# %%
rows = []
trs = soup.find_all('tr')
for tr in trs:
    row = [data.text for data in tr.find_all('td')]
    if len(row) != 0:
        rows.append(row)
# %%
# CREATING A DATASET
df = pd.DataFrame(rows, columns=columns)

# %%
# PREPARATION DATASET
sm_df = df[(df['Тип оборудования'] != 'Турбогенераторы') & 
            (df['Тип оборудования'] != 'Трансформаторы') & 
            (df['Тип оборудования'] != ' Трансформаторы') &
            (df['Тип оборудования'] != 'Турбогенераторы ') &
            (df['Тип оборудования'] != 'Гидрогенераторы')]

sm_df['Тип оборудования'] = sm_df['Тип оборудования'].replace('Паровые турбины\t', 'Паровые турбины')
sm_df['Страна'] = sm_df['Страна'].replace('Россия ', 'Россия')

sm_df = sm_df.drop('Напряжение', axis=1)
# %%
sm_df = sm_df.rename(columns={'Тип оборудования': 'type_of_equipment',
                              'Мощность, МВт': 'power',
                              'Кол-во, шт.': 'number_of_turbines',
                              'Станция': 'station',
                              'Страна': 'country',
                              'Год изготовления': 'year_of_manufacture'})

# %%
sm_df['power'] = sm_df['power'].apply(lambda x: float(x) if x != '' else np.nan) 
sm_df['number_of_turbines'] = sm_df['number_of_turbines'].apply(lambda x: int(x) if x != '' else np.nan)
sm_df['sum_power'] = sm_df['power'] * sm_df['number_of_turbines']
sm_df['type_of_station'] = sm_df['station'].str.extract(r'(\bГЭС\b|\bГРЭС\b|\bТЭС\b|\bАЭС\b|\bТЭЦ\b)', 
                                                        flags=re.IGNORECASE)
#%%
sm_df = sm_df[['type_of_equipment', 'type_of_station',
               'station', 'country', 'year_of_manufacture',
               'power', 'number_of_turbines', 'sum_power']]
# %%
# SAVING THE DATASET
sm_df.to_csv('power_machines.csv', header=True, sep=';')

# %%
