import numpy as np
import plotly.express as px
import pandas as pd
import customers
import baskets
import cat_distr
import exper

data = pd.read_csv('final.csv.csv')
essential_goods = {"Авиабилеты": 3,
                   "Автоуслуги": 2,
                   "Аптеки": 1,
                   "Аренда авто": 3,
                   "Госсборы": 1,
                   "Дом/Ремонт": 3,
                   "Ж/д билеты": 3,
                   "Животные": 3,
                   "Искусство": 3,
                   "Кино": 3,
                   "Книги": 3,
                   "Красота": 3,
                   "Медицинские услуги": 1,
                   "Музыка": 3,
                   "НКО": 3,
                   "Образование": 2,
                   "Одежда/Обувь": 2,
                   "Отели": 3,
                   "Развлечения": 3,
                   "Разные товары": 2,
                   "Рестораны": 3,
                   "Связь/Телеком": 2,
                   "Сервисные услуги": 2,
                   "Спорттовары": 3,
                   "Сувениры": 3,
                   "Супермаркеты": 1,
                   "Топливо": 1,
                   "Транспорт": 1,
                   "Турагентства": 3,
                   "Фаст Фуд": 3,
                   "Финансовые услуги": 2,
                   "Фото/Видео": 3,
                   "Цветы": 3,
                   "Частные услуги": 2
                   }  # 1-likely, 2-maybe, 3 - surely not


def main():
    # print(data["category"].values())
    # customers.spending_bars(data)
    # baskets.mean_basket_graph(data)
    # cat_distr.histogramm(data)
    # print(baskets.mean_category_data(data)["category"])
    # baskets.category_graph(data, "Супермаркеты")
    exper.graph(data)


if __name__ == "__main__":
    main()
