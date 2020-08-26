#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Задание ДЗ 3 модуля на чисто, с комментариями'''


# In[ ]:


import requests
from bs4 import BeautifulSoup
headers = {"User-Agent": "ittensive-python-courses/1.0 (+https://www.ittensive.com/)"}
url="https://video.ittensive.com/data/018-python-advanced/beru.ru/"#ссылка на зеркало
r = requests.get(url, headers=headers)
html = BeautifulSoup(r.content)
#print (html)#не будем печатать в итоговой версии
def find_links (links, keyword):# find_links - имя функции, а в скобках указываем параметры, который ф. получает на входе
#здесь это будут ссылки (links) которые функция будет обрабатывать и ключевое слво(keyword), по которому функция будет фильтровать эти ссылки только с нужными нам тегами
    links_filtered = {}#наш словарик, куда мы будем складывать результаты. Словарик, а не список - чтобы ссылки были уникальными
    for link in links:#запускаем перебор ссылок в цикле
#next row:услвоие-у ссылки есть атрибут хреф,и этот атрибут (хреф) содержит наше ключевое слово (через услвоие на индекс>-1)
        if link.has_attr("href") and link["href"].find(keyword) > -1:
            links_filtered[link["href"]] = 1 #здесь мы объявляем, что значение ключа из словаря=1. Т.е. все ссылки в слоавре будут уникальными. а их значение=1
    return list(links_filtered.keys())#здесь мы преобразуем значения словаря в список            
holod = []#создаем пустой список уже  для ссылок на холодильники
holod.extend(find_links(html.find_all("a"), "kholodilnik-saratov")) #здесь двухходовочка.Сначала мы вызываем нашу функцию с 2-мя параметрами (ссылка и кейворд)
#а вторым действием заносим результат работы функции в список holod
#в результате в списке holod будут ссылки на страницы моделей (без домена), только урлы

result=[]#создаем пустой список для занесения наборов значений по условию ДЗ
for hols in holod:
    url2 = url + hols.strip()#соединяем домен+урл=получаем готовую ссылку для парсинга. Предв-но через стрип убираем возможные пробелы в начале/конце, чтобы не было сюрпризов со ссылками
    r = requests.get(url2)#создаем реквест из урла
    html = BeautifulSoup(r.content)
    h1=html.find("h1", {"data-tid-prop":"4b145b4d 8c8a88a0"}).get_text()#парсим тег с названием модели и выцепляем его текст
    price = html.find("span", {"data-tid":"c3eaad93"}).get_text()#парсим тег с ценой и выцепляем его текст
    tags = html.find_all("span", {"class":"_112Tad-7AP"})#здесь парисим сложный тег с нескольими элементами
    size = tags[0].get_text()#это 0 элемент нашего сложного тега
    wvol = tags[2].get_text()#это 2 элемент нашего сложного тега
    vol  = tags[3].get_text()# это 3 элемент нашего сложного тега 
    result=[url2,h1,price,size,wvol,vol]#заносим строку набора в наш список
    with open("fridges.csv", "a", encoding="utf-8") as f:#создаем csv,очень важно открыть его с параметром 'a' -чтобы запись была в конец файла. И также кодировка, т.к. в примере текста в кривой кодировке
        f.write(",".join(result))#записываем набор в файл одной строчкой
        f.write('\n')#делаем перевод строки
#результатом будет файл с наборами значений по каждой найденой модели
import pandas as pd
df = pd.read_csv('fridges.csv', sep=',', names = ['url', 'title', 'price','size','whole_volume','freezer_volume'],encoding="utf-8")
# в строке выше создаем из нашего csv датафрейм. Будем использовать метод добавления в таблицу SQL
# метод добавления из дф, собственной разработки
import sqlite3 #импортируем нужные библиотеки
import numpy as np #импортируем нужные библиотеки
conn = sqlite3.connect("SQL-light/data.db3")#Это коннектор
db = conn.cursor()#а это объект
conn.commit()#это строчка означает завершение команды
db.execute("""CREATE TABLE fridges 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT not null,
                   url text,
                   title text default '',
                   price text default '',
                   size text default '',
                   whole_volume text default '',
                   freezer_volume text default '')""")
conn.commit()#выше - создаем таблицу с такими же полями, как у нашего дф с наборами
for index, row in df.iterrows():#волшебный метод, который обходит фрейм построчно. Это то, что нам нужно, чтобы добавить всю строку с набором прямо в такую же таблицу
    db.execute(
        "INSERT INTO fridges (url,title,price,size,whole_volume,freezer_volume) VALUES (?,?,?,?,?,?)",#команда для sql добавить по именами столбцов все значения (?)
        (row['url'],row['title'],row['price'],row['size'],row['whole_volume'],row['freezer_volume'])) #здесь перечисляем столбцы, которые будем добавлять построчно
conn.commit()
data = np.array(db.execute("SELECT * FROM fridges").fetchall())#выбираем данные из таблицы и загружаем в массив numpy
print (data)
db.close()#завершаем работу с базой данных.


# In[ ]:


'''Еще 1 вариант посмотреть результат - вывести таблицу в датафрейм'''
itog = pd.read_sql_query("SELECT * FROM fridges", conn)
itog.head(10)
db.close()#завершаем работу с базой данных.


# In[ ]:


#полезная команда для удаления таблицы после предыдущей итерации
db.execute("""DROP TABLE fridges""")
conn.commit()

