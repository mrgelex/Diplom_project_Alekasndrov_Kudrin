from tkinter import *
from tkinter import ttk
import sqlite3 as sl
from threading import Thread
from web_interface.startweb import startweb
import server

pathDB='web_interface/Logs.db'

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
        if data:
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
        self.form=Form("TM Debit-E","800x400")
        self.lframe=Frame(self.form.root)
        self.lframe.pack(side=LEFT)
        self.rframe=Frame(self.form.root)
        self.rframe.pack(side=RIGHT)
        self.text=Text(self.lframe, wrap="word")
        self.text.pack(side=LEFT)
        self.text_scrl=Scrollbar(self.lframe, command=self.text.yview)
        self.text_scrl.pack(side=LEFT, fill=Y)
        self.text.config(yscrollcommand=self.text_scrl.set) 
        self.serv=server.Server(self.text)
        self.but_device=But(self.rframe,"Устройства",lambda:scene_device(),TOP)
        self.but_perm=But(self.rframe,"Права доступа",lambda:scene_perm("all",0),TOP)
        self.but_user=But(self.rframe,"Пользователи",lambda:scene_user(),TOP)
        self.but_run_server=But(self.rframe,"Запустить сервер",lambda:self.serv.Start(),TOP)
        self.but_stop_server=But(self.rframe,"Остановить сервер",lambda:self.serv.Stop(),TOP)
        self.but_start_web=But(self.rframe,"Запустить web",lambda:self.RunServer(),TOP)
        self.form.root.mainloop()
        
    def RunServer(self):
        self.th2=Thread(target=startweb)
        self.th2.daemon=True
        self.th2.start()
        
class scene_device:
    def __init__(self):  
        self.form_device=Form("Устройства","750x650")
        self.left_frame=Frame(self.form_device.root)
        self.left_frame.pack(side=LEFT)
        self.left_frame_top=Frame(self.left_frame)
        self.left_frame_top.pack(side=TOP)
        self.tree=ttk.Treeview(self.left_frame_top, columns=("Name","Description"), displaycolumns=(0,1), show="tree")
        self.tree.configure(height=30)
        self.tree.pack(side=LEFT,padx=4, pady=4, anchor="nw")
        self.tree.column("#0", stretch=True, anchor="w", width=60)
        self.tree.column("Name", stretch=False, anchor="w", width=200)
        self.scrl=Scrollbar(self.left_frame_top, command=self.tree.yview)
        self.scrl.pack(side=LEFT, fill=Y)
        self.tree.config(yscrollcommand=self.scrl.set) 
        self.Tree_Refresh()
        self.right_frame=Frame(self.form_device.root)
        self.right_frame.pack(side=LEFT, padx=4,pady=4)
        self.tree.bind('<<TreeviewSelect>>',self.Detect_click)
        self.left_frame_bot=Frame(self.left_frame)
        self.left_frame_bot.pack(side=BOTTOM)
        self.but_new_client=But(self.left_frame_bot,"Новый клиент",lambda:self.CreateClient_form(),LEFT)
        self.but_new_folder=But(self.left_frame_bot,"Новая группа",lambda:self.CreateFolder_form(),LEFT)
        self.but_new_subfolder=But(self.left_frame_bot,"Новая подгруппа",lambda:self.CreateSubFolder_form(),LEFT)
        self.but_new_device=But(self.left_frame_bot,"Новое устройство",lambda:self.CreateDevice_form(),LEFT)
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
            cursor.execute("""SELECT folder_id, client_id, name FROM FOLDER WHERE root_folder IS NULL""")
            self.folder0=cursor.fetchall()
            if self.folder0!=[]:
                for i in self.folder0:
                    lab1=self.tree.insert("clt-"+str(i[1]),"end","fld-"+str(i[0]), values=(i[2],""))
            cursor.execute("""SELECT folder_id, root_folder, name FROM FOLDER WHERE root_folder IS NOT NULL""")
            self.folder1=cursor.fetchall()
            if self.folder1!=[]:
                for i in self.folder1:
                    lab2=self.tree.insert("fld-"+str(i[1]),"end","fld-"+str(i[0]), values=(i[2],""))
            cursor.execute("""SELECT device_id, folder_id, name_user, IMEI FROM DEVICE""")
            self.device_list=cursor.fetchall()
            if self.device_list!=[]:
                for i in self.device_list:
                    lab_d=self.tree.insert("fld-"+str(i[1]),"end","dev-"+str(i[0]), values=(i[2],i[3]))
    
    def Detect_click(self,event):
        self.curobject=self.tree.focus().split("-")
        if not self.curobject:
            return
        self.right_frame.destroy()
        self.right_frame=Frame(self.form_device.root)
        self.right_frame.pack(side=LEFT, padx=4,pady=4)
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
            self.but_showperm=But(self.but_frame1,"Доступ",lambda:scene_perm("client",self.client_id),BOTTOM)
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
                if self.root_folder==None:
                    self.folder_name=answear[0][3]
                    self.ent_id_folder=Ent(self.right_frame,"ID группы",self.folder_id,TOP,justify="center")
                    self.ent_id_folder.block()
                    self.ent_name_folder=Ent(self.right_frame,"Название группы",self.folder_name,TOP)
                    cursor.execute("""SELECT name FROM CLIENT""")
                    answear=cursor.fetchall()
                    self.client_list=unpack(answear)
                    cursor.execute("""SELECT name FROM CLIENT WHERE client_id='"""+str(self.client_id)+"""'""")
                    answear=cursor.fetchall()
                    self.client_name=answear[0][0]
                    self.cmbx_folder=Cmbox(self.right_frame,"Клиент",self.client_list,TOP)
                    self.cmbx_folder.set(self.client_name)
                else:
                    self.subfolder_name=answear[0][3]
                    self.ent_id_folder=Ent(self.right_frame,"ID подгруппы",self.folder_id,TOP,justify="center")
                    self.ent_id_folder.block()
                    self.ent_name_subfolder=Ent(self.right_frame,"Название подгруппы",self.folder_name,TOP)
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
            self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeleteFolder_form(),RIGHT)
            self.but_showperm=But(self.but_frame1,"Доступ",lambda:scene_perm("folder",self.folder_id),BOTTOM)
        elif self.curobject[0]=="dev":
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""SELECT * FROM DEVICE WHERE device_id='"""+self.curobject[1]+"""'""")
                answear=cursor.fetchall()
                self.device_id=answear[0][0]
                self.device_folder_id=answear[0][1]
                self.device_name_user=answear[0][2]
                self.device_IMEI=answear[0][3]
                self.device_description=answear[0][4]
                self.device_IP=answear[0][5]
                self.device_port=answear[0][6]
                self.device_modbus_over_tcp=answear[0][7]
                self.device_add_pr200=answear[0][8]
                self.device_add_tr16=answear[0][9]
                self.device_add_inv=answear[0][10]
                self.device_type_inv=answear[0][11]
                self.device_GMT=answear[0][12]
                self.device_en=answear[0][13]
                cursor.execute("""SELECT name FROM FOLDER WHERE root_folder IS NOT NULL""")
                answear=cursor.fetchall()
                self.device_folder_list=unpack(answear)
                cursor.execute("""SELECT name FROM FOLDER WHERE folder_id='"""+str(self.device_folder_id)+"""'""")
                answear=cursor.fetchall()
                self.device_folder_name=answear[0][0]
            self.ent_device_id=Ent(self.right_frame,"ID устройства",self.device_id,TOP,justify="center")
            self.ent_device_id.block()
            self.cmbx_folder=Cmbox(self.right_frame,"Подруппа",self.device_folder_list,TOP)
            self.cmbx_folder.set(self.device_folder_name)
            self.ent_device_name_user=Ent(self.right_frame,"Пользовательское имя",self.device_name_user,TOP,justify="center")
            self.ent_device_IMEI=Ent(self.right_frame,"IMEI",self.device_IMEI,TOP,justify="center")
            self.ent_device_description=Ent(self.right_frame,"Описание",self.device_description,TOP,justify="center")
            self.ent_device_IP=Ent(self.right_frame,"IP",self.device_IP,TOP,justify="center")
            self.ent_device_port=Ent(self.right_frame,"Порт",self.device_port,TOP,justify="center")
            self.mb_list=("true","false")
            self.ent_device_modbus_over_tcp=Cmbox(self.right_frame,"Modbus over TCP",self.mb_list,TOP)
            self.ent_device_modbus_over_tcp.set(self.device_modbus_over_tcp)
            self.ent_device_add_pr200=Ent(self.right_frame,"Адрес ПР200",self.device_add_pr200,TOP,justify="center")
            self.ent_device_add_tr16=Ent(self.right_frame,"Адрес ТР16",self.device_add_tr16,TOP,justify="center")
            self.ent_device_add_inv=Ent(self.right_frame,"Адрес ПЧВ",self.device_add_inv,TOP,justify="center")
            self.INV_list=("danfoss","INVT")
            self.ent_device_type_inv=Cmbox(self.right_frame,"Тип ПЧВ",self.INV_list,TOP)
            self.ent_device_type_inv.set(self.device_type_inv)
            self.GMT_list=("+13","+12","+11","+10","+9","+8","+7","+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6","-7","-8","-9","-10","-11","-12")
            self.ent_device_GMT=Cmbox(self.right_frame,"Часовой пояс",self.GMT_list,TOP)
            self.ent_device_GMT.set(self.device_GMT)
            self.en_list=("true","false")
            self.ent_device_en=Cmbox(self.right_frame,"Enable",self.en_list,TOP)
            self.ent_device_en.set(self.device_en)
            self.but_frame1=Frame(self.right_frame)
            self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
            self.but_save=But(self.but_frame1,"Сохранить",lambda:self.UpdateDevice_form(),LEFT)
            self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeleteDevice_form(),RIGHT)
        
    def UpdateClient_form(self):
        self.form_client_upd=Toplevel()
        self.form_client_upd.geometry("250x65")
        self.form_client_upd.title("Сохранить изменения")
        self.form_client_upd.wait_visibility()
        self.form_client_upd.grab_set_global()
        self.lab_upd=Label(self.form_client_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_client_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.UpdateClient_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_client_upd.destroy(),RIGHT)
        self.form_client_upd.mainloop()
            
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
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""UPDATE CLIENT SET name='"""+self.client_name+"""',rule_id='"""+str(self.client_rule)+"""' WHERE client_id="""+str(self.client_id))
            con.commit()
        self.Tree_Refresh()
        self.form_client_upd.destroy()
        
    def UpdateFolder_form(self):
        self.form_folder_upd=Toplevel()
        self.form_folder_upd.geometry("250x65")
        self.form_folder_upd.title("Сохранить изменения")
        self.form_folder_upd.wait_visibility()
        self.form_folder_upd.grab_set_global()
        self.lab_upd=Label(self.form_folder_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_folder_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.UpdateFolder_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_folder_upd.destroy(),RIGHT)
        self.form_folder_upd.mainloop()
    
    def UpdateFolder_DB(self):
        self.folder_id=self.ent_id_folder.get()
        self.folder_name=self.ent_name_folder.get()
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            if self.root_folder==None:
                self.client_name=self.cmbx_folder.get()
                cursor.execute("""SELECT client_id FROM CLIENT WHERE name='"""+str(self.client_name)+"""'""")
                answear=cursor.fetchall()
                self.client_id=answear[0][0]
                cursor.execute("""PRAGMA foreign_keys = ON;""")
                cursor.execute("""UPDATE FOLDER SET name='"""+self.folder_name+"""',client_id='"""+str(self.client_id)+"""' WHERE folder_id="""+str(self.folder_id))
                con.commit()
            else:
                self.name_root_folder=self.cmbx_folder.get()
                cursor.execute("""SELECT folder_id FROM FOLDER WHERE name='"""+str(self.name_root_folder)+"""'""")
                answear=cursor.fetchall()
                self.root_folder=answear[0][0]
                cursor.execute("""PRAGMA foreign_keys = ON;""")
                cursor.execute("""UPDATE FOLDER SET name='"""+self.folder_name+"""',root_folder='"""+str(self.root_folder)+"""' WHERE folder_id="""+str(self.folder_id))
                con.commit()
        self.Tree_Refresh()
        self.form_folder_upd.destroy()
    
    def UpdateDevice_form(self):
        self.form_device_upd=Toplevel()
        self.form_device_upd.geometry("250x65")
        self.form_device_upd.title("Сохранить изменения")
        self.form_device_upd.wait_visibility()
        self.form_device_upd.grab_set_global()
        self.lab_upd=Label(self.form_device_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_device_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.UpdateDevice_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_device_upd.destroy(),RIGHT)
        self.form_device_upd.mainloop()
    
    def UpdateDevice_DB(self):
        self.device_id=self.ent_device_id.get()
        self.device_folder_name=self.cmbx_folder.get()
        self.device_name_user=self.ent_device_name_user.get()
        self.device_IMEI=self.ent_device_IMEI.get()
        self.device_description=self.ent_device_description.get()
        self.device_IP=self.ent_device_IP.get()
        self.device_port=self.ent_device_port.get()
        self.device_modbus_over_tcp=self.ent_device_modbus_over_tcp.get()
        self.device_add_pr200=self.ent_device_add_pr200.get()
        self.device_add_tr16=self.ent_device_add_tr16.get()
        self.device_add_inv=self.ent_device_add_inv.get()
        self.device_type_inv=self.ent_device_type_inv.get()
        self.device_GMT=self.ent_device_GMT.get()
        self.device_en=self.ent_device_en.get()
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT folder_id FROM FOLDER WHERE name='"""+str(self.device_folder_name)+"""'""")
            answear=cursor.fetchall()
            self.device_folder_id=answear[0][0]
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""UPDATE DEVICE SET folder_id='"""+str(self.device_folder_id)+"""', name_user='"""+str(self.device_name_user)+"""', 
                           IMEI='"""+str(self.device_IMEI)+"""', description='"""+str(self.device_description)+"""', 
                           IP='"""+str(self.device_IP)+"""', port='"""+str(self.device_port)+"""', 
                           modbus_over_tcp='"""+str(self.device_modbus_over_tcp)+"""', add_pr200='"""+str(self.device_add_pr200)+"""', 
                           add_tr16='"""+str(self.device_add_tr16)+"""', add_inv='"""+str(self.device_add_inv)+"""', 
                           type_inv='"""+str(self.device_type_inv)+"""', GMT='"""+str(self.device_GMT)+"""', 
                           enable='"""+str(self.device_en)+"""' WHERE device_id="""+str(self.device_id))
            con.commit()
        self.Tree_Refresh()
        self.form_device_upd.destroy()
    
    def DeleteClient_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM FOLDER WHERE client_id='"""+str(self.client_id)+"""'""")
            folder_list=cursor.fetchall()
            cursor.execute("""SELECT name FROM USER WHERE client_id='"""+str(self.client_id)+"""'""")
            user_list=cursor.fetchall()
        self.form_del_client=Toplevel()
        self.form_del_client.geometry("300x65")
        self.form_del_client.title("Удалить клиента")
        self.form_del_client.wait_visibility()
        self.form_del_client.grab_set_global()
        if folder_list == [] and user_list == []:        
            self.lab_del=Label(self.form_del_client, text="Вы точно хотите удалить клиента?")
            self.lab_del.pack(side=TOP)
            self.f_upd=Frame(self.form_del_client, width=200)
            self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
            self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeleteClient_DB(),LEFT)
            self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del_client.destroy(),RIGHT)
        else:
            self.lab_del=Label(self.form_del_client, text="Удаление невозможно, есть привязанные объекты")
            self.lab_del.pack(side=TOP)
            self.but_del_ok=But(self.form_del_client,"ОК",lambda:self.form_del_client.destroy(),TOP)
        self.form_del_client.mainloop()
        
    def DeleteClient_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""DELETE FROM CLIENT WHERE client_id='"""+str(self.client_id)+"""'""")
            con.commit()
        self.Tree_Refresh()
        self.form_del_client.destroy()
        
    def DeleteFolder_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            if self.root_folder==None:
                cursor.execute("""SELECT folder_id FROM FOLDER WHERE root_folder='"""+str(self.folder_id)+"""'""")
                client_list=cursor.fetchall()
                device_list=[]
            else:
                cursor.execute("""SELECT device_id FROM DEVICE WHERE folder_id='"""+str(self.folder_id)+"""'""")
                device_list=cursor.fetchall()
                client_list=[]
        self.form_del_folder=Toplevel()
        self.form_del_folder.geometry("300x65")
        self.form_del_folder.title("Удалить группу")
        self.form_del_folder.wait_visibility()
        self.form_del_folder.grab_set_global()
        if device_list == [] and client_list == []:        
            self.lab_del=Label(self.form_del_folder, text="Вы точно хотите удалить группу?")
            self.lab_del.pack(side=TOP)
            self.f_upd=Frame(self.form_del_folder, width=200)
            self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
            self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeleteFolder_DB(),LEFT)
            self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del_folder.destroy(),RIGHT)
        else:
            self.lab_del=Label(self.form_del_folder, text="Удаление невозможно, есть привязанные объекты")
            self.lab_del.pack(side=TOP)
            self.but_del_ok=But(self.form_del_folder,"ОК",lambda:self.form_del_folder.destroy(),TOP)
        self.form_del_folder.mainloop()
    
    def DeleteFolder_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""DELETE FROM FOLDER WHERE folder_id='"""+str(self.folder_id)+"""'""")
            con.commit()
        self.Tree_Refresh()
        self.form_del_folder.destroy()
    
    def DeleteDevice_form(self):
        self.form_del_device=Toplevel()
        self.form_del_device.geometry("300x65")
        self.form_del_device.title("Удалить устройство")
        self.form_del_device.wait_visibility()
        self.form_del_device.grab_set_global()   
        self.lab_del=Label(self.form_del_device, text="Вы точно хотите удалить устройство?")
        self.lab_del.pack(side=TOP)
        self.f_upd=Frame(self.form_del_device, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeleteDevice_DB(),LEFT)
        self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del_device.destroy(),RIGHT)
        self.form_del_device.mainloop()
    
    def DeleteDevice_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""DELETE FROM DEVICE WHERE device_id='"""+str(self.device_id)+"""'""")
            con.commit()
        self.Tree_Refresh()
        self.form_del_device.destroy()
        
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
        self.form_new_folder=Form("Создать группу","300x300")
        self.new_name_folder=Ent(self.form_new_folder.root,"Название группы","",TOP)
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
        
    def CreateSubFolder_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM FOLDER WHERE root_folder IS NULL""")
            answear=cursor.fetchall()
            self.root_folder_list=unpack(answear)
        self.form_new_subfolder=Form("Создать подгруппу","300x300")
        self.new_name_subfolder=Ent(self.form_new_subfolder.root,"Название подгруппы","",TOP)
        self.new_cmbx_subfolder=Cmbox(self.form_new_subfolder.root,"Группа",self.root_folder_list,TOP)
        try:
            self.new_cmbx_subfolder.set(self.ent_name_folder.get())
        except:
            self.new_cmbx_subfolder.set(self.root_folder_list[0])
        self.but_frame_create_subfolder1=Frame(self.form_new_subfolder.root)
        self.but_frame_create_subfolder1.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save_new_folder=But(self.but_frame_create_subfolder1,"Сохранить",lambda:self.CreateSubFolder_DB(),LEFT)
        self.but_cancel_new_folder=But(self.but_frame_create_subfolder1,"Отмена",lambda:self.form_new_subfolder.root.destroy(),RIGHT)
        
    def CreateSubFolder_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT folder_id FROM FOLDER WHERE name='"""+str(self.new_cmbx_subfolder.get())+"""'""")
            answear=cursor.fetchall()
            cursor.execute("""INSERT INTO FOLDER (name,root_folder) VALUES ('"""+self.new_name_subfolder.get()+"""','"""+str(answear[0][0])+"""')""")
            con.commit()
        self.Tree_Refresh()
        self.form_new_subfolder.root.destroy()
    
    def CreateDevice_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM FOLDER WHERE root_folder IS NOT NULL""")
            answear=cursor.fetchall()
            self.subfolder_list=unpack(answear)
        self.form_new_device=Form("Создать устройство","300x550")
        self.new_cmbx_device=Cmbox(self.form_new_device.root,"Подруппа",self.subfolder_list,TOP)
        try:
            self.new_cmbx_device.set(self.subfolder_name)
        except:
            self.new_cmbx_device.set(self.subfolder_list[0])
        self.new_device_name_user=Ent(self.form_new_device.root,"Пользовательское имя","",TOP,justify="center")
        self.new_device_IMEI=Ent(self.form_new_device.root,"IMEI","",TOP,justify="center")
        self.new_device_description=Ent(self.form_new_device.root,"Описание","",TOP,justify="center")
        self.new_device_IP=Ent(self.form_new_device.root,"IP","127.0.0.1",TOP,justify="center")
        self.new_device_port=Ent(self.form_new_device.root,"Порт","",TOP,justify="center")
        self.mb_list=("true","false")
        self.new_device_modbus_over_tcp=Cmbox(self.form_new_device.root,"Modbus over TCP",self.mb_list,TOP)
        self.new_device_modbus_over_tcp.set(self.mb_list[0])
        self.new_device_add_pr200=Ent(self.form_new_device.root,"Адрес ПР200","10",TOP,justify="center")
        self.new_device_add_tr16=Ent(self.form_new_device.root,"Адрес ТР16","16",TOP,justify="center")
        self.new_device_add_inv=Ent(self.form_new_device.root,"Адрес ПЧВ","1",TOP,justify="center")
        self.INV_list=("danfoss","INVT")
        self.new_device_type_inv=Cmbox(self.form_new_device.root,"Тип ПЧВ",self.INV_list,TOP)
        self.new_device_type_inv.set(self.INV_list[0])
        self.GMT_list=("+13","+12","+11","+10","+9","+8","+7","+6","+5","+4","+3","+2","+1","0","-1","-2","-3","-4","-5","-6","-7","-8","-9","-10","-11","-12")
        self.new_device_GMT=Cmbox(self.form_new_device.root,"Часовой пояс",self.GMT_list,TOP)
        self.new_device_GMT.set("+3")
        self.en_list=("true","false")
        self.new_device_en=Cmbox(self.form_new_device.root,"Enable",self.en_list,TOP)
        self.new_device_en.set("True")
        self.but_frame_create_device=Frame(self.form_new_device.root)
        self.but_frame_create_device.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save_new_folder=But(self.but_frame_create_device,"Сохранить",lambda:self.CreateDevice_DB(),LEFT)
        self.but_cancel_new_folder=But(self.but_frame_create_device,"Отмена",lambda:self.form_new_device.root.destroy(),RIGHT)
    
    def CreateDevice_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT folder_id FROM FOLDER WHERE name='"""+str(self.new_cmbx_device.get())+"""'""")
            answear=cursor.fetchall()
            cursor.execute("""INSERT INTO DEVICE (folder_id,name_user,IMEI,description,IP,port,modbus_over_tcp,add_pr200,add_tr16,add_inv,type_inv,GMT,enable) VALUES 
                            ('"""+str(answear[0][0])+"""', '"""+str(self.new_device_name_user.get())+"""', 
                            '"""+str(self.new_device_IMEI.get())+"""', '"""+str(self.new_device_description.get())+"""', 
                            '"""+str(self.new_device_IP.get())+"""', '"""+str(self.new_device_port.get())+"""', 
                            '"""+str(self.new_device_modbus_over_tcp.get())+"""', '"""+str(self.new_device_add_pr200.get())+"""', 
                            '"""+str(self.new_device_add_tr16.get())+"""', '"""+str(self.new_device_add_inv.get())+"""', 
                            '"""+str(self.new_device_type_inv.get())+"""', '"""+str(self.new_device_GMT.get())+"""', 
                            '"""+str(self.new_device_en.get())+"""')""")
            con.commit()
        self.Tree_Refresh()
        self.form_new_device.root.destroy()

class scene_perm:        
    def __init__(self,sort,id):
        self.form_perm=Form("Разрешения пользователей","1200x600")
        self.lframe_perm=Frame(self.form_perm.root)
        self.lframe_perm.pack(side=LEFT)
        self.lframe_perm_top=Frame(self.lframe_perm)
        self.lframe_perm_top.pack(side=TOP)
        self.lframe_perm_bot=Frame(self.lframe_perm)
        self.lframe_perm_bot.pack(side=BOTTOM)
        self.rframe_perm=Frame(self.form_perm.root)
        self.rframe_perm.pack(side=LEFT, padx=4,pady=4)
        self.table_perm=ttk.Treeview(self.lframe_perm_top, columns=("id","client_name","user_name","folder_name","rule_name"), displaycolumns=(0,1,2,3,4), show="headings")
        self.table_perm.heading("id", text="ID")
        self.table_perm.heading("client_name", text="Клиент")
        self.table_perm.heading("user_name", text="Пользователь")
        self.table_perm.heading("folder_name", text="Папка")
        self.table_perm.heading("rule_name", text="Разрешение")
        self.table_perm.column(0,width=30,stretch=False)
        self.table_perm.configure(height=26)
        self.table_perm.pack(side=LEFT,padx=4, pady=4, anchor="nw")
        self.scrl_perm=Scrollbar(self.lframe_perm_top, command=self.table_perm.yview)
        self.scrl_perm.pack(side=LEFT, fill=Y)
        self.table_perm.config(yscrollcommand=self.scrl_perm.set) 
        self.table_perm.bind('<<TreeviewSelect>>',self.Detect_click)
        self.Refresh_table(sort,id)
        self.but_show_all=But(self.lframe_perm_bot,"Показать всё",lambda:self.Show_all(),LEFT)
        self.but_show_client=But(self.lframe_perm_bot,"Показать клиента",lambda:self.Show_client(),LEFT)
        self.but_show_folder=But(self.lframe_perm_bot,"Показать папку",lambda:self.Show_folder(),LEFT)
        self.but_show_user=But(self.lframe_perm_bot,"Показать пользователя",lambda:self.Show_user(),LEFT)
        self.but_new_perm=But(self.lframe_perm_bot,"Создать разрешение",lambda:self.CreatePerm_form(),LEFT)
    
    def Refresh_table(self,sort,id):
        self.table_perm.delete(*self.table_perm.get_children())
        self.last_sort=(sort,id)
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            if sort=="user":
                cursor.execute("""SELECT * FROM USER_PERM WHERE user_id='"""+str(id)+"""'""")
            elif sort=="folder":
                cursor.execute("""SELECT * FROM USER_PERM WHERE folder_id='"""+str(id)+"""'""")
            elif sort=="client":
                cursor.execute("""SELECT user_id FROM USER WHERE client_id='"""+str(id)+"""'""")
                answear=cursor.fetchall()
                answear=unpack(answear)
                answear=tuple(answear)
                cursor.execute("""SELECT * FROM USER_PERM WHERE user_id IN """+str(answear))
            else:
                cursor.execute("""SELECT * FROM USER_PERM""")
            answear=cursor.fetchall()
            self.tableuser=[]
            for string in answear:
                cursor.execute("""SELECT USER.name,CLIENT.name,FOLDER.name,RULES.name 
                               FROM USER,CLIENT,FOLDER,RULES 
                               WHERE USER.user_id='"""+str(string[1])+"""' 
                               AND USER.client_id=CLIENT.client_id 
                               AND FOLDER.folder_id='"""+str(string[2])+"""' 
                               AND RULES.rule_id='"""+str(string[3])+"""'""")
                answear=cursor.fetchall()
                username=answear[0][0]
                clientname=answear[0][1]
                foldername=answear[0][2]
                rulename=answear[0][3]
                newstring=(string[0],clientname,username,foldername,rulename)
                self.tableuser.append(newstring)
        for user in self.tableuser:
            self.table_perm.insert("", "end", user[0], values=user)
    
    def Show_all(self):
        self.Refresh_table("all",0)    
            
    def Show_client(self):
        try:
            self.Refresh_table("client",self.client_id)
        except:
            pass        
    
    def Show_folder(self):
        try:
            self.Refresh_table("folder",self.folder_id)
        except:
            pass 
    
    def Show_user(self):
        try:
            self.Refresh_table("user",self.user_id)
        except:
            pass 
            
    def Detect_click(self,event):
        self.curobject=self.table_perm.focus()
        if not self.curobject:
            return
        self.rframe_perm.destroy()
        self.rframe_perm=Frame(self.form_perm.root)
        self.rframe_perm.pack(side=LEFT, padx=4,pady=4)
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT * FROM USER_PERM WHERE perm_id='"""+str(self.curobject)+"""'""")
            answear=cursor.fetchall()
            self.perm_id=answear[0][0]
            self.user_id=answear[0][1]
            self.folder_id=answear[0][2]
            self.rule_id=answear[0][3]
            cursor.execute("""SELECT USER.name,CLIENT.client_id,CLIENT.name,FOLDER.name,RULES.name 
                            FROM USER,CLIENT,FOLDER,RULES 
                            WHERE USER.user_id='"""+str(self.user_id)+"""' 
                            AND USER.client_id=CLIENT.client_id 
                            AND FOLDER.folder_id='"""+str(self.folder_id)+"""' 
                            AND RULES.rule_id='"""+str(self.rule_id)+"""'""")
            self.answear=cursor.fetchall()
            self.username=self.answear[0][0]
            self.client_id=self.answear[0][1]
            self.clientname=self.answear[0][2]
            self.foldername=self.answear[0][3]
            self.rulename=self.answear[0][4]
            cursor.execute("""SELECT name FROM USER""")
            answear=cursor.fetchall()
            self.user_list=unpack(answear)
            cursor.execute("""SELECT name FROM FOLDER""")
            answear=cursor.fetchall()
            self.folder_list=unpack(answear)
            cursor.execute("""SELECT name FROM RULES""")
            answear=cursor.fetchall()
            self.rule_list=unpack(answear)   
        self.ent_id_perm=Ent(self.rframe_perm,"ID правила",self.perm_id,TOP,justify="center")
        self.ent_id_perm.block()
        self.ent_id_perm=Ent(self.rframe_perm,"Клиент",self.clientname,TOP,justify="center")
        self.ent_id_perm.block()
        self.cmbx_user=Cmbox(self.rframe_perm,"Пользователь",self.user_list,TOP)
        self.cmbx_user.set(self.username)
        self.cmbx_folder=Cmbox(self.rframe_perm,"Папка",self.folder_list,TOP)
        self.cmbx_folder.set(self.foldername)
        self.cmbx_perm=Cmbox(self.rframe_perm,"Максимальные права",self.rule_list,TOP)
        self.cmbx_perm.set(self.rulename)
        self.but_frame1=Frame(self.rframe_perm)
        self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save=But(self.but_frame1,"Сохранить",lambda:self.SavePerm_form(),LEFT)    
        self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeletePerm_form(),RIGHT)
        self.but_frame2=Frame(self.rframe_perm)
        self.but_frame2.pack(side=TOP, fill=X, padx=8, pady=10)
    
    def SavePerm_form(self):
        self.form_perm_upd=Toplevel()
        self.form_perm_upd.geometry("250x65")
        self.form_perm_upd.title("Сохранить изменения")
        self.form_perm_upd.wait_visibility()
        self.form_perm_upd.grab_set_global()
        self.lab_upd=Label(self.form_perm_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_perm_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.SavePerm_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_perm_upd.destroy(),RIGHT)
        self.form_perm_upd.mainloop()
    
    def SavePerm_DB(self):
        self.username=self.cmbx_user.get()
        self.foldername=self.cmbx_folder.get()
        self.rulename=self.cmbx_perm.get()
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT USER.user_id,FOLDER.folder_id,RULES.rule_id 
                           FROM USER,FOLDER,RULES 
                           WHERE USER.name='"""+str(self.username)+"""' 
                           AND FOLDER.name='"""+str(self.foldername)+"""' 
                           AND RULES.name='"""+str(self.rulename)+"""'""")
            answear=cursor.fetchall()
            self.user_id=answear[0][0]
            self.folder_id=answear[0][1]
            self.rule_id=answear[0][2]
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""UPDATE USER_PERM SET user_id='"""+str(self.user_id)+"""',folder_id='"""+str(self.folder_id)+"""',rule_id='"""+str(self.rule_id)+"""' 
                           WHERE perm_id="""+str(self.perm_id))
            con.commit()
        self.Refresh_table(self.last_sort[0],self.last_sort[1])
        self.form_perm_upd.destroy()
    
    def DeletePerm_form(self):
        self.form_del_perm=Toplevel()
        self.form_del_perm.geometry("300x65")
        self.form_del_perm.title("Удалить разрешение")
        self.form_del_perm.wait_visibility()
        self.form_del_perm.grab_set_global()       
        self.lab_del=Label(self.form_del_perm, text="Вы точно хотите удалить разрешение?")
        self.lab_del.pack(side=TOP)
        self.f_upd=Frame(self.form_del_perm, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeletePerm_DB(),LEFT)
        self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del_perm.destroy(),RIGHT)
        self.form_del_perm.mainloop()
    
    def DeletePerm_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""DELETE FROM USER_PERM WHERE perm_id='"""+str(self.perm_id)+"""'""")
            con.commit()
        self.Refresh_table(self.last_sort[0],self.last_sort[1])
        self.form_del_perm.destroy()
        
    def CreatePerm_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM USER""")
            answear=cursor.fetchall()
            self.user_list=unpack(answear)
            cursor.execute("""SELECT name FROM FOLDER""")
            answear=cursor.fetchall()
            self.folder_list=unpack(answear)
            cursor.execute("""SELECT name FROM RULES""")
            answear=cursor.fetchall()
            self.rule_list=unpack(answear) 
        self.form_new_perm=Form("Создать разрешение","300x300")
        self.new_cmbx_user=Cmbox(self.form_new_perm.root,"Пользователь",self.user_list,TOP)
        self.new_cmbx_folder=Cmbox(self.form_new_perm.root,"Папка",self.folder_list,TOP)
        self.new_cmbx_rule=Cmbox(self.form_new_perm.root,"Права доступа",self.rule_list,TOP)
        self.but_frame_create_perm1=Frame(self.form_new_perm.root)
        self.but_frame_create_perm1.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save_new_client=But(self.but_frame_create_perm1,"Сохранить",lambda:self.CreatePerm_DB(),LEFT)
        self.but_cancel_new_client=But(self.but_frame_create_perm1,"Отмена",lambda:self.form_new_perm.root.destroy(),RIGHT)
    
    def CreatePerm_DB(self):
        con = sl.connect(pathDB)
        username=self.new_cmbx_user.get()
        foldername=self.new_cmbx_folder.get()
        rulename=self.new_cmbx_rule.get()
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT USER.user_id,FOLDER.folder_id,RULES.rule_id 
                           FROM USER,FOLDER,RULES 
                           WHERE USER.name='"""+str(username)+"""' 
                           AND FOLDER.name='"""+str(foldername)+"""' 
                           AND RULES.name='"""+str(rulename)+"""'""")
            answear=cursor.fetchall()
            user_id=answear[0][0]
            folder_id=answear[0][1]
            rule_id=answear[0][2]
            cursor.execute("""INSERT INTO USER_PERM (user_id,folder_id,rule_id) 
                           VALUES ('"""+str(user_id)+"""','"""+str(folder_id)+"""','"""+str(rule_id)+"""')""")
            con.commit()
        self.Refresh_table(self.last_sort[0],self.last_sort[1])
        self.form_new_perm.root.destroy()

class scene_user:
    def __init__(self): 
        self.form_user=Form("Пользователи","750x600")
        self.lframe_user=Frame(self.form_user.root)
        self.lframe_user.pack(side=LEFT)
        self.lframe_user_top=Frame(self.lframe_user)
        self.lframe_user_top.pack(side=TOP)
        self.tree_user=ttk.Treeview(self.lframe_user_top, columns=("Name","Description"), displaycolumns=(0,1), show="tree")
        self.tree_user.configure(height=28)
        self.tree_user.pack(side=LEFT,padx=4, pady=4, anchor="nw")
        self.tree_user.column("#0", stretch=True, anchor="w", width=60)
        self.tree_user.column("Name", stretch=False, anchor="w", width=200)
        self.scrl=Scrollbar(self.lframe_user_top, command=self.tree_user.yview)
        self.scrl.pack(side=LEFT, fill=Y)
        self.tree_user.config(yscrollcommand=self.scrl.set) 
        self.TreeUser_Refresh()
        self.rframe_user=Frame(self.form_user.root)
        self.rframe_user.pack(side=RIGHT, padx=4,pady=4)
        self.tree_user.bind('<<TreeviewSelect>>',self.Detect_click)
        self.lframe_user_bot=Frame(self.lframe_user)
        self.lframe_user_bot.pack(side=BOTTOM)
        self.but_new_client=But(self.lframe_user_bot,"Новый пользователь",lambda:self.CreateUser_form(),LEFT)
        self.form_user.root.mainloop()   
        
    def TreeUser_Refresh(self):
        self.tree_user.delete(*self.tree_user.get_children())
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT client_id, name FROM CLIENT""")
            self.clients_list=cursor.fetchall()
            for i in self.clients_list:
                lab0=self.tree_user.insert("","end","clt-"+str(i[0]), values=(i[1],""))
            cursor.execute("""SELECT user_id, client_id, name FROM USER""")
            self.user_list=cursor.fetchall()
            if self.user_list!=[]:
                for i in self.user_list:
                    lab1=self.tree_user.insert("clt-"+str(i[1]),"end","usr-"+str(i[0]), values=(i[2],""))
    
    def Detect_click(self,event):
        self.curobject=self.tree_user.focus().split("-")
        if not self.curobject:
            return
        self.rframe_user.destroy()
        self.rframe_user=Frame(self.form_user.root)
        self.rframe_user.pack(side=LEFT, padx=4,pady=4)
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
            self.ent_id_client=Ent(self.rframe_user,"ID клиента",self.client_id,TOP,justify="center")
            self.ent_id_client.block()
            self.ent_name_client=Ent(self.rframe_user,"Название клиента",self.client_name,TOP)
            self.cmbx_rule=Cmbox(self.rframe_user,"Максимальные права клиента",self.rules_list,TOP)
            self.cmbx_rule.set(self.client_rule_name)
            self.but_frame1=Frame(self.rframe_user)
            self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
            self.but_save=But(self.but_frame1,"Сохранить",lambda:self.UpdateClient_form(),LEFT)
            self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeleteClient_form(),RIGHT)
            self.but_showperm=But(self.but_frame1,"Доступ",lambda:scene_perm("client",self.client_id),BOTTOM)
            self.but_frame2=Frame(self.rframe_user)
            self.but_frame2.pack(side=TOP, fill=X, padx=8, pady=10)
        elif self.curobject[0]=="usr":
            con = sl.connect(pathDB)
            with con:
                cursor=con.cursor()
                cursor.execute("""SELECT * FROM USER WHERE user_id='"""+self.curobject[1]+"""'""")
                answear=cursor.fetchall()
                self.user_id=answear[0][0]
                self.client_id=answear[0][1]
                self.username=answear[0][2]
                self.userlogin=answear[0][3]
                self.userpass=answear[0][4]
                self.usertgid=answear[0][5]
                cursor.execute("""SELECT name FROM CLIENT""")
                self.client_list=cursor.fetchall()
                self.client_list=unpack(self.client_list)
                cursor.execute("""SELECT name FROM CLIENT WHERE client_id='"""+str(self.client_id)+"""'""")
                answear=cursor.fetchall()
                self.clientname=answear[0][0]
            self.ent_id_user=Ent(self.rframe_user,"ID пользователя",self.user_id,TOP,justify="center")
            self.ent_id_user.block()
            self.cmbx_client=Cmbox(self.rframe_user,"Клиент",self.client_list,TOP)
            self.cmbx_client.set(self.clientname)
            self.ent_username=Ent(self.rframe_user,"Имя пользователя",self.username,TOP,justify="center")
            self.ent_userlogin=Ent(self.rframe_user,"Логин",self.userlogin,TOP,justify="center")
            self.ent_userpass=Ent(self.rframe_user,"Пароль",self.userpass,TOP,justify="center")
            self.ent_usertgid=Ent(self.rframe_user,"ID Telegram",self.usertgid,TOP,justify="center")
            self.but_frame1=Frame(self.rframe_user)
            self.but_frame1.pack(side=TOP, fill=X, padx=8, pady=10)
            self.but_save=But(self.but_frame1,"Сохранить",lambda:self.UpdateUser_form(),LEFT)
            self.but_del=But(self.but_frame1,"Удалить",lambda:self.DeleteUser_form(),RIGHT)
            self.but_showperm=But(self.but_frame1,"Доступ",lambda:scene_perm("user",self.user_id),BOTTOM)
            self.but_frame2=Frame(self.rframe_user)
            self.but_frame2.pack(side=TOP, fill=X, padx=8, pady=10)
    
    def UpdateClient_form(self):
        self.form_client_upd=Toplevel()
        self.form_client_upd.geometry("250x65")
        self.form_client_upd.title("Сохранить изменения")
        self.form_client_upd.wait_visibility()
        self.form_client_upd.grab_set_global()
        self.lab_upd=Label(self.form_client_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_client_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.UpdateClient_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_client_upd.destroy(),RIGHT)
        self.form_client_upd.mainloop()
            
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
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""UPDATE CLIENT SET name='"""+self.client_name+"""',rule_id='"""+str(self.client_rule)+"""' WHERE client_id="""+str(self.client_id))
            con.commit()
        self.TreeUser_Refresh()
        self.form_client_upd.destroy()
        
    def UpdateUser_form(self):
        self.form_user_upd=Toplevel()
        self.form_user_upd.geometry("250x65")
        self.form_user_upd.title("Сохранить изменения")
        self.form_user_upd.wait_visibility()
        self.form_user_upd.grab_set_global()
        self.lab_upd=Label(self.form_user_upd, text="Вы хотите сохранить изменения?")
        self.lab_upd.pack(side=TOP)
        self.f_upd=Frame(self.form_user_upd, width=200)
        self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
        self.but_upd_yes=But(self.f_upd,"Сохранить",lambda:self.UpdateUser_DB(),LEFT)
        self.but_upd_no=But(self.f_upd,"Отменить",lambda:self.form_user_upd.destroy(),RIGHT)
        self.form_user_upd.mainloop()
    
    def UpdateUser_DB(self):
        self.user_id=self.ent_id_user.get()
        self.clientname=self.cmbx_client.get()
        self.username=self.ent_username.get()
        self.userlogin=self.ent_userlogin.get()
        self.userpass=self.ent_userpass.get()
        self.usertgid=self.ent_usertgid.get()
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT client_id FROM CLIENT WHERE name='"""+str(self.clientname)+"""'""")
            answear=cursor.fetchall()
            self.client_id=answear[0][0]
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""UPDATE USER SET client_id='"""+str(self.client_id)+"""',name='"""+str(self.username)+"""',
                           login='"""+str(self.userlogin)+"""',password='"""+str(self.userpass)+"""',tg_id='"""+str(self.usertgid)+"""'
                           WHERE user_id="""+str(self.user_id))
            con.commit()
        self.TreeUser_Refresh()
        self.form_user_upd.destroy()
    
    def CreateUser_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM CLIENT""")
            self.client_list=cursor.fetchall()
            self.client_list=unpack(self.client_list)
        self.form_new_user=Form("Создать пользователя","300x300")
        self.new_cmbx_user=Cmbox(self.form_new_user.root,"Клиент",self.client_list,TOP)
        self.new_name_user=Ent(self.form_new_user.root,"Имя пользователя","",TOP)
        self.new_login_user=Ent(self.form_new_user.root,"Логин","",TOP)
        self.new_pass_user=Ent(self.form_new_user.root,"Пароль","",TOP)
        self.new_tgid_user=Ent(self.form_new_user.root,"ID Telegram","",TOP)
        try:
            self.new_cmbx_user.set(self.ent_name_client.get())
        except:
            self.new_cmbx_user.set(self.client_list[0])
        self.but_frame_create_user=Frame(self.form_new_user.root)
        self.but_frame_create_user.pack(side=TOP, fill=X, padx=8, pady=10)
        self.but_save_new_folder=But(self.but_frame_create_user,"Сохранить",lambda:self.CreateUser_DB(),LEFT)
        self.but_cancel_new_folder=But(self.but_frame_create_user,"Отмена",lambda:self.form_new_user.root.destroy(),RIGHT)
    
    def CreateUser_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT client_id FROM CLIENT WHERE name='"""+str(self.new_cmbx_user.get())+"""'""")
            answear=cursor.fetchall()
            cursor.execute("""INSERT INTO USER (client_id,name,login,password,tg_id) 
                           VALUES ('"""+str(answear[0][0])+"""','"""+self.new_name_user.get()+"""','"""+self.new_login_user.get()+"""',
                           '"""+self.new_pass_user.get()+"""','"""+self.new_tgid_user.get()+"""')""")
            con.commit()
        self.TreeUser_Refresh()
        self.form_new_user.root.destroy()
    
    def DeleteClient_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT name FROM FOLDER WHERE client_id='"""+str(self.client_id)+"""'""")
            folder_list=cursor.fetchall()
            cursor.execute("""SELECT name FROM USER WHERE client_id='"""+str(self.client_id)+"""'""")
            user_list=cursor.fetchall()
        self.form_del_client=Toplevel()
        self.form_del_client.geometry("300x65")
        self.form_del_client.title("Удалить клиента")
        self.form_del_client.wait_visibility()
        self.form_del_client.grab_set_global()
        if folder_list == [] and user_list == []:        
            self.lab_del=Label(self.form_del_client, text="Вы точно хотите удалить клиента?")
            self.lab_del.pack(side=TOP)
            self.f_upd=Frame(self.form_del_client, width=200)
            self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
            self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeleteClient_DB(),LEFT)
            self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del_client.destroy(),RIGHT)
        else:
            self.lab_del=Label(self.form_del_client, text="Удаление невозможно, есть привязанные объекты")
            self.lab_del.pack(side=TOP)
            self.but_del_ok=But(self.form_del_client,"ОК",lambda:self.form_del_client.destroy(),TOP)
        self.form_del_client.mainloop()
        
    def DeleteClient_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""DELETE FROM CLIENT WHERE client_id='"""+str(self.client_id)+"""'""")
            con.commit()
        self.TreeUser_Refresh()
        self.form_del_client.destroy()
    
    def DeleteUser_form(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""SELECT perm_id FROM USER_PERM WHERE user_id='"""+str(self.user_id)+"""'""")
            perm_list=cursor.fetchall()
        self.form_del_user=Toplevel()
        self.form_del_user.geometry("300x65")
        self.form_del_user.title("Удалить пользователя")
        self.form_del_user.wait_visibility()
        self.form_del_user.grab_set_global()
        if perm_list == []:        
            self.lab_del=Label(self.form_del_user, text="Вы точно хотите удалить пользователя?")
            self.lab_del.pack(side=TOP)
            self.f_upd=Frame(self.form_del_user, width=200)
            self.f_upd.pack(side=BOTTOM, fill=X, padx=8, pady=8)
            self.but_del_yes=But(self.f_upd,"Удалить",lambda:self.DeleteUser_DB(),LEFT)
            self.but_del_no=But(self.f_upd,"Отменить",lambda:self.form_del_user.destroy(),RIGHT)
        else:
            self.lab_del=Label(self.form_del_user, text="Удаление невозможно, есть привязанные объекты")
            self.lab_del.pack(side=TOP)
            self.but_del_ok=But(self.form_del_user,"ОК",lambda:self.form_del_user.destroy(),TOP)
        self.form_del_user.mainloop()
    
    def DeleteUser_DB(self):
        con = sl.connect(pathDB)
        with con:
            cursor=con.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON;""")
            cursor.execute("""DELETE FROM USER WHERE user_id='"""+str(self.user_id)+"""'""")
            con.commit()
        self.TreeUser_Refresh()
        self.form_del_user.destroy()
        
        
M=main_window()