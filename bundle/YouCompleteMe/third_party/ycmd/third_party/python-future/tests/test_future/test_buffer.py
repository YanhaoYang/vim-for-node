# Tests that work for both bytes and buffer objects.
# See PEP 3137.

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *
from future.tests.base import unittest, expectedFailurePY26

import struct
import sys


class MixinBytesBufferCommonTests(object):
    """Tests that work for both bytes and buffer objects.
    See PEP 3137.
    """

    def marshal(self, x):
        """Convert x into the appropriate type for these tests."""
        raise RuntimeError('test class must provide a marshal method')

    def test_islower(self):
        self.assertFalse(self.marshal(b'').islower())
        self.assertTrue(self.marshal(b'a').islower())
        self.assertFalse(self.marshal(b'A').islower())
        self.assertFalse(self.marshal(b'\n').islower())
        self.assertTrue(self.marshal(b'abc').islower())
        self.assertFalse(self.marshal(b'aBc').islower())
        self.assertTrue(self.marshal(b'abc\n').islower())
        self.assertRaises(TypeError, self.marshal(b'abc').islower, 42)

    def test_isupper(self):
        self.assertFalse(self.marshal(b'').isupper())
        self.assertFalse(self.marshal(b'a').isupper())
        self.assertTrue(self.marshal(b'A').isupper())
        self.assertFalse(self.marshal(b'\n').isupper())
        self.assertTrue(self.marshal(b'ABC').isupper())
        self.assertFalse(self.marshal(b'AbC').isupper())
        self.assertTrue(self.marshal(b'ABC\n').isupper())
        self.assertRaises(TypeError, self.marshal(b'abc').isupper, 42)

    def test_istitle(self):
        self.assertFalse(self.marshal(b'').istitle())
        self.assertFalse(self.marshal(b'a').istitle())
        self.assertTrue(self.marshal(b'A').istitle())
        self.assertFalse(self.marshal(b'\n').istitle())
        self.assertTrue(self.marshal(b'A Titlecased Line').istitle())
        self.assertTrue(self.marshal(b'A\nTitlecased Line').istitle())
        self.assertTrue(self.marshal(b'A Titlecased, Line').istitle())
        self.assertFalse(self.marshal(b'Not a capitalized String').istitle())
        self.assertFalse(self.marshal(b'Not\ta Titlecase String').istitle())
        self.assertFalse(self.marshal(b'Not--a Titlecase String').istitle())
        self.assertFalse(self.marshal(b'NOT').istitle())
        self.assertRaises(TypeError, self.marshal(b'abc').istitle, 42)

    def test_isspace(self):
        self.assertFalse(self.marshal(b'').isspace())
        self.assertFalse(self.marshal(b'a').isspace())
        self.assertTrue(self.marshal(b' ').isspace())
        self.assertTrue(self.marshal(b'\t').isspace())
        self.assertTrue(self.marshal(b'\r').isspace())
        self.assertTrue(self.marshal(b'\n').isspace())
        self.assertTrue(self.marshal(b' \t\r\n').isspace())
        self.assertFalse(self.marshal(b' \t\r\na').isspace())
        self.assertRaises(TypeError, self.marshal(b'abc').isspace, 42)

    def test_isalpha(self):
        self.assertFalse(self.marshal(b'').isalpha())
        self.assertTrue(self.marshal(b'a').isalpha())
        self.assertTrue(self.marshal(b'A').isalpha())
        self.assertFalse(self.marshal(b'\n').isalpha())
        self.assertTrue(self.marshal(b'abc').isalpha())
        self.assertFalse(self.marshal(b'aBc123').isalpha())
        self.assertFalse(self.marshal(b'abc\n').isalpha())
        self.assertRaises(TypeError, self.marshal(b'abc').isalpha, 42)

    def test_isalnum(self):
        self.assertFalse(self.marshal(b'').isalnum())
        self.assertTrue(self.marshal(b'a').isalnum())
        self.assertTrue(self.marshal(b'A').isalnum())
        self.assertFalse(self.marshal(b'\n').isalnum())
        self.assertTrue(self.marshal(b'123abc456').isalnum())
        self.assertTrue(self.marshal(b'a1b3c').isalnum())
        self.assertFalse(self.marshal(b'aBc000 ').isalnum())
        self.assertFalse(self.marshal(b'abc\n').isalnum())
        self.assertRaises(TypeError, self.marshal(b'abc').isalnum, 42)

    def test_isdigit(self):
        self.assertFalse(self.marshal(b'').isdigit())
        self.assertFalse(self.marshal(b'a').isdigit())
        self.assertTrue(self.marshal(b'0').isdigit())
        self.assertTrue(self.marshal(b'0123456789').isdigit())
        self.assertFalse(self.marshal(b'0123456789a').isdigit())

        self.assertRaises(TypeError, self.marshal(b'abc').isdigit, 42)

    def test_lower(self):
        self.assertEqual(bytes(b'hello'), self.marshal(b'HeLLo').lower())
        self.assertEqual(bytes(b'hello'), self.marshal(b'hello').lower())
        self.assertRaises(TypeError, self.marshal(b'hello').lower, 42)

    def test_upper(self):
        self.assertEqual(bytes(b'HELLO'), self.marshal(b'HeLLo').upper())
        self.assertEqual(bytes(b'HELLO'), self.marshal(b'HELLO').upper())
        self.assertRaises(TypeError, self.marshal(b'hello').upper, 42)

    def test_capitalize(self):
        self.assertEqual(bytes(b' hello '), self.marshal(b' hello ').capitalize())
        self.assertEqual(bytes(b'Hello '), self.marshal(b'Hello ').capitalize())
        self.assertEqual(bytes(b'Hello '), self.marshal(b'hello ').capitalize())
        self.assertEqual(bytes(b'Aaaa'), self.marshal(b'aaaa').capitalize())
        self.assertEqual(bytes(b'Aaaa'), self.marshal(b'AaAa').capitalize())

        self.assertRaises(TypeError, self.marshal(b'hello').capitalize, 42)

    def test_ljust(self):
        self.assertEqual(bytes(b'abc       '), self.marshal(b'abc').ljust(10))
        self.assertEqual(bytes(b'abc   '), self.marshal(b'abc').ljust(6))
        self.assertEqual(bytes(b'abc'), self.marshal(b'abc').ljust(3))
        self.assertEqual(bytes(b'abc'), self.marshal(b'abc').ljust(2))
        self.assertEqual(bytes(b'abc*******'), self.marshal(b'abc').ljust(10, b'*'))
        self.assertRaises(TypeError, self.marshal(b'abc').ljust)

    def test_rjust(self):
        self.assertEqual(bytes(b'       abc'), self.marshal(b'abc').rjust(10))
        self.assertEqual(bytes(b'   abc'), self.marshal(b'abc').rjust(6))
        self.assertEqual(bytes(b'abc'), self.marshal(b'abc').rjust(3))
        self.assertEqual(bytes(b'abc'), self.marshal(b'abc').rjust(2))
        self.assertEqual(bytes(b'*******abc'), self.marshal(b'abc').rjust(10, b'*'))
        self.assertRaises(TypeError, self.marshal(b'abc').rjust)

    def test_center(self):
        self.assertEqual(bytes(b'   abc    '), self.marshal(b'abc').center(10))
        self.assertEqual(bytes(b' abc  '), self.marshal(b'abc').center(6))
        self.assertEqual(bytes(b'abc'), self.marshal(b'abc').center(3))
        self.assertEqual(bytes(b'abc'), self.marshal(b'abc').center(2))
        self.assertEqual(bytes(b'***abc****'), self.marshal(b'abc').center(10, b'*'))
        self.assertRaises(TypeError, self.marshal(b'abc').center)

    def test_swapcase(self):
        self.assertEqual(bytes(b'hEllO CoMPuTErS'),
            self.marshal(bytes(b'HeLLo cOmpUteRs')).swapcase())

        self.assertRaises(TypeError, self.marshal(b'hello').swapcase, 42)

    def test_zfill(self):
        self.assertEqual(bytes(b'123'), self.marshal(b'123').zfill(2))
        self.assertEqual(bytes(b'123'), self.marshal(b'123').zfill(3))
        self.assertEqual(bytes(b'0123'), self.marshal(b'123').zfill(4))
        self.assertEqual(bytes(b'+123'), self.marshal(b'+123').zfill(3))
        self.assertEqual(bytes(b'+123'), self.marshal(b'+123').zfill(4))
        self.assertEqual(bytes(b'+0123'), self.marshal(b'+123').zfill(5))
        self.assertEqual(bytes(b'-123'), self.marshal(b'-123').zfill(3))
        self.assertEqual(bytes(b'-123'), self.marshal(b'-123').zfill(4))
        self.assertEqual(bytes(b'-0123'), self.marshal(b'-123').zfill(5))
        self.assertEqual(bytes(b'000'), self.marshal(b'').zfill(3))
        self.assertEqual(bytes(b'34'), self.marshal(b'34').zfill(1))
        self.assertEqual(bytes(b'0034'), self.marshal(b'34').zfill(4))

        self.assertRaises(TypeError, self.marshal(b'123').zfill)

    def test_expandtabs(self):
        self.assertEqual(bytes(b'abc\rab      def\ng       hi'),
                         self.marshal(b'abc\rab\tdef\ng\thi').expandtabs())
        self.assertEqual(bytes(b'abc\rab      def\ng       hi'),
                         self.marshal(b'abc\rab\tdef\ng\thi').expandtabs(8))
        self.assertEqual(bytes(b'abc\rab  def\ng   hi'),
                         self.marshal(b'abc\rab\tdef\ng\thi').expandtabs(4))
        self.assertEqual(bytes(b'abc\r\nab  def\ng   hi'),
                         self.marshal(b'abc\r\nab\tdef\ng\thi').expandtabs(4))
        self.assertEqual(bytes(b'abc\rab      def\ng       hi'),
                         self.marshal(b'abc\rab\tdef\ng\thi').expandtabs())
        self.assertEqual(bytes(b'abc\rab      def\ng       hi'),
                         self.marshal(b'abc\rab\tdef\ng\thi').expandtabs(8))
        self.assertEqual(bytes(b'abc\r\nab\r\ndef\ng\r\nhi'),
            self.marshal(b'abc\r\nab\r\ndef\ng\r\nhi').expandtabs(4))
        self.assertEqual(bytes(b'  a\n b'), self.marshal(b' \ta\n\tb').expandtabs(1))

        self.assertRaises(TypeError, self.marshal(b'hello').expandtabs, 42, 42)
        # This test is only valid when sizeof(int) == sizeof(void*) == 4.
        if sys.maxsize < (1 << 32) and struct.calcsize('P') == 4:
            self.assertRaises(OverflowError,
                              self.marshal(b'\ta\n\tb').expandtabs, sys.maxsize)

    def test_title(self):
        self.assertEqual(bytes(b' Hello '), self.marshal(b' hello ').title())
        self.assertEqual(bytes(b'Hello '), self.marshal(b'hello ').title())
        self.assertEqual(bytes(b'Hello '), self.marshal(b'Hello ').title())
        self.assertEqual(bytes(b'Format This As Title String'),
                         self.marshal(b'fOrMaT thIs aS titLe String').title())
        self.assertEqual(bytes(b'Format,This-As*Title;String'),
                         self.marshal(b'fOrMaT,thIs-aS*titLe;String').title())
        self.assertEqual(bytes(b'Getint'), self.marshal(b'getInt').title())
        self.assertRaises(TypeError, self.marshal(b'hello').title, 42)

    def test_splitlines(self):
        self.assertEqual([bytes(b'abc'), bytes(b'def'), bytes(b''), bytes(b'ghi')],
                         self.marshal(b'abc\ndef\n\rghi').splitlines())
        self.assertEqual([bytes(b'abc'), bytes(b'def'), bytes(b''), bytes(b'ghi')],
                         self.marshal(b'abc\ndef\n\r\nghi').splitlines())
        self.assertEqual([bytes(b'abc'), bytes(b'def'), bytes(b'ghi')],
                         self.marshal(b'abc\ndef\r\nghi').splitlines())
        # TODO: add bytes calls around these too ...
        self.assertEqual([b'abc', b'def', b'ghi'],
                         self.marshal(b'abc\ndef\r\nghi\n').splitlines())
        self.assertEqual([b'abc', b'def', b'ghi', b''],
                         self.marshal(b'abc\ndef\r\nghi\n\r').splitlines())
        self.assertEqual([b'', b'abc', b'def', b'ghi', b''],
                         self.marshal(b'\nabc\ndef\r\nghi\n\r').splitlines())
        self.assertEqual([b'', b'abc', b'def', b'ghi', b''],
                         self.marshal(b'\nabc\ndef\r\nghi\n\r').splitlines(False))
        self.assertEqual([b'\n', b'abc\n', b'def\r\n', b'ghi\n', b'\r'],
                         self.marshal(b'\nabc\ndef\r\nghi\n\r').splitlines(True))
        self.assertEqual([b'', b'abc', b'def', b'ghi', b''],
                         self.marshal(b'\nabc\ndef\r\nghi\n\r').splitlines(False))
        self.assertEqual([b'\n', b'abc\n', b'def\r\n', b'ghi\n', b'\r'],
                         self.marshal(b'\nabc\ndef\r\nghi\n\r').splitlines(True))

        self.assertRaises(TypeError, self.marshal(b'abc').splitlines, 42, 42)


# From Python-3.3.5/Lib/test/test_bytes.py:

class BytearrayPEP3137Test(unittest.TestCase,
                           MixinBytesBufferCommonTests):
    def marshal(self, x):
        return bytearray(bytes(x))

    @expectedFailurePY26
    def test_returns_new_copy(self):
        val = self.marshal(b'1234')
        # On immutable types these MAY return a reference to themselves
        # but on mutable types like bytearray they MUST return a new copy.
        for methname in ('zfill', 'rjust', 'ljust', 'center'):
            method = getattr(val, methname)
            newval = method(3)
            self.assertEqual(val, newval)
            self.assertTrue(val is not newval,
                            methname+' returned self on a mutable object')
        for expr in ('val.split()[0]', 'val.rsplit()[0]',
                     'val.partition(b".")[0]', 'val.rpartition(b".")[2]',
                     'val.splitlines()[0]', 'val.replace(b"", b"")'):
            newval = eval(expr)
            self.assertEqual(val, newval)
            self.assertTrue(val is not newval,
                            expr+' returned val on a mutable object')



if __name__ == '__main__':
    unittest.main()
