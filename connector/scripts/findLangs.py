import requests
from bs4 import BeautifulSoup
r=requests.get( 'https://pl.wiktionary.org/wiki/Wikis%C5%82ownik:Kody_j%C4%99zyk%C3%B3w' )
br=BeautifulSoup( r.content, 'html.parser')
ts=br.find_all( 'table', class_ = 'wikitable' )
tb=ts[0].find( 'tbody' )
lang={}
for l in tb.find_all( 'tr'  ):
    ll = l.find_all( 'td' )
    if len(ll) == 2:
        lcode = str(ll[1].text).strip('\n')
        if len( lcode ) > 3:
            print( f"Too long: {str(ll[1].text)} - {str(ll[0].text)}" )
            continue
        elif len( lcode ) == 2:
            lcode = lcode + "_"
        lname = str(ll[0].text).strip('\n')
        if lname.startswith( 'język' ):
            lname = lname[6:]
        lang[lcode] = lname
    else:
        print( "Wrong table size: {len(ll)}" )


for l in lang:
    cur.execute( f"INSERT INTO language (id,name) VALUES ('{l}','{lang[l]}')" )
cur.connection.commit()

cur.execute( f"UPDATE series SET note = 'Przygody dwóch dzielnych wojaków (albo marynarzy)' WHERE id = '4';" )
cur.connection.commit()
