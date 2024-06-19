import sqlite3 as sl
pathDB='Logs.db'
con = sl.connect(pathDB)
with con:
    con.execute("""PRAGMA foreign_keys = ON;""")
    con.execute("""INSERT INTO RULES (rule_id, name, web, setting, control, report, bot) VALUES ('99', 'полный доступ', 'true', 'true', 'true', 'true', 'true')""")
    con.execute("""INSERT INTO RULES (rule_id, name, web, setting, control, report, bot) VALUES ('0', 'запрет доступа', 'false', 'false', 'false', 'false', 'false')""")
    con.execute("""INSERT INTO RULES (rule_id, name, web, setting, control, report, bot) VALUES ('10', 'только просмотр', 'true', 'false', 'false', 'false', 'false')""")
    con.execute("""INSERT INTO RULES (rule_id, name, web, setting, control, report, bot) VALUES ('20', 'с уставками', 'true', 'true', 'false', 'false', 'false')""")
    con.execute("""INSERT INTO RULES (rule_id, name, web, setting, control, report, bot) VALUES ('30', 'с управлением', 'true', 'true', 'true', 'false', 'false')""")
    
    con.execute("""INSERT INTO CLIENT (name, rule_id) VALUES ('DEBIT-E', '99')""")
    con.execute("""INSERT INTO CLIENT (name, rule_id) VALUES ('Клиент 1', '0')""")
    con.execute("""INSERT INTO CLIENT (name, rule_id) VALUES ('Клиент 2', '10')""")
    con.execute("""INSERT INTO CLIENT (name, rule_id) VALUES ('Клиент 3', '20')""")
    con.execute("""INSERT INTO CLIENT (name, rule_id) VALUES ('Клиент 4', '30')""")
    
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('1', 'admin', 'admin', 'qwerty')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('1', 'сервис инженер', 'serv_eng', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('2', 'технолог', 'tech1', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('2', 'оператор', 'oper1', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('3', 'технолог', 'tech2', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('3', 'оператор', 'oper2', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('4', 'технолог', 'tech3', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('4', 'оператор', 'oper3', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('5', 'технолог', 'tech4', '123')""")
    con.execute("""INSERT INTO USER (client_id, name, login, password) VALUES ('5', 'оператор', 'oper4', '123')""")
    
    con.execute("""INSERT INTO FOLDER (client_id, name) VALUES ('1', 'test_DE')""")
    con.execute("""INSERT INTO FOLDER (client_id, name, root_folder) VALUES ('1', 'DE_sub1', '1')""")
    con.execute("""INSERT INTO FOLDER (client_id, name, root_folder) VALUES ('1', 'DE_sub2', '1')""")
    con.execute("""INSERT INTO FOLDER (client_id, name) VALUES ('2', 'test_client1')""")
    con.execute("""INSERT INTO FOLDER (client_id, name) VALUES ('3', 'test_client2')""")
    con.execute("""INSERT INTO FOLDER (client_id, name) VALUES ('4', 'test_client3')""")
    con.execute("""INSERT INTO FOLDER (client_id, name) VALUES ('5', 'test_client4')""")
    
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '1', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '2', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '3', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '4', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '5', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '6', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('1', '7', '99')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('2', '4', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('2', '5', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('2', '6', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('2', '7', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('3', '4', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('4', '4', '10')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('5', '5', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('6', '5', '10')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('7', '6', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('8', '6', '10')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('9', '7', '30')""")
    con.execute("""INSERT INTO USER_PERM (user_id, folder_id, rule_id) VALUES ('10', '7', '10')""")
    
    
    con.execute("""INSERT INTO DEVICE (folder_id, name_user, IMEI, description, IP, port, modbus_over_tcp, add_pr200, add_tr16, add_inv, type_inv, GMT) 
                VALUES ('1', 'test_device', '1234567890', 'тестовая лебедка', '127.0.0.1', '10200', 'true', '10', '16', '1', 'danfoss', '+3')""")
    
    
    
    
    
    con.commit()