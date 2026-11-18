import sqlite3, sys
con = sqlite3.connect("file:data/boutique.sqlite?mode=ro", uri=True)
sql = open(sys.argv[1], encoding="utf-8").read()
cur = con.execute(sql)
print([d[0] for d in cur.description])
for row in cur.fetchall():
    print(row)