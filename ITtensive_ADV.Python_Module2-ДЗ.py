#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Основанная на методе наименьших квадратов линейная одномерная регрессия является широко используемым приемом
для построения прямой линии, проходящей через набор двумерных точек.'''


# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# In[2]:


bezrab_msk=pd.read_csv("https://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv",sep=';')
bezrab_msk['UnPercnt']=bezrab_msk['UnemployedDisabled']/bezrab_msk['UnemployedTotal']*100
bezrab_msk['UnPercnt'].head()


# In[3]:


bezrab_msk.head()


# In[4]:


data=bezrab_msk
data = data.groupby("Year").filter(lambda x: x["Year"].count() >= 6)
data.head()


# In[5]:


data_avg2 = data.groupby("Year").mean()
data_avg2.head()


# In[7]:


#Готоим модель нашей линейной регрессии
x = np.array(data_avg2.index).reshape(len(data_avg2.index), 1)#решейпим наш массив из одномерного в думерный (лин.рег. работает только с двумерными массиваам)
y = np.array(data_avg2["UnPercnt"]).reshape(len(data_avg2.index), 1)#то же для набора данных y
#print(data_avg2.index)
print(x)
print(y)


# In[8]:


#Теперь строим модель линейной регрессии и загружаем в нее данные:
model = LinearRegression()
model.fit(x, y)


# In[10]:


#Фактически, мы уже готовы получить ответ.
#Но давайте посмотрим какие данные у нас получились. Построим график разброса значений
plt.scatter(x, y,  color='orange')
#Добавим в годы 2020 , чтобы увидеть предсказанное значение на графике.
x = np.append(x, [2020]).reshape(len(data_avg2.index)+1, 1)#после аппенда надо снова решейпить. Обрати + 1 добавляем т.к. к x у нас добавился 1 элемент. (т.е. форма стала на +1 больше)
#Теперь добавим линейный график по предсказанным данным
plt.plot(x, model.predict(x), color='blue', linewidth=3)
plt.show()


# In[9]:


'''Дополнительно можно вывести значение предсказание,
для этого потребуется снова reshape от единственного значения - 2020 - чтобы сделать из него таблицу:'''
#print(model.predict(np.array(2020).reshape(1, 1)))
x=float(model.predict(np.array(2020).reshape(1, 1)))
round(x,2)
                


# In[ ]:




