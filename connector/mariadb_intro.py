# coding: utf-8
import mariadb
ping
conn = mariadb.connect( user = "example", password = "example", host = "kolekcje-db-1", port =3306, database="katalog" )
conn
dir(conn)
conn.ping()
v=conn.ping()
v
cur=conn.cursor()
cur.execute( "show tables")
cur
cur.fetchall()
cur.execute( "SELECT * FROM Books" )
cur.fetchall()
cur.execute( "DESCRIBE Books" )
cur.fetchall()
