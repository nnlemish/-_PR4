#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# In[26]:


#1 Загрузити датасет, що містить інформацію про відвідуваність музеїв в різні роки. 
data = pd.read_csv(r'C:\Users\admin\Desktop\Настя\museum_visitors.csv')


# In[27]:


#2 Вивести перші 5 рядків датасету. 
data.head(5)


# In[28]:


#3 Провести попередній аналіз даних (визначити розмір датасету, тип даних, кількість пропусків). 
print('Розмір датасету: ', data.shape)
print('Типи даних, що містить датасет: ', data.dtypes)
print('Кількість пропусків в кожному стовпці: ', data.isna().sum())


# In[29]:


#4 Перевірити наявність дублікатів. Якщо є, видалити їх і вивести розмір таблиці (без дублікатів). 
duplicates = data.duplicated()
print('Загальна кількість дублікатів:', duplicates.sum())
data_without_dupl = data.drop_duplicates()
rows_without_dupl, columns_without_dupl = data_without_dupl.shape
print('Кількість рядків після видалення дублікатів: ', rows_without_dupl)
print('Кількість стовпців: ', columns_without_dupl)


# In[30]:


#5 Про які роки містить інформацію датасет. 
date = pd.to_datetime(data['Date'], format='%Y-%m-%d')
year = date.dt.year
уnique_years = year.unique()
print('Роки, які містяться в датасеті: ', уnique_years)


# In[31]:


#6 Змінити назви столбців. Замінити великі букви на маленьки, пробіли на підкреслення (date, avila_adobe, firehouse_museum, chinese_american_museum, america_tropical_interpretive_center). 
data.columns = ['date', 'avila_adobe', 'firehouse_museum', 'chinese_american_museum', 'america_tropical_interpretive_center']
data


# In[32]:


#7 Обчислити середню кількість відвідувачів для кожного музею протягом всього періоду. 
average_visitors = data[['avila_adobe', 'firehouse_museum', 'chinese_american_museum', 'america_tropical_interpretive_center']].mean()
print(average_visitors)


# In[33]:


#8 Знайти мінімальну та максимальну кількість відвідувачів для кожного музею за 2018 рік 
maximum = data[['avila_adobe', 'firehouse_museum', 'chinese_american_museum', 'america_tropical_interpretive_center']].max()
print('Максимальна кількість відвідувачів музеїв: \n', maximum)
minimum = data[['avila_adobe', 'firehouse_museum', 'chinese_american_museum', 'america_tropical_interpretive_center']].min()
print('Мінімальна кількість відвідувачів музеїв: \n', minimum)


# In[34]:


#9 Визначити місяці з найвищою і найнижчою загальною кількістю відвідувачів серед усіх музеїв для 2015 року. Вивести назви місяців (не цифри). 

data_2015 = data[year == 2015]
data_2015["date"] = pd.to_datetime(data_2015["date"])
data_2015["month"] = data_2015["date"].dt.strftime('%B')
data_2015.drop("date", axis=1, inplace=True)
data_2015["total_visitors"] = data_2015.sum(axis=1)

highest_month = data_2015["month"].iloc[data_2015["total_visitors"].argmax()]
lowest_month = data_2015["month"].iloc[data_2015["total_visitors"].argmin()]

print(f"Місяць з найвищою загальною кількістю відвідувачів: {highest_month}")
print(f"Місяць з найнижчою загальною кількістю відвідувачів: {lowest_month}")


# In[35]:


#10 Порівняти кількість відвідувачів музею "Avila Adobe" у літні і зимові місяці 2018 року 
data_2018 = data[year == 2018]
data_2018["date"] = pd.to_datetime(data_2018["date"])
data_2018["month"] = data_2018["date"].dt.strftime("%B")
data_2018.drop("date", axis=1, inplace=True)
summer_months = data_2018[data_2018["month"].isin(["June","July","August"])]
winter_months = data_2018[data_2018["month"].isin(["January","February"])]
summer_visitors = summer_months["avila_adobe"].sum()
winter_visitors = winter_months["avila_adobe"].sum()

print(f"Кількість відвідувачів музею 'Avila Adobe' у літні місяці: {summer_visitors}")
print(f"Кількість відвідувачів музею 'Avila Adobe' у зимові місяці: {winter_visitors}")


# In[36]:


#11 Завдання знайти кореляцію між кількістю відвідувачів в кожному з музеїв  та датами у 2016 році

data_2016 = data[year == 2016]
data_2016["date"] = pd.to_datetime(data_2016["date"])
data_2016["month"] = data_2016["date"].dt.strftime("%B")

data_2016["date"] = data_2016["date"].dt.to_period("D").astype(int)
for museum in ["avila_adobe", "firehouse_museum", "chinese_american_museum", "america_tropical_interpretive_center"]:
    print(f"Кореляція між кількістю відвідувачів музею {museum} та датою: {data_2016[museum].corr(data_2016['date'])}")


# In[37]:


#12 Завдання побудувати теплокарту кореляції для попереднього завдання.

import seaborn as sns

corr = data_2016.corr()
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)


# In[38]:


#13 Завдання побудувати графік ліній для кожного музею, показуючи їхню відвідуваність протягом 2017 року.
import matplotlib.pyplot as plt

data_2017 = data[year == 2017]
data_2017["date"] = pd.to_datetime(data_2017["date"])
data_2017["month"] = data_2017["date"].dt.strftime("%B")
data_2017.drop("date", axis=1, inplace=True)
for museum in ["avila_adobe", "firehouse_museum", "chinese_american_museum", "america_tropical_interpretive_center"]:
    series = data_2017[["month", museum]].set_index("month")
    plt.plot(series)
    plt.xlabel("Дата")
    plt.xticks(rotation=45)
    plt.ylabel("Кількість відвідувачів")
    plt.legend(["Avila Adobe", "Firehouse Museum", "Chinese American Museum", "America Tropical Interpretive Center"], fontsize=7)

plt.show()


# In[39]:


# 14 Завдання побудувати графіки розсіювання для кожного музею за 2018 рік

for museum in data_2018.columns:
    plt.scatter(data_2018["month"], data_2018[museum])
    plt.title(museum)
    plt.xticks( rotation=45)
    plt.show()


# In[40]:


#15 Завдання гістограма відвідуваності за місяцями кожного музею. Вивести 4 графіки: за 2014, 2015, 2016, 2017 роки.
#ці графіки розташовані два зверху, два знизу, колір 1 графіка - синій, 2 - зелений, 3 - жовтий, 4 - сірий.

fig, ax = plt.subplots(2, 2, figsize=(10,8))

data_2014 = data[year == 2014]
data_2014["date"] = pd.to_datetime(data_2014["date"])
data_2014["month"] = data_2014["date"].dt.strftime("%B")
data_2014.drop("date", axis=1, inplace=True)
museums_2014 = data_2014.columns[0:4]
ax[0,0].set_title("2014")  
for museum in museums_2014:
  ax[0,0].plot(data_2014["month"], data_2014[museum], color="b")

museums_2015 = data_2015.columns[0:4]  
ax[0,1].set_title("2015")
for museum in museums_2015:
  ax[0,1].plot(data_2015["month"], data_2015[museum], color="g")

museums_2016 = data_2016.columns[0:4]
ax[1,0].set_title("2016")
for museum in museums_2016:
  ax[1,0].plot(data_2016["month"], data_2016[museum], color="y")

museums_2017 = data_2017.columns[0:4]
ax[1,1].set_title("2017")  
for museum in museums_2017:
  ax[1,1].plot(data_2017["month"], data_2017[museum], color="gray")

for tick in ax[0,0].xaxis.get_major_ticks():
    tick.label.set_rotation(45)

for tick in ax[0,1].xaxis.get_major_ticks():
    tick.label.set_rotation(45)
    
for tick in ax[1,0].xaxis.get_major_ticks():
    tick.label.set_rotation(45)
    
for tick in ax[1,1].xaxis.get_major_ticks():
    tick.label.set_rotation(45)


# In[ ]:




