# %%
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup


# %%
def get_data(url):
    """
    Функция позволяет спарсить данные с сайта
    """
    r = requests.get(url)
    r.text

    soup = BeautifulSoup(r.text, "html.parser")
    txt = (
        soup.find("div", class_="table-klientam-prom")
        .find(
            "table", class_="table-investor table-blue block-table-none mobile-bl-none"
        )
        .find_all("span")
    )

    columns = []
    for t in txt:
        col = str(t)
        columns.append(col.strip("<span>").strip("</span>"))

    rows = []
    trs = soup.find_all("tr")
    for tr in trs:
        row = [data.text for data in tr.find_all("td")]
        if len(row) != 0:
            rows.append(row)

    return pd.DataFrame(rows, columns=columns)


# %%
def prepare_data(df):
    """
    Функция осатвляет только нужные категории в столбце "Тип оборудования", 
    убирает лишние пробелы, удаляет ненужный столбец, переименовывает название столбцов
    """
    sm_df = df[
    (df["Тип оборудования"] != "Турбогенераторы")
    & (df["Тип оборудования"] != "Трансформаторы")
    & (df["Тип оборудования"] != " Трансформаторы")
    & (df["Тип оборудования"] != "Турбогенераторы ")
    & (df["Тип оборудования"] != "Гидрогенераторы")
    ]
    sm_df["Тип оборудования"] = sm_df["Тип оборудования"].replace(
    "Паровые турбины\t", "Паровые турбины"
    )
    sm_df["Страна"] = sm_df["Страна"].replace("Россия ", "Россия")

    sm_df = sm_df.drop("Напряжение", axis=1)
    
    sm_df = sm_df.rename(
    columns={
        "Тип оборудования": "type_of_equipment",
        "Мощность, МВт": "power",
        "Кол-во, шт.": "number_of_turbines",
        "Станция": "station",
        "Страна": "country",
        "Год изготовления": "year_of_manufacture",
        }
    )
    return sm_df
# %%
