# coding: utf-8
import codecs
with codecs.open( 'output.json', 'r', 'utf-8' ) as fh:
    text = fh.read()
    
with open( 'o2.json', 'wt' ) as fh:
    fh.write( text )
    
