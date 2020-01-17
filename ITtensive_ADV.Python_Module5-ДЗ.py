#!/usr/bin/env python
# coding: utf-8

# In[22]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("https://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv", delimiter=";")

data["District"] = data["District"].str.replace("район ","").astype("category")#меняем слово район на ""
data["AdmArea"] = data["AdmArea"].apply(lambda x:x.split(" ")[0]).astype("category")#отсекаем все , кроме 1 элемента в названии
#дополнительно приводим эти столбцы к типу "category". Назначение данного тпа позволяет делать группировку быстрее

'''автор исп. оригинальный метод сортировки'''
#сначала он назначает индекс по году
#затем делает фильтрацию по loc
#и в конце сбрасывает индекс
data = data.set_index("YEAR").loc["2018-2019"].reset_index()

fig = plt.figure(figsize=(20, 20))#назначаем холст и размер
area = fig.add_subplot(2, 1, 1)#задаем положение подобласти
area.set_title("ЕГЭ в Москве", fontsize=20)#задаем заголовок/тайтл к диаграмме
total1 = data['PASSES_OVER_220'].sum()
data_adm = data.set_index("AdmArea")#назначаем индекс на столбец, для этого предыдущий индекс был сброшен
data_adm["PASSES_OVER_220"].groupby("AdmArea").sum().plot.pie(ax=area, label="", autopct=lambda x: int(round(total1 * x/100)))#группируем по округу, сразу считаем сумму
#и сразу строим плот в виде пирога(круговая диаграмма. с пустым тайтлом)

data_edu = data_adm.loc["Центральный"].reset_index().set_index("District")
data_edu2 = data_edu.loc["Басманный район"].reset_index().set_index("District")
data_edu3 = data_edu2.reset_index().set_index("EDU_NAME")
total3 = data_edu3['PASSES_OVER_220'].sum()
sr=data_edu3.sort_values('PASSES_OVER_220', ascending=False)


print(str('Общее кол-во сдавших ЕГЭ >=220 по Москве: ')+str(total1))
print(str('Больше всех отличников по ЕГЕ в школе: ')+str(sr.index[0]))


# In[40]:


'''Это удачная попытка. Но сначала надо назначить пароль для приложения
в сервисе яндекса. При отправке на gmail само письмо вроде уходит
но в самом яндексе пишет, что письмо похоже на спам и оно не прошло.
При отпрвке на доменную почту вроде уходит. Пока этот вариант рабочий'''
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

#Зададим все заголовки - From, Subject, Content-Type, To как свойства объекта.
letter = MIMEMultipart()
letter["From"] = "Vladimir Stepanov"
letter["Subject"] = "Результаты ЕГЭ по Москве"
letter["Content-Type"] = "text/html; charset=utf-8"
letter["To"] = "sender@yandex.ru"
#После этого добавим содержание файла parks.html как тело письма. 
letter.attach(MIMEText(open("footer.html", "r",
                            encoding="UTF-8").read(), 'html'))
#После этого дополнительно прикрепим PDF документ, созданный из этого HTML, к самому письму как вложение (attachment).
attachment = MIMEBase('application', "pdf")
attachment.set_payload(open("MSK_EGE.pdf", "rb").read())
#Обязательно зададим заголовок Content-Disposition у вложения:
#это позволит скачать его как нужный файл (имя вложенного файла иначе не передается).
attachment.add_header('Content-Disposition',
                      'attachment; filename="MSK_EGE.pdf"')
#Теперь преобразуем бинарные данные в base64-формат и прикрепим файл к письму:
encoders.encode_base64(attachment)
letter.attach(attachment)
#Наконец, все готово для отправки сформированного письма
user = "sender@yandex.ru"
password = "PASSWORD"
server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
server.login(user, password)
#Отправим письмо, вызвав метод as_string у объекта MIMEMultipart.
server.sendmail("sender@yandex.ru", "support@ittensive.com",letter.as_string())
server.quit()


# In[ ]:




