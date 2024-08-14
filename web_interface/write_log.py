import sqlite3 as sql
from datetime import datetime

def write(user_id, rectype_id, device_id=None):
    db_conn=sql.connect('Logs.db')
    curs=db_conn.cursor()
    curs.execute(
        "INSERT INTO JOURNAL (user_id, rectype_id, device_id, timestamp) VALUES(?, ?, ?, ?)",
        (user_id, rectype_id, device_id, str(datetime.now())[0:19])
    )
    db_conn.commit()
    curs.execute("SELECT * FROM JOURNAL")
    # print(curs.fetchall ())
    db_conn.close()
# write(2, 4)
