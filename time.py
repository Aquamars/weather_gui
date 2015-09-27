# -*- coding: utf-8 -*- 
import os, sys, urllib, urllib2, cStringIO
from urllib2 import urlopen,Request
from bs4 import BeautifulSoup 
import sys
from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import re

##print time
import time
t=time.time()
tmp_time=time.strftime('%m/%d %H:%M', time.localtime(t))
print tmp_time
##

##print row & col
def col_value(rows):
    for row in rows:
        cols = row.findAll('td')
        for col in cols:
            print col.text,"_"
        print "**"
##		

## To get taichung temprature
resp = urllib2.urlopen('http://www.cwb.gov.tw/V7/observe/real/RealData_C.htm')
soup = BeautifulSoup(resp)
trs=soup.find_all('table',{"class" : "BoxTable"})

for c in trs:
	## taichung temprature in row_7 col_1
	rows = c.findAll('tr')
	cols = rows[7].findAll('td')
	tc=cols[1].get_text()
	# print tc
	# col_value(rows)
	# print "**************"
##

## To get weather icon
resp = urllib2.urlopen('http://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm')
soup = BeautifulSoup(resp)
trs=[x['src'] for x in soup.findAll('img')]
icon_url = re.sub('../../', "http://www.cwb.gov.tw/V7/", trs[0])  
img = cStringIO.StringIO(urllib.urlopen(icon_url).read())

##	
root = Tk()
root.title("Temperature")
frame = Frame(root)
frame.pack()

t_label = Label(frame, text="Taichung City: {t} °c".format(t=tc), width="30", height="5")
t_label.pack(side = LEFT)


image = Image.open(img)
photo = ImageTk.PhotoImage(image)
background_label = Label(frame, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.pack()


root.mainloop()
