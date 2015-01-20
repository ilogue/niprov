#!/usr/bin/python
# -*- coding: UTF-8 -*-


class HtmlExporter(object):

    header = """
<html>
<head>
<style>
html {font-family:arial;}
td {padding: 10px;}
tr:hover {background-color:lavender;}
dt {color: dark-grey; font-style: italic; background-color:lavender; padding: 10px;}
dd {padding: 10px;}
</style>
<title>Provenance</title>
</head>
<h1>Provenance</h1>
"""
    tableheader ="""
<table>
<thead>
<tr>
<th>Acquired</th>
<th>Subject</th>
<th>Protocol</th>
<th>Path</th>
</tr>
</thead>
<tbody>
"""
    footer = '</html>'
    expectedFields = ['acquired','subject','protocol']
    allfields = ['path','ancestor','acquired','subject','protocol','transformation','code','logtext']

    def __init__(self, filesys, listener, externals):
        self.filesys = filesys
        self.listener = listener
        self.externals = externals

    def exportList(self, provenance):
        """Publish the provenance for several images in an html file and display in Firefox.

        Args:
            provenance (list): List of provenance dictionaries.
        """
        itemfmt = '<tr><td>{0[acquired]}</td><td>{0[subject]}</td><td>{0[protocol]}</td><td>{1}</td></tr>\n'
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(self.header)
            htmlfile.write(self.tableheader)
            for provitem in provenance:
                for field in self.expectedFields:
                    if not (field in provitem):
                        provitem[field] = '?'
                path = provitem['path']
                if len(path) > 42:
                    path = '..'+path[-40:]
                htmlfile.write(itemfmt.format(provitem, path))
            htmlfile.write('</tbody></table>\n')
            htmlfile.write(self.footer)
        self.externals.run(['firefox', 'provenance.html'])

    def export(self, provenance):
        """Publish the provenance for one image in an html file and display in Firefox.

        Args:
            provenance (dict): Provenance for one image file
        """
        provitem = provenance
        keyvaluefmt = '<dt>{0}</dt><dd>{1}</dd>\n'
        for field in self.expectedFields:
            if not (field in provitem):
                provitem[field] = '?'
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(self.header)
            htmlfile.write('<dl>\n')
            for field in self.allfields:
                if field in provitem:
                    htmlfile.write(keyvaluefmt.format(field, provitem[field]))
            htmlfile.write('</dl>\n')
            htmlfile.write(self.footer)
        self.externals.run(['firefox', 'provenance.html'])

