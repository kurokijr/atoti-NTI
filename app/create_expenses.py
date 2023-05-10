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

    ratio_vs_std_h: list[str] = []
    ratio_vs_std_m:list[float] = []
    valor_analisado:list[float] = []

    target_status:list[str] = ["Aceito", "Aceito parcialmente", "Rejeitado"]

    for row in df.itertuples():
        p = row.Projeto
        r = row.Rubrica
        v = row.Valor_apresentado
        s = row.Status
        std = 0
        std = 0.0 if math.isnan(dict_std.get((p, r))) else dict_std.get((p, r))
        mean = dict_avg.get((p, r))
        dsc = v - mean
        if (std != 0 and dsc != 0):
            target = dsc/std
            tier = round_off_rating(target)
        else:
            tier = 0
        ratio_vs_std_h.append(str(tier))
        ratio_vs_std_m.append(tier)

        if s in target_status:
            valor_analisado.append(v)
        else:
            valor_analisado.append(0)

    df["Ratio_VS_STD_h"] = ratio_vs_std_h
    df["Ratio_VS_STD_m"] = ratio_vs_std_m
    df["Valor_analisado"] = valor_analisado

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
