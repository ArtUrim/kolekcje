import json

with open( 'output.json', 'r' ) as fh:
    kk = json.load(fh)
cur.execute( "INSERT INTO publisher (name,webpage) VALUES (?,?)", ( kk[0]['Wydawnictwo'], 'kwiatyorientu.com' ) )
wydaw_id=cur.lastrowid

cur.execute( "INSERT INTO Authors (name,nationality_id) VALUES (?,?)", ( kk[0]['Autor'], 'xh_' ) )
conn.commit()
aut_id=cur.lastrowid

cur.execute( "INSERT INTO Books (isbn,title,release_date,format,publisher_id,pages,description,translator,language_id) VALUES (?,?,?,?,?,?,?,?,?)", ( kk[0]['ISBN'], kk[0]['Tytuł'], 2019, 'paperback', wydaw_id, kk[0]['Liczba stron'], kk[0]['Opis'], kk[0]['Tłumacz'], 'pl_' ) )
conn.commit()
book_id=cur.lastrowid

cur.executemany( "INSERT INTO bookGenres (book_id,genre_id) VALUES (?,?)",  [(book_id,4), (book_id,8)] )
conn.commit()

cur.execute( "INSERT INTO bookAuthors (book_id,author_id) VALUES (?,?)", (book_id,aut_id) )
conn.commit()
conn.close()
