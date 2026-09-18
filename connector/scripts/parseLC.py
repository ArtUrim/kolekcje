# coding: utf-8
from bs4 import BeautifulSoup
import requests
import json
import re

import nameUtils

class Opis:

    def __init__(self, page : str ):
        self.__page = page
        self.__resp = requests.get( page )
        self.__parsed = BeautifulSoup( self.__resp.content, 'html.parser' )
        self.dane = self.getData()

    def getData( self ):
        dane = {}
        det=self.__parsed.find( 'div', id = 'book-details')
        if det:
            dt=det.find_all( 'dt' )
            dd=det.find_all( 'dd' )
            dane = { str(k.text).strip().rstrip(':'):str(v.text).strip() for k,v in zip(dt,dd) }
        
        if not 'Autor' in dane:
            so = self.__parsed.find( 'span', class_ = 'author' )
            if so:
                a = so.find('a')
                if a:
                    dane['Autor'] = str(a.text).strip()

        if not 'Opis' in dane:
            so = self.__parsed.find( 'div', id='book-description' )
            if so:
                a = so.find('p')
                if a:
                    dane['Opis'] = str(a.text).strip()

        if not 'Tytuł' in dane:
            so = self.__parsed.find( 'h1', class_ = 'book__title' )
            if so:
                dane['Tytuł'] = str(so.text).strip()

        if not 'Okładka' in dane:
            so = self.__parsed.find( 'div', class_ = 'book-cover' )
            if so:
                pic = so.find( 'picture' )
                if pic:
                    img = pic.find( 'img' )
                    if 'src' in pic:
                        dane['Okładka'] = pic['src'] # TODO: pobrać obrazek

        if not 'Wydawnictwo' in dane:
            so = self.__parsed.find( 'span', class_ = 'book__txt' )
            if so:
                dane['Wydawnictwo'] = str(so.text).strip() # TODO: usuń 'Wydawnictwo'  z początku string

        if not 'Kategoria' in dane:
            so = self.__parsed.find( 'a', class_='book__category')
            if so:
                dane['Kategoria'] = str(so.text).strip()

        if not 'Liczba stron' in dane:
            so = self.__parsed.find( 'span', class_='book-pages' )
            if so:
                dane['Liczba stron'] = str(so.text).strip()

        return dane


def toYear( value ):
    if value is None:
        return None
    m = re.search( r'\d{4}', str(value) )
    return int( m.group(0) ) if m else None

def toPages( value ):
    if value is None:
        return None
    digits = re.sub( r'\D', '', str(value) )
    return int( digits ) if digits else None

FORMAT_ENUM = { 'unknown', 'hardback', 'hardcover', 'paperback', 'papier',
                'ebook', 'e-book', 'jacket', 'notebook', '' }

def toFormat( value ):
    if not value:
        return None
    fmt = str(value).strip().lower()
    if fmt in FORMAT_ENUM:
        return fmt
    if 'e-book' in fmt or 'ebook' in fmt:
        return 'ebook'
    if 'twarda' in fmt:
        return 'hardback'
    if 'miękka' in fmt or 'miekka' in fmt or 'broszura' in fmt:
        return 'paperback'
    return 'unknown'

def toNamedEntity( title ):
    return { 'id': None, 'title': str(title).strip(), 'isCustom': True }

def toNamedEntities( value ):
    if value is None:
        return None
    titles = value if isinstance( value, list ) else str(value).split(',')
    return [ toNamedEntity( t ) for t in titles if str(t).strip() ]

def toSchema( dane ):
    transformers = {
        'publishYear': toYear,
        'firstPublishYear': toYear,
        'pages': toPages,
        'format': toFormat,
        'author': toNamedEntities,
        'publisher': toNamedEntities,
        'genre': toNamedEntities,
        'series': toNamedEntity,
    }

    book = {}
    for key, value in dane.items():
        if key in transformers:
            v = transformers[key]( value )
            if v:
                book[key] = v
        else:
            book[key] = value

    if 'publisher' in book:
        kept = []
        for e in book['publisher']:
            e['title'] = re.sub( r'^wydawnictwo\b[:\s]*', '', e['title'], flags=re.IGNORECASE ).strip()
            if e['title']:
                kept.append( e )
        if kept:
            book['publisher'] = kept
        else:
            del book['publisher']

    return book

def oldMain():
    op = []
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/4883018/lkajace-ryby-i-inne-opowiadania' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/168442/miraz-zlota' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/72428/dom-przy-cmentarzu-t-1' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/4893110/listy-milosne' ) )

    tj = [ o.dane for o in op ]
    with open('output.json', 'w') as json_file:
        json.dump(tj, json_file, indent=3)

if __name__ == "__main__":
    with open( "newUnicorns.txt", "rt" ) as fh:
        books = [ b.strip('\n') for b in fh.readlines()]

    for b in books:
        bn = nameUtils.transform_name( nameUtils.get_basename_from_uri( b ) )
        print(bn)
        opis = Opis( b )
        with open( bn + '.json', 'w', encoding='utf-8' ) as fh:
            json.dump( toSchema( nameUtils.translate_keys(opis.dane) ), fh, indent=3, ensure_ascii=False )
