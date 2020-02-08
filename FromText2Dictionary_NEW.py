#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import Levenshtein
import os
# See if  ДополненияСловарю.csv  file is formated correctly. Fix errors.
print os.system('pluma ДополненияСловарю.csv')


from Tkinter import *
import tkFileDialog
from operator import itemgetter


top = Tk()
top.title("NewWords 2 Dictionary")
top.geometry('1000x1200+100+200')
tempvalue = StringVar(top,"temp")
global T
T=""
words = []

import operator
import codecs

# Functions definishions

def ReadDictionaries():
	global words
	print "ReadDictionaries"
	# ============= Read dictionaries to 
	# array  words[] - 3 columns: bad word, matching good word, length of bad word
	#
	with codecs.open("СЕВ_словарь.csv", "r", "utf-8") as f:
		for l in f:
			print l
			l=l.strip("\n")
			if l : words.append(l.split("	"))
	print "СЕВ_словарь.csv прочитан."
	with codecs.open("ДополненияСловарю.csv", "r", "utf-8") as f:
		for l in f:
			l=l.strip("\n")
			if l : words.append(l.split("	"))
	print "ДополненияСловарю.csv прочитаны"
	print " ======== Done read dictionaries to words[]"
	print "Длина words: ", len(words)
	print words[0]
	for tmp in words:
#		tmp[2] = int(tmp[2])
		if len(tmp) != 3: print tmp, "--number of elements in line is not 3-", tmp
	print "before last: ", words[-2] 
	print "last: ", words[-1] 
	for ww in words: ww[2]=len(ww[0])
	
#
#	adding "ИменаСобственные.csv"
	with codecs.open("ИменаСобственные.csv", "r", "utf-8") as f:
		for l in f:
	 		l=l.strip("\n")
			if l : words.append(l.split("	"))
	print "ИменаСобственные.csv прочитаны"
	print len(words)
	words = sorted(words, key=itemgetter(2,1,0))
	print "----------- Dictionary is sorted and ready! -----------"


def getfile(): # 
	print "getfile"
	# ========== если текст файл был открыт, сохранить.
	if T.compare("end-1c", "!=", "1.0"):  
		print "TEXT does exist"
		
	# 
	#============ открыть вновь выбранный файл. 
	original = tkFileDialog.askopenfile(title='Select a file',initialdir='/home/sergey/Data/storage/PrintedMaterials/ЕпархиальныеВедомости/СмоленскиеЕпархВед',filetypes = (('TEXT files','*.text'),('All files','*.*')))
	OT = original.read()
	T.delete("1.0",END)
	T.insert(END, OT)
	f_name=original.name
	f_name=f_name.replace('/home/sergey/Data/storage/PrintedMaterials/', '') # remove directory from filename
	L.configure(text=f_name) 
	#======================

def prove (txt):
	global words
	print words[0]
	words.sort(key=itemgetter(2), reverse=True)
#	for ww in words: print ww[0],"-----",ww[2]
	print words[0]
	print "Это был сортированый словарь"
	print "prove"
	txt=txt.replace(" ","")
	reducted = " " * len(txt)
	for ww_prove in words:
		if ww_prove[2] == 0: continue
		existing = ww_prove[0] # original word
		# ------------------------ Disable special symbols 
		print ww_prove
		for ch in [')','(','"','|','+','^',',',':','.',';']:
			if ch in existing:
				existing=existing.replace(ch,"\\"+ch)	
		# ------------------------ Special symbols disabled
		replacement=ww_prove[1] # replacement word
		ml=[] # list of matches
		matches = re.compile(existing, re.UNICODE) 
		for match in matches.finditer(txt): ml.insert(0,[match.start(),match.end()])
		for m in ml:
			# ------------------------
			txt = txt[0:m[0]] + txt[m[1]:] # строка txt до найденного + после найденного слова existing (найденное слово вырезается, backslash не учитывается) 
			reducted = reducted[0:m[0]] + reducted[m[1]:] # из строки reducted вырезается то же место что и в строке existing (чтобы строки были идентичны)
			txt = txt[0:m[0]] + " " + " " * len(replacement) + " " + txt[m[0]:] # в строке txt  вместо слова existing вставляются пробелы по числу букв в слове replacement
			reducted = reducted[0:m[0]] + " " + replacement + " " + reducted[m[0]:] # в строке reducted  вместо слова existing вставляются словo replacement
	# --------- Combining reducted words with unrecognized.
	print "words replaced"
	combined=""
	for i in range(0, len(txt)):
		if txt[i] == " ": 
			# print "reducted"
			combined = combined + reducted[i]
		else:
			combined = combined + txt[i]
			# print "txt"
	# --------- removing spaces before <dot> and <point> and adding space after if there is none.
	combined.replace(" .",".")
	combined.replace(" ,",",")
	combined.replace(" :",":")
	return combined

		
def T_oncopy(event):
	print "T_oncopy"
	# =========   Called on Ctrl <C> in TEXT window
	LB.delete(0,END) 
	E1.delete(0,END)
	E2.delete(0,END)
	new_word=event.widget.selection_get() # get selection from TEXT  
	new_word = new_word.replace(' ', '') # remove spaces
	E1.insert(END, new_word)
	print len(words)
	for one_word in words:
		# print one_word[0].encode("utf-8")
		ld = one_word[1] 
		one_word.append(Levenshtein.distance(new_word,ld))
		# print one_word[0]," ---- ",one_word[1]," ---- ", wone_word[2]
	print "2"
	words.sort(key=itemgetter(3))
	for item in words[:10]:
		print ld, type(ld), len(ld)
		print item
		LB.insert(END, item[1]) #.decode('utf-8', 'ignore'))
	for one_word in words:
		one_word.pop()
	#======================


def selectedE1(select):
	print "selectedE1"
	#======================
	E2.delete(0,END)
	E2.insert(END,E1.get())
	#======================

def selectedLB(select):
	print "selectedLB"
	#======================
	E2.delete(0,END)
	E2.insert(END,LB.get(LB.curselection()))
	#======================
	

def add2dictionary(event): # Adding new found word to dictionary. 
	print "add2dictionary"
	#======================
	t1 = E1.get() # existing word (ww[0])
	if not t1: return
	t2 = E2.get() # replacing word (ww[1])
	t3 = len(t1)
	if not t1: return
	new_word = [t1,t2,t3]	
	words.append(new_word) 	# adding new word to ДополненияСловарю.csv file
	with codecs.open("ДополненияСловарю.csv", "a", "utf-8") as myfile:
		strng=t1 + "	" + t2 +"	" + str(t3).encode("utf-8")+"\n"
		myfile.write (strng)
	E2.delete(0,END)
	E1.delete(0,END)
	LB.delete(0,END)
	ttxt = prove(T.get("0.1",END))
	T.delete("1.0",END)
	# print ttxt
	T.insert(END,ttxt)
	#======================



#===================================
# Main window widgets
#===================================

# --------  Create file menu
#
print "Here we go!"
menubar = Menu(top)
menubar.add_command(label="Open new file", command=getfile)
menubar.pack
top.config(menu=menubar)
L = Label(text="No file selected")
L.grid(row=1, column=0, columnspan=4)


# -------- TEXT - test box for analized text
#            
T = Text(top, height=36, width=80)
T.configure(font=("Times New Roman", 18))
T.grid(row=2,column=0,columnspan=4)
T.bind('<<Copy>>', T_oncopy)

# -------- Entry widget where found in TEXT word goes to
#
E1 = Entry(top, bd = 1)
E1.grid(row=0,column=0)
E1.bind("<Button-1>",selectedE1)

# -------- Listbox for words in dictionary similar to selected in text
#
LB = Listbox(top,exportselection=1)
LB.grid(row=0,column=1)
LB.bind("<<ListboxSelect>>",selectedLB)

# -------- Entry widget-2 where found word is reducted before goes to Dictionary
#
E2 = Entry(top, bd = 1)
E2.grid(row=0,column=2)

# -------- Button "Добавить в Словарь"
# 
B1=Button(top,text="Добавить в Словарь")
B1.grid(row=0,column=3)
B1.bind('<Button-1>',add2dictionary)

ReadDictionaries()

# ======================= Main loop =====================

top.mainloop()
