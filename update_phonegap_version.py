#!/usr/bin/env python

from lxml.etree import parse

doc = parse(open("app/phonegap/config.xml", 'r'))

version_parts = map(int,doc.getroot().attrib['version'].split("."))
version_parts[-1] += 1

doc.getroot().attrib['version'] = ".".join(map(str, version_parts))
doc.write("app/phonegap/config.xml", encoding="utf-8", xml_declaration=True)

