from tkinter import *
from tkinter import ttk
import sqlite3 as sl
from threading import Thread
import socket

pathDB='Logs.db'

def unpack(data):
    ln=len(data)
    for i in range(ln):
        data[i]=data[i][0]
    return data

class Form:
    def __init__(self,name_form,geom):
        self.root=Tk()
        self.root.title(name_form)
        self.root.geometry(geom)
        self.root.resizable(width=False, height=False)
        
class Ent:
    def __init__(self, form, label, data, packside, justify="left"):
        self.label=Label(form, text=label)
        self.entry=Entry(form, justify=justify, width="40")
        self.label.pack(side=packside)
        self.entry.pack(side=packside)
        self.entry.insert(0,data)
    def get(self):
        return self.entry.get()
    def set(self,d):
        self.entry.delete(0,END)
        self.entry.insert(0,d)
    def block(self):
        self.entry.config(state="readonly")
    def unblock(self):
        self.entry.config(state="normal")
        
class But:
    def __init__(self, form, txt, com, packside):
        self.but=Button(form, text=txt)
        self.but.config(command=com)
        self.but.pack(side=packside)
        
class Box:
    def __init__(self, form, h, w, data):
        self.box=Listbox(form, selectmode=SINGLE, height=h, width=w) 
        self.box.pack(side=LEFT)
        self.scrl=Scrollbar(form, command=self.box.yview)
        self.scrl.pack(side=LEFT, fill=Y)
        self.box.config(yscrollcommand=self.scrl.set) 
        self.Refresh(data)     
    def Return_index(self):
        cursel=self.box.curselection()
        return cursel[0]
    def Refresh(self, data):
        self.box.delete(0,END)
        i=0 
        for str in data:
            self.box.insert(i,str)
            i+=1    
             
class Cmbox:
    def __init__(self, form, label, data, packside):
        self.lab=Label(form, text=label)
        self.lab.pack(side=packside)
        self.cmbx=ttk.Combobox(form, values=data, state="readonly", width="37")
        self.cmbx.pack(side=packside)
    def get(self):
        return self.cmbx.get()
    def set(self, data):
        self.cmbx.set(data)
     
        
class main_window:
    def __init__(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM CLIENT""")
            self.clients_list=cursor.fetchall()
            self.clients_list=unpack(self.clients_list)
            cursor.execute("""SELECT * FROM CLIENT WHERE name='"""+self.clients_list[0]+"""'""")
            answear=cursor.fetchall()
            self.client_id=answear[0][0]
            self.client_name=answear[0][1]
            self.client_rule=answear[0][2]
            cursor.execute("""SELECT name FROM RULES""")
            self.rules_list=cursor.fetchall()
            self.rules_list=unpack(self.rules_list)
            cursor.execute("""SELECT name FROM RULES WHERE rule_id='"""+str(self.client_rule)+"""'""")
            answear=cursor.fetchall()
            self.client_rule_name=answear[0][0]
        self.form=Form("TM Debit-E","520x400")
        self.box=Box(self.form.root,"25","40",self.clients_list)
        self.box.box.bind('<<ListboxSelect>>',self.Select)
        self.ent_id_client=Ent(self.form.root,"ID клиента",self.client_id,TOP,justify="center")
        self.ent_id_client.block()
        self.ent_name_client=Ent(self.form.root,"Название клиента",self.client_name,TOP)
        self.cmbx_rule=Cmbox(self.form.root,"Максимальные права клиента",self.rules_list,TOP)
        self.cmbx_rule.set(self.client_rule_name)
        self.but_frame1=Frame(self.form.root)
        self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save=But(self.but_frame1,"Сохранить",lambda:self.UpdateClient_form(),LEFT)
        self.form.root.mainloop()
        
    def Select(self, event):
        if self.box.box.curselection()!=():
            self.client_name=self.clients_list[self.box.box.curselection()[0]]
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""SELECT * FROM CLIENT WHERE name='"""+self.client_name+"""'""")
                answear=cursor.fetchall()
                self.client_id=answear[0][0]
                self.client_name=answear[0][1]
                self.client_rule=answear[0][2]
                cursor.execute("""SELECT name FROM RULES WHERE rule_id='"""+str(self.client_rule)+"""'""")
                answear=cursor.fetchall()
                self.client_rule_name=answear[0][0]
            self.ent_id_client.unblock()
            self.ent_id_client.set(self.client_id)
            self.ent_id_client.block()
            self.ent_name_client.set(self.client_name)
            self.cmbx_rule.set(self.client_rule_name)
     
    def UpdateClient_form(self):
        self.form_upd=Toplevel()
        self.form_upd.geometry("250x65")
        self.form_upd.title("Сохранить изменения")
        self.form_upd.wait_visibility()
        self.form_upd.grab_set_global()
        self.lab_upd=Label(self.form_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.UpdateClient_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_upd.destroy(),RIGHT)
        self.form_upd.mainloop()
            
    def UpdateClient_DB(self):
        self.client_id=self.ent_id_client.get()
        self.client_name=self.ent_name_client.get()
        self.client_rule_name=self.cmbx_rule.get()
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT rule_id FROM RULES WHERE name='"""+str(self.client_rule_name)+"""'""")
            answear=cursor.fetchall()
            self.client_rule=answear[0][0]
            cursor.execute("""UPDATE CLIENT SET name='"""+self.client_name+"""',rule_id='"""+str(self.client_rule)+"""' WHERE client_id="""+str(self.client_id))
            con.commit()
        self.form_upd.destroy()
        
m=main_window()