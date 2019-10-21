import sqlite3

conn = sqlite3.connect('macPrices.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS prices(gameName TEXT, price TEXT, link TEXT)")


def data_entry():
    c.execute("INSERT INTO prices VALUES('gameName','0.00','https...')")

    conn.commit()
    c.close()
    conn.close()

create_table()
data_entry()