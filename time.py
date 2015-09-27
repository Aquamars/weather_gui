# -*- coding: utf-8 -*- 
import os, sys, urllib, urllib2
from urllib2 import urlopen,Request
from bs4 import BeautifulSoup 
import sys
from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
 
################
##print time
import time
t=time.time()
tmp_time=time.strftime('%m/%d %H:%M', time.localtime(t))
print tmp_time
###############

resp = urllib2.urlopen('http://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm')
soup = BeautifulSoup(resp)

trs=soup.find_all('td')

print trs[0].get_text()  

root = Tk()
root.title("Temperature")
frame = Frame(root)
frame.pack()

t_label = Label(frame, text="Taichung City: {t} °c".format(t=trs[0].get_text()), width="30", height="5")
t_label.pack(side = LEFT)


image = Image.open("images.jpg")
photo = ImageTk.PhotoImage(image)
background_label = Label(frame, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.pack()


root.mainloop()
