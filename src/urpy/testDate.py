
from datetime import datetime

#today=datetime(2017, 11, 28, 23, 55, 55, 55)
#heure = datetime.date('13/08/2021 10:00')

#print(today)
#print(f'{today.min}h{today.min}')

#b = datetime(2017, 11, 28, 23, 55)
#print(b)


date_string = "2021-08-10 15:00"
print("date_string =", date_string)

date = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
print("date_object =", date)

# current date and time
#now = datetime.now()

t = date.strftime("%Hh%M")
print("heure formatée :", t)

s1 = date.strftime("%Y-%m-%d")
print("date formatée :", s1)




