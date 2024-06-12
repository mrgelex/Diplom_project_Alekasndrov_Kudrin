from tkinter import *
from tkinter import ttk
import sqlite3 as sl
from threading import Thread
import socket

pathDB='Logs.db'

class Form:
    def __init__(self,name_form,geom):
        self.root=Tk()
        self.root.title(name_form)
        self.root.geometry(geom)
        
class Entry_1:
    def __init__(self, form, label, data, packside):
        self.lab_1=Label(form, text=label)
        self.ent_1=Entry(form)
        self.lab_1.pack(side=packside)
        self.ent_1.pack(side=packside)
        self.ent_1.insert(0,data)
    def get_1(self):
        return self.ent_1.get()
    def set_1(self,d):
        self.ent_1.delete(0,END)
        self.ent_1.insert(0,d)
        
class Button_1:
    def __init__(self, form, txt, com, packside):
        self.but_1=Button(form, text=txt)
        self.but_1.config(command=com)
        self.but_1.pack(side=packside)
        
class Box_1:
    def __init__(self, form, h, w, data):
        self.bx_1=Listbox(form, selectmode=SINGLE, height=h, width=w) 
        self.bx_1.pack(side=LEFT)
        self.bx_1.bind('<<ListboxSelect>>',self.Select)
        self.scrl=Scrollbar(form, command=self.bx_1.yview)
        self.scrl.pack(side=LEFT, fill=Y)
        self.bx_1.config(yscrollcommand=self.scrl.set) 
        self.Refresh(data)     
    def Return_index(self):
        cursel=self.bx_1.curselection()
        return cursel[0]
    def Refresh(self, data):
        self.bx_1.delete(0,END)
        i=0 
        for str in data:
            self.bx_1.insert(i,str)
            i+=1 
    def Select(self,event):
        print(self.bx_1.curselection())
             
class Combobox_1:
    def __init__(self, form, label, data, packside):
        self.lab_1=Label(form, text=label)
        self.lab_1.pack(side=packside)
        self.cmbx_1=ttk.Combobox(form, values=data, state="readonly")
        self.cmbx_1.pack(side=packside)
    def get_1(self):
        return self.cmbx_1.get()
    def set_1(self, data):
        self.cmbx_1.set(data)
     
        
class main_window:
    def __init__(self):
        self.form=Form("TM Debit-E","400x400")
        self.box=Box_1(self.form.root,"20","40",["1","2","3"])
        self.Entry=Entry_1(self.form.root,"ID клиента","",TOP)
        self.form.root.mainloop()
        
m=main_window()