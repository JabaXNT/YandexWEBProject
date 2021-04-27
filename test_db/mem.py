import csv
import sqlite3
from requests import get
import ast
from random import randint


with open('test_db/flipkart_com-ecommerce_sample.csv', encoding="utf8") as fin:
    dr = csv.DictReader(fin, delimiter=",")
    ar = [(i['product_name'], i['retail_price'], i['image']) for i in dr]

con = sqlite3.connect('db/products_final.db')
cur = con.cursor()
count = 0
for i in ar:
    lest = [i[0], i[1], i[2]]
    lest3 = []
    res = ast.literal_eval(i[2])
    for j in res:
        a = get(j)
        if a.status_code == 200:
            lest3.append(j)
    lest[2] = str(lest3)
    if len(lest3) > 0:
        result = cur.execute(
            "INSERT INTO products (title, price, image, count) VALUES (?, ?, ?, ?)", (lest[0], lest[1], lest[2], randint(3, 30),))
    count += 1
    print(count)
    con.commit()
