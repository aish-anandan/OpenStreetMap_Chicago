# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 19:02:11 2020

@author: Aishwarya
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import json
"""
Data in .osm file is in the form of XML. There are different kinds of attributes. In this example, we only want tags where the attribute type is node, 
has a valid identification - name or amenity and has a lat-long position.
Parsed data will be in the following format and will be read into a MongoDB database
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
"""

FILENAME = "<path>/Chicago.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile(r'^addr:')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    created = {}
    if element.tag == "node":
        tag_list = []
        for item in element.iter("tag"):
            key = item.attrib['k']
            tag_list.append(key)
        if ('amenity' in tag_list or 'name' in tag_list) and element.get('lat') and element.get('lon'):
            pos = [float(element.attrib['lat']),float(element.attrib['lon'])] 
            node['pos'] = pos
            node['id'] = element.attrib['id']
            node['type'] = element.tag
            node['visible'] = element.get('visible')
            for key in CREATED:
                if element.get(key):
                    val = element.attrib[key]
                    created[key] = val
            node['created'] = created
            address = {}
            for item in element.iter("tag"):
                key = item.attrib['k']
                if problemchars.search(key):
                    continue
                if key.count(":") == 1:
                    idx = key.index(":")
                    if addr.search(key):
                        address[key[idx+1:]] = item.attrib['v']
                elif key.count(":") == 0:
                    node[key] = item.attrib['v']
            if len(address) > 0:
                node['address'] = address
            return node
        else:
            return None
    else:
        return None

"""
This function dumps the parsed data into a JSON file. It also treturns a list of JSON docs that can be directly inserted into MongoDB
"""
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "chicago_output.json"
    data = []
    i = 0
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                i += 1
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data

if __name__ == "__main__":
    data = process_map(FILENAME, False)
