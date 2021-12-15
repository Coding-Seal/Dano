import pandas as pd

data = pd.read_csv("tink.csv")


def quantile_outliers(dataframe, column: str):
    """Deletes outliers form dataframe {sample} using Tukey's fences. Returns dataframe"""
    q25 = dataframe[column].quantile(0.25)
    q75 = dataframe[column].quantile(0.75)
    more = dataframe[column] >= q25 - 1.5 * (q75 - q25)
    less = dataframe[column] <= q75 + 1.5 * (q75 - q25)
    return dataframe[more & less]


good_mcc = []

for mcc in data["code"].unique():
    sample = quantile_outliers(data[data["code"] == mcc], "transaction_amt")

    if sample["code"].size >= 50:
        good_mcc.append((mcc, sample["transaction_amt"].std()))



# fun = pd.DataFrame(dict(code=[a[0] for a in good_mcc], std=[a[1] for a in good_mcc]))

# mcc = pd.read_csv("mcc_code.csv", sep=";", encoding="Windows-1251")
# mcc = dict(zip(mcc["mcc"], mcc["значение mcc"]))

# fun["code"] = fun["code"].replace(mcc)
# print(fun.sort_values("std"))

# (4131, 14.87903451444718, 'offline')
# (7999, 22.8176830776325, 'online')
# (7299, 25.793528693239697, 'online')
# (4111, 28.918124242339957, 'offline')
# (8398, 34.91601346634131, 'online')
# (3423, 75.13193278358581, 'online')
# (5735, 84.85666185529861, 'online')
# (5462, 130.7666086006701, 'offline')
# (7512, 139.17762286330927, 'online')
# (5499, 144.82340038240352, 'offline')
# (4111, 150.45565226087086, 'online')
# (3431, 171.324782656162, 'online')
# (5814, 186.40328530275417, 'offline')
# (7523, 188.4078118958265, 'offline')
# (7311, 220.1265415748276, 'online')
# (5311, 244.54967705097684, 'offline')
