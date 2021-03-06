#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals
import unittest, re, os, tempfile, shutil

from plasTeX.TeX import TeX
from unittest import TestCase


from hamcrest import assert_that
from hamcrest import has_length
from hamcrest import is_
#from hamcrest import same_instance

from . import BeautifulSoup as Soup
from . import _run_plastex

class RunLongtablesLayer(object):
    """
    To run longtables in their own parallel layer.
    """

class TestLongtables(TestCase):
    layer = RunLongtablesLayer
    level = 3 # Extremely slow, especially testFooters

    def runDocument(self, content):
        """
        Compile a document with the given content

        Arguments:
        content - string containing the content of the document

        Returns: TeX document

        """
        tex = TeX()
        tex.disableLogging()
        tex.input('\\document{article}\\usepackage{longtable}\\begin{document}%s\\end{document}' % content)
        return tex.parse()

    def runTable(self, content):
        """
        This method compiles and renders a document fragment and
        returns the result

        Arguments:
        content - string containing the document fragment

        Returns: content of output file

        """
        # Create document file
        document = '\\documentclass{article}\\usepackage{longtable}\\begin{document}%s\\end{document}' % content
        tmpdir = tempfile.mkdtemp()
        oldpwd = os.path.abspath(os.getcwd())
        try:
            os.chdir(tmpdir)
            filename = os.path.join(tmpdir, 'longtable.tex')
            with open(filename, 'wb') as f:
                f.write(document.encode('utf-8'))

            log = _run_plastex(tmpdir, filename)

            # Get output file
            index_file = os.path.join(tmpdir, 'index.html')
            if not os.path.exists(index_file):
                raise ValueError(log)

            with open(index_file, 'rb') as f:
                output = f.read()
        finally:
            # Clean up
            shutil.rmtree(tmpdir)
            os.chdir(oldpwd)
        return Soup(output).find('table', 'tabular')

    def testSimple(self):
        # Table with no bells or whistles
        out = self.runTable(r'''\begin{longtable}{lll} 1 & 2 & 3 \\ a & b & c \\\end{longtable}''')

        all_rows = out.findAll('tr')
        assert_that( all_rows, has_length( 2 ), 'Wrong number of rows (expecting 2, but got %s): %s' % (len(all_rows), out) )

        numcols = len(out.findAll('tr')[0].findAll('td'))
        assert numcols == 3, 'Wrong number of columns (expecting 3, but got %s): %s' % (numcols, out)

        numcols = len(out.findAll('tr')[1].findAll('td'))
        assert numcols == 3, 'Wrong number of columns (expecting 3, but got %s): %s' % (numcols, out)


    def testHeaders(self):
        headers = [
            r'M & N & O \\\endhead',
            r'M & N & O \\\endfirsthead',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead',
            r'M & N & O \\\endfirsthead\n\\\endhead',
        ]

        # Each header pattern should return the same result
        for header in headers:
            out = self.runTable(r'''\begin{longtable}{lll} %s 1 & 2 & 3 \\ a & b & c \\\end{longtable}''' % header)

            numrows = len(out.findAll('tr'))
            assert numrows == 3, 'Wrong number of rows (expecting 3, but got %s) - %s - %s' % (numrows, header, out)

            headercells = out.findAll('tr')[0].findAll('th')
            numcols = len(headercells)
            assert numcols, 'No header cells found'
            assert numcols == 3, 'Wrong number of headers (expecting 3, but got %s) - %s - %s' % (numcols, header, out)
            text = [x.p.string.strip() for x in headercells]
            assert text[0]=='M','Cell should contain M, but contains %s' % text[0]
            assert text[1]=='N','Cell should contain N, but contains %s' % text[1]
            assert text[2]=='O','Cell should contain O, but contains %s' % text[2]

            numcols = len(out.findAll('tr')[1].findAll('td'))
            assert numcols == 3, 'Wrong number of columns (expecting 3, but got %s) - %s - %s' % (numcols, header, out)

    def testFooters(self):
        footers = [
            # Test \endfoot
            r'M & N & O \\\endhead F & G & H \\\endfoot',
            r'M & N & O \\\endfirsthead F & G & H \\\endfoot',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead F & G & H \\\endfoot',
            r'M & N & O \\\endfirsthead\n\\\endhead F & G & H \\\endfoot',
            r'M & N & O \\\endhead F & G & H \\\endfoot',
            r'M & N & O \\\endfirsthead F & G & H \\\endfoot',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead F & G & H \\\endfoot',
            r'M & N & O \\\endfirsthead\n\\\endhead F & G & H \\\endfoot',

            # Test \endlastfoot
            r'M & N & O \\\endhead F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n\\\endhead F & G & H \\\endlastfoot',
            r'M & N & O \\\endhead F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n\\\endhead F & G & H \\\endlastfoot',

            # Test both \endfoot and \endlastfoot
            r'M & N & O \\\endhead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n\\\endhead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endhead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n X & Y & Z \\\endhead I & J & K \\\endfoot F & G & H \\\endlastfoot',
            r'M & N & O \\\endfirsthead\n\\\endhead I & J & K \\\endfoot F & G & H \\\endlastfoot',
        ]

        # Each footer pattern should return the same result
        for footer in footers:
            out = self.runTable(r'''\begin{longtable}{lll} %s 1 & 2 & 3 \\ a & b & c \\\end{longtable}''' % footer)

            numrows = len(out.findAll('tr'))
            assert numrows == 4, 'Wrong number of rows (expecting 4, but got %s) - %s - %s' % (numrows, footer, out)

            headercells = out.findAll('tr')[-1].findAll('th')
            numcols = len(headercells)
            assert numcols, 'No header cells found'
            assert numcols == 3, 'Wrong number of headers (expecting 3, but got %s) - %s - %s' % (numcols, footer, out)
            text = [x.p.string.strip() for x in headercells]
            assert text[0]=='F','Cell should contain F, but contains %s' % text[0]
            assert text[1]=='G','Cell should contain G, but contains %s' % text[1]
            assert text[2]=='H','Cell should contain H, but contains %s' % text[2]

            numcols = len(out.findAll('tr')[1].findAll('td'))
            assert numcols == 3, 'Wrong number of columns (expecting 3, but got %s) - %s - %s' % (numcols, footer, out)

    def testCaptionNodes(self):
        captions = [
            r'\caption{Caption Text}\\',
            r'\caption{Caption Text}\\ A & B & C \\\endfirsthead',
            r'''\caption{Caption Text}\\ A & B & C \\\endfirsthead
                \caption{Next Caption Text}\\ X & Y & Z \\\endhead''',
        ]

        for caption in captions:
            doc = self.runDocument(r'''\begin{longtable}{lll} %s 1 & 2 & 3 \end{longtable}''' % caption)

            # Make sure that we only have one caption, which is not
            # in the DOM
            src = caption
            caption = doc.getElementsByTagName('caption')
            assert_that( caption, has_length( 0 ), "Given %s" % src )
            longtables = doc.getElementsByTagName('longtable')
            caption = longtables[0].title

            # Make sure that the caption node matches the caption on the table
            assert caption is not None, 'Caption is empty'

            # JAM: table.caption refers to the /class/
            #table = doc.getElementsByTagName('longtable')[0]
            #assert table.caption is not None, 'Table caption is empty'
            #assert_that( table.caption, is_(same_instance( caption ) ), 'Caption does not match table caption' )

            # JAM: This relation does not hold
            # Make sure that the caption is the sibling of the caption
            #assert table.previousSibling is caption, 'Previous sibling is not the caption'
            #assert caption.nextSibling is table, 'Next sibling is not the table'

            # Make sure that we got the right caption
            text = caption.textContent.strip()
            assert text == 'Caption Text', 'Caption text should be "Caption Text", but is "%s"' % text

    def testKill(self):
        doc = self.runDocument(r'''\begin{longtable}{lll} 1 & 2 & 3 \\ longtext & & \kill\end{longtable}''')

        table = doc.getElementsByTagName('longtable')[0]
        rows = table.getElementsByTagName('ArrayRow')
        assert_that( rows, has_length( 1 ), 'There should be only 1 row, but found %s' % len(rows) )
        content = re.sub(r'\s+', r' ', rows[0].textContent.strip())
        assert_that( content, is_( '1 2 3' ) )


if __name__ == '__main__':
    unittest.main()
