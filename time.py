# -*- coding: utf-8 -*- 
import os, sys, urllib, urllib2, cStringIO
from urllib2 import urlopen,Request
from bs4 import BeautifulSoup 
import sys
from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import re
from area import *

print area_t['Taipei_City']
print area_d['Taipei_City']

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

## To get temprature
def get_tc_t(area_t,area_d):
	resp = urllib2.urlopen('http://www.cwb.gov.tw/V7/observe/real/RealData_{}.htm'.format(area_d))
	soup = BeautifulSoup(resp)
	trs=soup.find_all('table',{"class" : "BoxTable"})
	for c in trs:
		## taichung temprature in row_7 col_1
		rows = c.findAll('tr')
		cols = rows[int(area_t)].findAll('td')
		tc=cols[1].get_text()
		# print tc
		# col_value(rows)
		# print "**************"
		return tc
##

## To get weather icon
def get_icon(county):
	resp = urllib2.urlopen('http://www.cwb.gov.tw/V7/forecast/taiwan/{}.htm'.format(county))
	soup = BeautifulSoup(resp)
	trs=[x['src'] for x in soup.findAll('img')]
	icon_url = re.sub('../../', "http://www.cwb.gov.tw/V7/", trs[0])  
	img = cStringIO.StringIO(urllib.urlopen(icon_url).read())
	return img
##

##SetSelect
def setSelect():
    # area.sort()
    select.delete(0,END)
    for name in area :
        select.insert(END,name)
##

## whichSelected
def whichSelected() :
    # print "At %s of %d" % (select.curselection(), len(area))
    return int(select.curselection()[0])
##

##
def change_icon():
	global background_label
	city_new = area[whichSelected()]
	img_now=get_icon(city_new)
	background_label.destroy()
	image = Image.open(img_now)
	photo = ImageTk.PhotoImage(image)
	background_label = Label(frame, image=photo)
	background_label.image=photo
	background_label.place(x=0, y=0, relwidth=1, relheight=1)
	background_label.pack(side = LEFT)
##

## build gui
root = Tk()
root.title("Temperature")
frame = Frame(root)
frame.pack()


city='Taichung_City'
#display temperature
tc_t=get_tc_t(area_t[city],area_d[city])
t_label = Label(frame, font=('times', 15, 'bold'), width="25", height="5")
t_label.config(text="{0}: {1} °c".format(city,tc_t))
t_label.pack(side = LEFT)
#display weather icon
img_o=get_icon(city)
image = Image.open(get_icon(city))
photo = ImageTk.PhotoImage(image)
background_label = Label(frame, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.pack(side = LEFT)
#display computer time
time1 = ''
clock = Label(root, font=('times', 20, 'bold'), bg='green')
clock.pack(fill=BOTH, expand=1)
#display listbox
lstbox = Frame(root)       # select of names
lstbox.pack()
scroll = Scrollbar(lstbox, orient=VERTICAL)
select = Listbox(lstbox, yscrollcommand=scroll.set, height=6)
scroll.config (command=select.yview)
scroll.pack(side=RIGHT, fill=Y)
select.pack(side=LEFT,  fill=BOTH, expand=1)
setSelect()

def load() :
	county = area[whichSelected()]
	t=get_tc_t(area_t[county],area_d[county])
	t_label.config(text="{0}: {1} °c".format(county,t))
	change_icon()
	print county

#display button
btn = Frame(root)       # Row of buttons
btn.pack()
b1 = Button(btn,text="Load",command=load)
b1.pack(side=LEFT)

start=0

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
	global city
	tc_now = get_tc_t(area_t[city],area_d[city])
	if tc_now != tc_t:
		tc_t = tc_now
		t_label.config(text="{c}: {t} °c".format(c=city,t=tc_t))
	t_label.after(60000, tick2)
	
	
	global background_label
	global start
	if start == 0 :
		start = 1
	else :
		change_icon()
	background_label.after(60000, tick2)
tick2()

root.mainloop()
