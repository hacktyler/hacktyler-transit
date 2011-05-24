#!/usr/bin/env python

import sys

from lxml.html import parse
from lxml.cssselect import CSSSelector

filename = sys.argv[1]

doc = parse(open(filename, 'r'))

s = doc.xpath( CSSSelector('script').path )[0]
e = s.makeelement('script', attrib={'type': 'text/javascript','src': 'phonegap.js'})
s.addprevious(e)

doc.write(open(filename, 'w'), method='html', pretty_print=True)

