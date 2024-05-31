# %%
import pandas as pd
import numpy as np
import re
import funcs

# %%
# GET DATA FROM THE POWER MACHINES WEBSITE
url = "https://power-m.ru/customers/references/"
df = funcs.get_data(url)
 # %%
# PREPARATION DATASET
sm_df = funcs.prepare_data(df)
# %%
sm_df["power"] = sm_df["power"].apply(lambda x: float(x) if x != "" else np.nan)
sm_df["number_of_turbines"] = sm_df["number_of_turbines"].apply(
    lambda x: int(x) if x != "" else np.nan
)
sm_df["sum_power"] = sm_df["power"] * sm_df["number_of_turbines"]
sm_df["type_of_station"] = sm_df["station"].str.extract(
    r"(\bГЭС\b|\bГРЭС\b|\bТЭС\b|\bАЭС\b|\bТЭЦ\b)", flags=re.IGNORECASE
)
# %%
sm_df = sm_df[
    [
        "type_of_equipment",
        "type_of_station",
        "station",
        "country",
        "year_of_manufacture",
        "power",
        "number_of_turbines",
        "sum_power",
    ]
]
# %%
# SAVING THE DATASET
sm_df.to_csv("power_machines.csv", header=True, sep=";")

# %%
