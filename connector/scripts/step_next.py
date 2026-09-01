# coding: utf-8
import mariadb
import ib,importlib
(conn,cur)=ib.makeConnection()
jedno=ib.loadData()
cur.execute( "SELECT id FROM Books WHERE name = %s", ("Cyprian Kamil Norwid",) )
cur.execute( "SELECT id FROM Authors WHERE name LIKE '%Norwid'" )
nn=cur.fetchall()
cur.execute( "SELECT book_id FROM bookAuthors WHERE author_id = 74" )
n2=cur.fetchall()

cur.execute( "SELECT id FROM series WHERE name = %s", (kk['Seria'],) )
cur.fetchall()

cur.execute( "UPDATE Books SET series_id = ? WHERE id = ?", (3,67) )
conn.commit()
cur.lastrowid

cur.execute( "describe Books" )
cur.fetchall()


cur.executemany( "INSERT INTO bookGenres (book_id,genre_id) VALUES (?,?)", [(67,4),(68,4)] )
cur.executemany( "INSERT INTO bookAuthors (book_id,author_id) VALUES (?,?)", [(67,74),(68,74)] )
conn.commit()

cur.execute( "SELECT book_id FROM bookAuthors WHERE author_id = 84" )
cur.fetchall()
cur.execute( "SELECT book_id FROM bookAuthors WHERE author_id = 74" )
cur.fetchall()

cur.execute( "UPDATE Books SET series_id = ? WHERE id = ?", (1,166) )
conn.commit()
cur.execute( "SELECT * FROM bookAuthors WHERE author_id = 129" )
cur.fetchall()
cur.execute( "SELECT title FROM Books WHERE id IN (125,126,166)" )
cur.fetchall()
