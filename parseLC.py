# coding: utf-8
from bs4 import BeautifulSoup
import requests

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

if __name__ == "__main__":
    op = []
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/4883018/lkajace-ryby-i-inne-opowiadania' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/168442/miraz-zlota' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/72428/dom-przy-cmentarzu-t-1' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/72428/dom-przy-cmentarzu-t-1' ) )
    op.append(Opis( 'https://lubimyczytac.pl/ksiazka/72428/dom-przy-cmentarzu-t-1' ) )
