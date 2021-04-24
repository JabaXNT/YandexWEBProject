import csv
import sqlite3
from requests import get
import ast


with open('flipkart_com-ecommerce_sample.csv', encoding="utf8") as fin:
    dr = csv.DictReader(fin, delimiter=",")
    ar = [(i['product_name'], i['image']) for i in dr]

con = sqlite3.connect('db/products.db')
cur = con.cursor()
count = 0
for i in ar:
    lest = [i[0], i[1]]
    lest3 = []
    res = ast.literal_eval(i[1])
    for j in res:
        a = get(j)
        if a.status_code == 200:
            lest3.append(j)
    lest[1] = str(lest3)
    result = cur.execute(
        "INSERT INTO products (title, image, count) VALUES (?, ?, ?)", (lest[0], lest[1], 3,))
    count += 1
    print(count)
    con.commit()
