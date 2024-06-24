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
        self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeleteClient_form(),RIGHT)
        self.but_frame2=Frame(self.form.root)
        self.but_frame2.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_del=But(self.but_frame2,"Новый клиент",lambda:self.CreateClient_form(),LEFT)
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
        
class scene_device:
    def __init__(self):  
        self.form_device=Form("Устройства","1000x600")
        self.left_frame=Frame(self.form_device.root)
        self.left_frame.pack(side=LEFT)
        self.left_frame_top=Frame(self.left_frame)
        self.left_frame_top.pack(side=TOP)
        self.tree=ttk.Treeview(self.left_frame_top, columns=("Name","Description"), displaycolumns=(0,1), show="tree")
        self.tree.configure(height=28)
        self.tree.pack(side=LEFT,padx=4, pady=4, anchor="nw")
        self.tree.column("#0", stretch=True, anchor="w", width=60)
        self.tree.column("Name", stretch=False, anchor="w", width=200)
        self.scrl=Scrollbar(self.left_frame_top, command=self.tree.yview)
        self.scrl.pack(side=LEFT, fill=Y)
        self.tree.config(yscrollcommand=self.scrl.set) 
        self.Tree_Refresh()
        self.right_frame=Frame(self.form_device.root)
        self.right_frame.pack(side=RIGHT, padx=4,pady=4)
        self.tree.bind('<<TreeviewSelect>>',self.Detect_click)
        self.left_frame_bot=Frame(self.left_frame)
        self.left_frame_bot.pack(side=BOTTOM)
        self.but_new_client=But(self.left_frame_bot,"Новый клиент",lambda:self.CreateClient_form(),LEFT)
        self.but_new_folder=But(self.left_frame_bot,"Новая группа",lambda:self.CreateFolder_form(),LEFT)
        
        self.form_device.root.mainloop()
    
    def Tree_Refresh(self):
        self.tree.delete(*self.tree.get_children())
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT client_id, name FROM CLIENT""")
            self.clients_list=cursor.fetchall()
            for i in self.clients_list:
                lab0=self.tree.insert("","end","clt-"+str(i[0]), values=(i[1],""))
                cursor.execute("""SELECT folder_id, name FROM FOLDER WHERE client_id="""+str(i[0])+""" AND root_folder IS NULL""")
                self.folder0=cursor.fetchall()
                if self.folder0!=[]:
                    for j in self.folder0:
                        lab1=self.tree.insert(lab0,"end","fld-"+str(j[0]), values=(j[1],""))
                        cursor.execute("""SELECT folder_id, name FROM FOLDER WHERE root_folder="""+str(j[0]))
                        self.folder1=cursor.fetchall()
                        if self.folder1!=[]:
                            for k in self.folder1:
                                lab2=self.tree.insert(lab1,"end","fld-"+str(k[0]), values=(k[1],""))
            cursor.execute("""SELECT device_id, folder_id, name_user, IMEI FROM DEVICE""")
            self.device_list=cursor.fetchall()
            for i in self.device_list:
                lab_d=self.tree.insert("fld-"+str(i[1]),"end","dev-"+str(i[0]), values=(i[2],i[3]))
    
    def Detect_click(self,event):
        self.right_frame.destroy()
        self.right_frame=Frame(self.form_device.root)
        self.right_frame.pack(side=LEFT)
        self.curobject=self.tree.focus().split("-")
        if self.curobject[0]=="clt":
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""SELECT * FROM CLIENT WHERE client_id='"""+self.curobject[1]+"""'""")
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
            self.ent_id_client=Ent(self.right_frame,"ID клиента",self.client_id,TOP,justify="center")
            self.ent_id_client.block()
            self.ent_name_client=Ent(self.right_frame,"Название клиента",self.client_name,TOP)
            self.cmbx_rule=Cmbox(self.right_frame,"Максимальные права клиента",self.rules_list,TOP)
            self.cmbx_rule.set(self.client_rule_name)
            self.but_frame1=Frame(self.right_frame)
            self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
            self.but_save=But(self.but_frame1,"Сохранить",lambda:self.UpdateClient_form(),LEFT)
            self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeleteClient_form(),RIGHT)
            self.but_frame2=Frame(self.right_frame)
            self.but_frame2.pack(side=TOP, fill=X, padx=8, pady=10)
        elif self.curobject[0]=="fld":
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""SELECT * FROM FOLDER WHERE folder_id='"""+self.curobject[1]+"""'""")
                answear=cursor.fetchall()
                self.folder_id=answear[0][0]
                self.client_id=answear[0][1]
                self.root_folder=answear[0][2]
                self.folder_name=answear[0][3]
                self.ent_id_folder=Ent(self.right_frame,"ID папки",self.folder_id,TOP,justify="center")
                self.ent_id_folder.block()
                self.ent_name_folder=Ent(self.right_frame,"Название группы",self.folder_name,TOP)
                if self.root_folder==None:
                    cursor.execute("""SELECT name FROM CLIENT""")
                    answear=cursor.fetchall()
                    self.client_list=unpack(answear)
                    cursor.execute("""SELECT name FROM CLIENT WHERE client_id='"""+str(self.client_id)+"""'""")
                    answear=cursor.fetchall()
                    self.client_name=answear[0][0]
                    self.cmbx_folder=Cmbox(self.right_frame,"Клиент",self.client_list,TOP)
                    self.cmbx_folder.set(self.client_name)
                else:
                    cursor.execute("""SELECT name FROM FOLDER WHERE root_folder IS NULL""")
                    answear=cursor.fetchall()
                    self.folder1_list=unpack(answear)
                    cursor.execute("""SELECT name FROM FOLDER WHERE folder_id='"""+str(self.root_folder)+"""'""")
                    answear=cursor.fetchall()
                    self.root_folder_name=answear[0][0]
                    self.cmbx_folder=Cmbox(self.right_frame,"Группа",self.folder1_list,TOP)
                    self.cmbx_folder.set(self.root_folder_name)
            self.but_frame1=Frame(self.right_frame)
            self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
            self.but_save=But(self.but_frame1,"Сохранить",lambda:self.UpdateFolder_form(),LEFT)
            self.but_del=But(self.but_frame1,"Удалить",lambda:self.UpdateFolder_DB(),RIGHT)
        elif self.curobject[0]=="dev":
            pass
        
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
        
    def UpdateFolder_form(self):
        pass
    
    def UpdateFolder_DB(self):
        pass
    
    def DeleteClient_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM FOLDER WHERE client_id='"""+str(self.client_id)+"""'""")
            folder_list=cursor.fetchall()
            cursor.execute("""SELECT name FROM USER WHERE client_id='"""+str(self.client_id)+"""'""")
            user_list=cursor.fetchall()
        self.form_del=Toplevel()
        self.form_del.geometry("300x65")
        self.form_del.title("Удалить клиента")
        self.form_del.wait_visibility()
        self.form_del.grab_set_global()
        if folder_list == [] and user_list == []:        
            self.lab_del=Label(self.form_del, text="Вы точно хотите удалить клиента?")
            self.lab_del.pack(side=TOP)
            self.f_upd=Frame(self.form_del, width=200)
            self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
            self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeleteClient_DB(),LEFT)
            self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del.destroy(),RIGHT)
        else:
            self.lab_del=Label(self.form_del, text="Удаление невозможно, есть привязанные объекты")
            self.lab_del.pack(side=TOP)
            self.but_del_ok=But(self.form_del,"ОК",lambda:self.form_del.destroy(),TOP)
        self.form_del.mainloop()
        
    def DeleteClient_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""DELETE FROM CLIENT WHERE client_id='"""+str(self.client_id)+"""'""")
            con.commit()
        self.Tree_Refresh()
        self.form_del.destroy()
        
    def CreateClient_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM RULES""")
            self.rules_list=cursor.fetchall()
            self.rules_list=unpack(self.rules_list)
        self.form_new_client=Form("Создать клиента","300x300")
        self.new_name_client=Ent(self.form_new_client.root,"Название клиента","",TOP)
        self.new_cmbx_rule=Cmbox(self.form_new_client.root,"Максимальные права клиента",self.rules_list,TOP)
        self.but_frame_create_client1=Frame(self.form_new_client.root)
        self.but_frame_create_client1.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save_new_client=But(self.but_frame_create_client1,"Сохранить",lambda:self.CreateClient_DB(),LEFT)
        self.but_cancel_new_client=But(self.but_frame_create_client1,"Отмена",lambda:self.form_new_client.root.destroy(),RIGHT)
        
    def CreateClient_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT rule_id FROM RULES WHERE name='"""+str(self.new_cmbx_rule.get())+"""'""")
            answear=cursor.fetchall()
            cursor.execute("""INSERT INTO CLIENT (name,rule_id) VALUES ('"""+self.new_name_client.get()+"""','"""+str(answear[0][0])+"""')""")
            con.commit()
        self.Tree_Refresh()
        self.form_new_client.root.destroy()
        
    def CreateFolder_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM CLIENT""")
            self.client_list=cursor.fetchall()
            self.client_list=unpack(self.client_list)
        self.form_new_folder=Form("Создать папку","300x300")
        self.new_name_folder=Ent(self.form_new_folder.root,"Название папки","",TOP)
        self.new_cmbx_folder=Cmbox(self.form_new_folder.root,"Клиент",self.client_list,TOP)
        try:
            self.new_cmbx_folder.set(self.ent_name_client.get())
        except:
            self.new_cmbx_folder.set(self.client_list[0])
        self.but_frame_create_folder1=Frame(self.form_new_folder.root)
        self.but_frame_create_folder1.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save_new_folder=But(self.but_frame_create_folder1,"Сохранить",lambda:self.CreateFolder_DB(),LEFT)
        self.but_cancel_new_folder=But(self.but_frame_create_folder1,"Отмена",lambda:self.form_new_folder.root.destroy(),RIGHT)
        
    def CreateFolder_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT client_id FROM CLIENT WHERE name='"""+str(self.new_cmbx_folder.get())+"""'""")
            answear=cursor.fetchall()
            cursor.execute("""INSERT INTO FOLDER (name,client_id) VALUES ('"""+self.new_name_folder.get()+"""','"""+str(answear[0][0])+"""')""")
            con.commit()
        self.Tree_Refresh()
        self.form_new_folder.root.destroy()
        
        
        
m=scene_device()