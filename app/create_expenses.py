from __future__ import annotations

import math

import atoti as tt
import pandas as pd


def round_off_rating(number: float) -> float:
    return round(number * 2) / 2

def create_expenses_table(session: tt.Session, /) -> None:

    df = pd.read_csv("app/data/TBDadosParecer.csv", sep=",", encoding="utf-8")

    df[["Inicial", "Complementar_1", "Complementar_2", "Complementar_3"]] = df["Parecer"].str.split(",", expand=True)

    df.pop("Parecer")
    df.pop("sequencial")

    standard_deviations = df.groupby(["Projeto","Rubrica"])["Valor_apresentado"].std()
    dict_std = standard_deviations.to_dict()

    averages = df.groupby(["Projeto","Rubrica"])["Valor_apresentado"].mean()
    dict_avg = averages.to_dict()

    ratio_vs_std: list[str] = []

    for row in df.itertuples():
        p = row.Projeto
        r = row.Rubrica
        v = row.Valor_apresentado
        std = 0
        std = 0.0 if math.isnan(dict_std.get((p, r))) else dict_std.get((p, r))
        mean = dict_avg.get((p, r))
        dsc = v - mean
        if (std != 0 and dsc != 0):
            target = dsc/std
            tier = round_off_rating(target)
        else:
            tier = 0
        ratio_vs_std.append(str(tier))

    df["Ratio_VS_STD"] = ratio_vs_std

    df["unit_count"] = 1

    expenses_table = session.read_pandas(df, table_name="PCdata")

    cube = session.create_cube(expenses_table)

    h, l, m = cube.hierarchies, cube.levels, cube.measures

    h["Parecer"] = [
        l["Inicial"],
        l["Complementar_1"],
        l["Complementar_2"],
        l["Complementar_3"],
        l["Situacao_Parecer"]
    ]
