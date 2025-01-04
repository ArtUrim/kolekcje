# coding: utf-8
import mariadb

conn = mariadb.connect( user = "example", password = "example", host = "kolekcje-db-1", port =3306, database="katalog" )
v=conn.ping()

cur=conn.cursor()
cur.execute( "show tables")

cur.fetchall()
cur.execute( "SELECT * FROM Books" )
cur.fetchall()
cur.execute( "DESCRIBE Books" )
cur.fetchall()
