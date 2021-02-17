import sqlite3


def create_db(db):
    action = ("CREATE TABLE IF NOT EXISTS stats ("
                "id INTEGER PRIMARY KEY, "
                "datetime CHAR(19) NOT NULL, "
                "per FLOAT NOT NULL, "
                "min FLOAT NOT NULL, "
                "avg FLOAT NOT NULL, "
                "max FLOAT NOT NULL, "
                "mdev FLOAT NOT NULL)"
                )
    db = sqlite3.connect(db)
    c = db.cursor()
    c.execute(action)
    db.commit()
    db.close()


def add_record(db, stats: list):
    db = sqlite3.connect(db)
    c = db.cursor()
    c.execute("INSERT INTO stats('datetime', 'per', 'min', 'avg', 'max', 'mdev') VALUES(?, ?, ?, ?, ?, ?)",
              (stats[0], stats[1], stats[2], stats[3], stats[4], stats[5])
              )
    db.commit()
    db.close()
