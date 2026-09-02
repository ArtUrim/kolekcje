import json
import mariadb
import logging

def fill(kk):
    fields = [kk['Tytuł'],'paperback',4,'pl_']
    vals = '?,?,?,?'
    ints = 'title,format,publisher_id,language_id'
    if 'ISBN' in kk:
        fields.append( kk['ISBN'] )
        vals += ',?'
        ints += ',isbn'
    if 'Data wydania' in kk:
        fields.append( int(kk['Data wydania'][0:4]) )
        vals += ',?'
        ints += ',release_date'
    if 'Liczba stron' in kk:
        fields.append( kk['Liczba stron'] )
        vals += ',?'
        ints += ',pages'
    if 'Opis' in kk:
        fields.append( kk['Opis'] )
        vals += ',?'
        ints += ',description'
    if 'Tłumacz' in kk:
        fields.append( kk['Tłumacz'] )
        vals += ',?'
        ints += ',translator'

    if 'Tytuł oryginału' in kk:
        fields.append( kk['Tytuł oryginału'] )
        vals += ',?'
        ints += ',original_title'

    if 'Data 1. wyd. pol.' in kk:
        fields.append( int(kk['Data 1. wyd. pol.'][0:4]) )
        vals += ',?'
        ints += ',first_polish_release_date'
    
    qStr = f"INSERT INTO Books ({ints}) VALUES ({vals})"
    qTuple = tuple(fields)

    return( qStr, qTuple )

""" TODO
    dd  "Seria": "Biblioteka Jednoro\u017cca",
"""

def loadData():
    with open( 'fig.json', 'r' ) as fh:
        jedno = json.load(fh)
    return jedno

def makeConnection():
    conn = mariadb.connect( user = "example", password = "example", host = "kolekcje-db-1", port =3306, database="katalog" )
    cur=conn.cursor()
    return (conn,cur)

def makeAuthor( conn,cur, autor ):
    if cur:
        cur.execute( "SELECT id FROM Authors WHERE name = %s", (autor,) )
        res = cur.fetchone()
        if res:
            return res[0]
        cur.execute( "INSERT INTO Authors (name,nationality_id) VALUES (?,?) ON DUPLICATE KEY UPDATE name = VALUES(name)", ( autor, 'pl_' ) )
        aut_id = cur.lastrowid
        conn.commit()
        return aut_id
    return None

def addSerie(conn,cur,kk,bookId):
    if cur:
        cur.execute( "SELECT id FROM series WHERE name = %s", (kk['Seria'],) )
        seria_id = cur.fetchone()
        if seria_id:
            seria_id = seria_id[0]
        else:
            cur.execute( "INSERT INTO series (name) VALUES(?)", (kk['Seria'],) )
            seria_id = cur.lastrowid
            conn.commit()
        if seria_id:
            cur.execute( "UPDATE Books SET series_id = ? WHERE id = ?", (seria_id,bookId) )


def execOneBook(conn,cur,kk):
    aut_id = makeAuthor( conn,cur, kk['Autor'] )
    if aut_id:
        (qStr,qTuple) = fill(kk)
        if cur:
            cur.execute( qStr, qTuple )
            bid = cur.lastrowid
            conn.commit()
            cur.execute( "INSERT INTO bookGenres (book_id,genre_id) VALUES (?,?)",  (bid,4) )
            cur.execute( "INSERT INTO bookAuthors (book_id,author_id) VALUES (?,?)", (bid,aut_id) )
            addSerie( conn, cur, kk, bid )
            conn.commit()
    else:
        logging.error( f"Error in adding autor {kk['Autor']}" )

def dataProcess(conn,cur,jedno):
    for kk in jedno:
        execOneBook(conn,cur,kk)

