from datetime import datetime, date, timedelta

import time
import threading

#future = date.today() + timedelta(days=30)
#print( abs( (date.today() - future).days) )

# import tkinter
# import pyautogui as pag
#pyautogui methods:
    # .typewrite(string)
    # .press("enter")

now = datetime.now()
print(now)

rda = [
    2021,
    6,
    9,
    1,
    15
]

rd = datetime(rda[0], rda[1], rda[2], rda[3], rda[4])

print(now)
print(rd)

# difference: use method call .total_seconds()
# instead of .seconds, for a timedelta object
print((now-rd).total_seconds()/60/60)


# SECTION: python auto gui

# time.sleep(.5)
# now = datetime.now()
# print(now)
# 
# dif = now - then
# print(dif)
# now += timedelta(days=5)
# print(now)
# 
# print(now.hour, now.minute)
# 
# print(dif.days, dif.seconds, dif.microseconds)
# # pag.displayMousePosition()
# 