#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904

import unittest

from hamcrest import assert_that
from hamcrest import is_

from six.moves import cPickle as pickle

from plasTeX.Config import newConfig

class TestConfig(unittest.TestCase):

    def test_can_pickle(self):
        c = newConfig( read_files=False )
        s = pickle.dumps( c, pickle.HIGHEST_PROTOCOL )

        assert_that( pickle.loads( s ), is_( c ) )
