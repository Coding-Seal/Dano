import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn import model_selection

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
    sample = data[data["code"] == mcc]
    online_sample = quantile_outliers(sample[sample["online_transaction_flg"] == 1], "transaction_amt")
    offline_sample = quantile_outliers(sample[sample["online_transaction_flg"] == 0], "transaction_amt")

    if online_sample["code"].size >= 100:
        good_mcc.append((mcc, online_sample["transaction_amt"].std(), 1))
    if offline_sample["code"].size >= 100:
        good_mcc.append((mcc, offline_sample["transaction_amt"].std(), 0))

good_mcc = sorted(good_mcc, key=lambda a: (a[1], a[0]))[:]

print(len(good_mcc), sep=",\n")
quit()

good_mcc = [(4131, 14.87903451444718, 0),
            (7999, 22.8176830776325, 1),
            (7299, 25.793528693239697, 1),
            (4111, 28.918124242339957, 0),
            (8398, 34.91601346634131, 1),
            (3423, 75.13193278358581, 1),
            (5735, 84.85666185529861, 1),
            (5462, 130.7666086006701, 0),
            (7512, 139.17762286330927, 1),
            (5499, 144.82340038240352, 0),
            (4111, 150.45565226087086, 1),
            (3431, 171.324782656162, 1),
            (5814, 186.40328530275417, 0),
            (7523, 188.4078118958265, 0),
            (7311, 220.1265415748276, 1),
            (5311, 244.54967705097684, 0),
            (4814, 253.02328111806963, 1),
            (5993, 259.9073821507421, 0),
            (5942, 263.7238044615665, 0),
            (4121, 276.06755163293565, 1), ]


for code, _, flag in good_mcc:
    sample = data[data["code"] == code]
    print(f"--------------{code}--------------")
    # print(sample[sample["online_transaction_flg"] == flag])
    sample = quantile_outliers(sample[sample["online_transaction_flg"] == flag], "transaction_amt")
    # print(sample)
    sample["mor"] = sample["time_of_day"] == "Утро"
    sample["day"] = sample["time_of_day"] == "День"
    sample["evn"] = sample["time_of_day"] == "Вечер"
    sample["mor"] = sample["mor"].astype(int)
    sample["day"] = sample["day"].astype(int)
    sample["evn"] = sample["evn"].astype(int)
    models = [LinearRegression(),  # метод наименьших квадратов
              RandomForestRegressor(n_estimators=100, max_features='sqrt'),  # случайный лес
              KNeighborsRegressor(n_neighbors=6),  # метод ближайших соседей
              SVR(kernel='linear'),  # метод опорных векторов с линейным ядром
              LogisticRegression()  # логистическая регрессия
              ]
    trn = sample[["mor", "evn", "day"]]
    # print(trn)
    trg = sample["transaction_amt"]
    # print(trg)
    Xtrn, Xtest, Ytrn, Ytest = model_selection.train_test_split(trn, trg, train_size=0.8)
    # print(Xtrn)
    best_model = ("", 0)
    score = 0
    for model in models:
        # получаем имя модели
        m = str(model)
        # tmp['Model'] = m[:m.index('(')]
        # для каждого столбцам результирующего набора
        # обучаем модель
        model.fit(Xtrn, Ytrn)
        pred = model.predict(Xtest)

        score = r2_score(Ytest, pred)
        print(m, score)
        if best_model[1] < score:
            best_model = (m, score)
    # print(best_model)



# mcc = pd.read_csv("mcc_code.csv", sep=";", encoding="Windows-1251")
# mcc = dict(zip(mcc["mcc"], mcc["значение mcc"]))
#
# fun["code"] = fun["code"].replace(mcc)
