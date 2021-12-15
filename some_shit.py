import pandas as pd

data = pd.read_csv("tink.csv")


def quantile_outliers(sample, column: str):
    """Deletes outliers form dataframe {sample} using Tukey's fences. Returns dataframe"""
    q25 = sample[column].quantile(0.25)
    q75 = sample[column].quantile(0.75)
    more = sample[column] >= q25 - 1.5 * (q75 - q25)
    less = sample[column] <= q75 + 1.5 * (q75 - q25)
    return sample[more & less]


good_mcc = []

for mcc in data["code"].unique():
    sample = data[data["code"] == mcc]
    online_sample = quantile_outliers(sample[sample["online_transaction_flg"] == 1], "transaction_amt")
    offline_sample = quantile_outliers(sample[sample["online_transaction_flg"] == 0], "transaction_amt")

    if online_sample["code"].size >= 50:
        good_mcc.append((mcc, online_sample["transaction_amt"].std(), "online"))
    if offline_sample["code"].size >= 50:
        good_mcc.append((mcc, offline_sample["transaction_amt"].std(), "offline"))

print(*sorted(good_mcc, key=lambda a: (a[1], a[0]))[:16], sep="\n")