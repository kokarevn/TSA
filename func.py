import pandas as pd
import datetime
import numpy as np

def fill_data(data: pd.DataFrame, name: str):
    data.Date = pd.to_datetime(data.timestamp)

    start_date = data.timestamp.loc[0] # Выделяем первую дату
    end_date = data.timestamp.loc[len(data)-1] # последнюю

    start_year = start_date.year # Выделяем год, месяц и день первого наблюдения
    start_month =  start_date.month
    start_day = start_date.day

    end_year = end_date.year # Аналогичное делаем для конца
    end_month =  end_date.month
    end_day = end_date.day

    number_of_days = abs((end_date-start_date).days) # Выделяем количество дней от начала наблюдений до конца
    start_date = datetime.date(start_date.year, start_date.month, start_date.day) # Переводим первую дату в режим дейтатайма
    date_list = [] # заводим список дат
    for day in range(number_of_days): # Цикл, который собирает список всех дат в периоде наблюдения по дням НЕРАЗРЫВНО, то есть если между данными были пропущены наблюдения, то у нас их будет больше
      a_date = (start_date + datetime.timedelta(days = day)).isoformat() # datetime.timedelta возвращает продолжительность,
      # операция start_date + datetime.timedelta по сути прибавляет день к стартовому наблюдению и в конца берется .isoformat()
      # переводящий дату в строку и добавляющую в общий список
      date_list.append(a_date)
    date_list = pd.to_datetime(date_list) # Переводим строчные даты в pd.datetime формат
    new_data = pd.DataFrame({'Date':date_list}) # И формируем новый список дат в датафрейм первой колонкой
    x = new_data.Date # Выделяем переменную содержащую в себе новые даты без пропусков, эта колонка сильно больше старой
    old_x = data.Date # Старые даты
    y = [] # Заводим список
    for i in range(len(x)):
      x_i = x.loc[i] # берем каждое наблюдение из новых дат
      diff_list = [] # заводим список разниц
      for j in range(len(data)): # теперь итерируемся по количеству старых наблюдений дат
          diff_list.append(abs((x_i-old_x.loc[j]).days)) # Мы берем абсодютную разницу в днях между нашей синтетичесой датой и каждым наблюдениями в реальных данных, заключаем в список этих разниц
      diff_list = np.array(diff_list) # В конце делаем этот список вектором
      y.append(data[name][diff_list.argmin()]) # diff_list.argmin(). вытаскиваем индекс наблюдения в списке, разица по дням с синтетическим у котороо минимальна и обращается к этому элементу в оригинальных данных и добавляет его цену закрытия
    data = pd.DataFrame(dict({'timestamp':x, name: y}))
    return data