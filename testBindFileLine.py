#!/usr/bin/python
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
#
# The Original Code is mozilla-bind-file-generator
#
# The Initial Developer of the Original Code is Rob Tucker. Portions created
# by Rob Tucker are Copyright (C) Mozilla, Inc. All Rights Reserved.
#
# Alternatively, the contents of this file may be used under the terms of the
# GNU Public License, Version 2 (the "GPLv2 License"), in which case the
# provisions of GPLv2 License are applicable instead of those above. If you
# wish to allow use of your version of this file only under the terms of the
# GPLv2 License and not to allow others to use your version of this file under
# the MPL, indicate your decision by deleting the provisions above and replace
# them with the notice and other provisions required by the GPLv2 License. If
# you do not delete the provisions above, a recipient may use your version of
# this file under either the MPL or the GPLv2 License.

from mock import Mock
import unittest
from BindFileLine import BindFileLine
import re
class BindFileTest(unittest.TestCase):

    def setUp(self):
        self.bf = BindFileLine()

    def tearDown(self):
        self.bf = None

    def test_initial(self):
        self.assertNotEqual(self.bf, None)

    def test_initial_type(self):
        self.assertEqual(self.bf.is_reverse, True)

    def test_initial_is_valid(self):
        self.assertEqual(self.bf.is_valid, False)

    def test_initial_is_valid(self):
        self.assertEqual(self.bf.is_valid, False)

    def test_initial_key_value_args_invalid(self):
        self.bf = BindFileLine()
        self.assertEqual(self.bf.is_valid, False)

    def test_initial_key_value_args(self):
        self.bf = BindFileLine(ip_address='10.0.1.1', hostname='foo.mozilla.com', is_reverse=True)
        self.assertEqual(self.bf.is_valid, True)

    def test_get_index(self):
        self.bf = BindFileLine(ip_address='10.0.1.1', hostname='foo.mozilla.com', is_reverse=True)
        self.assertEqual(self.bf._get_index(), 1)
        self.bf = BindFileLine(ip_address='10.0.1.255', hostname='foo.mozilla.com', is_reverse=True)
        self.assertEqual(self.bf._get_index(), 255)

    def test_get_output_full_hostname(self):
        self.bf = BindFileLine(ip_address='10.0.1.1', hostname='foo.mozilla.com', is_reverse=True)
        self.assertEqual(self.bf.output(), '1 IN ADDR foo.mozilla.com.')

    def test_get_output_hostname_only(self):
        self.bf = BindFileLine(ip_address='10.0.1.1', hostname='foo', is_reverse=True)
        self.assertEqual(self.bf.output(), '1 IN ADDR foo')
