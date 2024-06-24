import psycopg2
import pandas as pd 

def getdblocation():
    db = psycopg2.connect(
        host='localhost',
        database='CIEM',
        user='postgres',
        port=5432,
        password='klarenz0027'
    )

    return db

def modifydatabase(sql, values):
    db=getdblocation()
    cursor=db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

def querydatafromdatabase(sql, values, dfcolumns=None):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    if dfcolumns is None:
        rows = pd.DataFrame(cur.fetchall())
    else:
        rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows

def get_latest_affiliation_id():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT affiliation_id FROM affiliation ORDER BY affiliation_id DESC LIMIT 1")
    latest_affiliation_id = cur.fetchone()[0]  # Directly fetch the ID
    cur.close()
    return latest_affiliation_id

def get_latest_alum_id():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT max(alum_id) FROM alumni")
    latest_alum_id = cur.fetchone()[0]  # Directly fetch the ID
    cur.close()
    return latest_alum_id
