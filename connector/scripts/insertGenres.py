# coding: utf-8
import mariadb
conn = mariadb.connect( user="example", password = "example",
  host = "172.18.0.3", port=3306, database="katalog" )

cur.execute( "SHOW TABLES;" )
cur.fetchall()

rodzaje = ( 'proza', 'poezja', 'fantastyka', 'sztuka', 'orientalia', 'nauka', 'języki', 'słownik', 'humanistyka', 'komiks', 'historia' )
for r in rodzaje:
    cur.execute( f"INSERT INTO genres (name) VALUES ('{r}')" )
cur.connection.commit()
