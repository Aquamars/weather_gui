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
tmp_time=time.strftime('%m/%d %H:%M:%S', time.localtime(t))
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
def get_tc_t():
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
		return tc
##

## To get weather icon
def get_icon():
	resp = urllib2.urlopen('http://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm')
	soup = BeautifulSoup(resp)
	trs=[x['src'] for x in soup.findAll('img')]
	icon_url = re.sub('../../', "http://www.cwb.gov.tw/V7/", trs[0])  
	img = cStringIO.StringIO(urllib.urlopen(icon_url).read())
	return img
##

## build gui
root = Tk()
root.title("Temperature")
frame = Frame(root)
frame.pack()

#display temperature
tc_t=get_tc_t()
t_label = Label(frame, font=('times', 15, 'bold'), width="25", height="5")
t_label.config(text="Taichung City: {t} °c".format(t=tc_t))
t_label.pack(side = LEFT)
#display weather icon
img_o=get_icon()
image = Image.open(get_icon())
photo = ImageTk.PhotoImage(image)
background_label = Label(frame, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.pack(side = LEFT)
#display computer time
time1 = ''
clock = Label(root, font=('times', 20, 'bold'), bg='green')
clock.pack(fill=BOTH, expand=1)

#Dynamic time
def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed 
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)
tick()
#Dynamic temperature & icon
def tick2():
	global tc_t
	tc_now = get_tc_t()
	if tc_now != tc_t:
		tc_t = tc_now
		t_label.config(text="Taichung City: {t} °c".format(t=tc_t))
	t_label.after(60000, tick2)
	
	global img_o
	img_now=get_icon()
	if img_now != img_o:
		img_o = img_now
		image = Image.open(img_o)
		photo = ImageTk.PhotoImage(image)
		background_label.config = Label(image=photo)
	# background_label.after(60000, tick2)
tick2()

root.mainloop()
