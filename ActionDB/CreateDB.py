import sqlite3 as sl
pathDB='Logs.db'
con = sl.connect(pathDB)
with con:
    con.execute("""PRAGMA foreign_keys = ON;""")
    con.execute("""
        CREATE TABLE RULES (
            rule_id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            web BOOL NOT NULL,
            setting BOOL NOT NULL,
            control BOOL NOT NULL,
            report BOOL NOT NULL,
            bot BOOL NOT NULL
        );
    """)
    con.execute("""
        CREATE TABLE CLIENT (
            client_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            rule_id INTEGER NOT NULL,
            FOREIGN KEY (rule_id) REFERENCES RULES (rule_id) ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)
    con.execute("""
        CREATE TABLE USER (
            user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            tg_id TEXT,
            FOREIGN KEY (client_id) REFERENCES CLIENT (client_id) ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)
    con.execute("""
        CREATE TABLE FOLDER (
            folder_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            root_folder INTEGER,
            name TEXT NOT NULL UNIQUE,
            FOREIGN KEY (client_id) REFERENCES CLIENT (client_id) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (root_folder) REFERENCES FOLDER (folder_id) ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)
    con.execute("""
        CREATE TABLE USER_PERM (
            perm_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            folder_id INTEGER NOT NULL,
            rule_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES USER (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (folder_id) REFERENCES FOLDER (folder_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (rule_id) REFERENCES RULES (rule_id) ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)
    con.execute("""
        CREATE TABLE DEVICE (
            device_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            folder_id INTEGER NOT NULL,
            name_user TEXT NOT NULL UNIQUE,
            IMEI TEXT NOT NULL UNIQUE,
            description TEXT,
            IP TEXT NOT NULL,
            port INTEGER NOT NULL,
            modbus_over_tcp BOOL NOT NULL,
            add_pr200 INTEGER NOT NULL,
            add_tr16 INTEGER,
            add_inv INTEGER,
            type_inv TEXT,
            GMT TEXT NOT NULL,
            FOREIGN KEY (folder_id) REFERENCES FOLDER (folder_id) ON UPDATE CASCADE ON DELETE RESTRICT
        );
    """)
    con.execute("""
        CREATE TABLE RECORD_TYPE (
            rectype_id INTEGER NOT NULL PRIMARY KEY,
            type INTEGER NOT NULL,
            description TEXT NOT NULL
        );
    """)
    con.execute("""
        CREATE TABLE LOG_EVENT (
            log_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            timestamp_loc DATETIME NOT NULL,
            timestamp_dev DATETIME NOT NULL,
            GMT TEXT NOT NULL,
            status INTEGER NOT NULL,
            depth INTEGER NOT NULL,
            power INTEGER NOT NULL,
            status_string INTEGER,
            data TEXT,
            FOREIGN KEY (device_id) REFERENCES DEVICE (device_id) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)
    con.execute("""
        CREATE TABLE LOG_TIME (
            log_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            timestamp_loc DATETIME NOT NULL,
            timestamp_dev DATETIME NOT NULL,
            GMT TEXT NOT NULL,
            status INTEGER NOT NULL,
            depth INTEGER NOT NULL,
            power INTEGER NOT NULL,
            status_string INTEGER,
            data TEXT,
            FOREIGN KEY (device_id) REFERENCES DEVICE (device_id) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)
    con.execute("""
        CREATE TABLE JOURNAL (
            journal_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            rectype_id INTEGER NOT NULL,
            device_id INTEGER,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES USER (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (rectype_id) REFERENCES RECORD_TYPE (rectype_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (device_id) REFERENCES DEVICE (device_id) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)
    con.execute("""
        CREATE TABLE LOG_SETTING (
            log_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            journal_id INTEGER,
            data TEXT NOT NULL,
            FOREIGN KEY (device_id) REFERENCES DEVICE (device_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (journal_id) REFERENCES JOURNAL (journal_id) ON UPDATE CASCADE ON DELETE CASCADE
        );
    """)
    con.commit()