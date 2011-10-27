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
from BindFile import BindFile
import re
import datetime, time
class BindFileTest(unittest.TestCase):

    def setUp(self):
        self.bf = BindFile()

    def tearDown(self):
        self.bf = None

    def test_initial(self):
        self.assertNotEqual(self.bf, None)

    def test_initial_serial(self):
        self.assertEqual(self.bf.serial, self.bf.default_serial)

    def test_initial_name(self):
        self.assertEqual(self.bf.name, "@")

    def test_get_date_stamp(self):
        self.assertEqual(self.bf._date_stamp, datetime.date.today().strftime('%Y%m%d'))

    def test_get_default_serial(self):
        self.assertEqual(self.bf.default_serial, "%s%s" %(datetime.date.today().strftime('%Y%m%d'), "00") )
    
    def test_increment_serial(self):
        self.assertEqual(self.bf.increment_serial(2000102100), int("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "00")) )

    def test_increment_serial_more_than_10(self):
        self.assertEqual(self.bf.increment_serial("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "11")), int("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "12")) )

    def test_increment_serial_less_than_10(self):
        self.assertEqual(self.bf.increment_serial("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "01")), int("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "02")) )

    def test_increment_serial_00(self):
        self.assertEqual(self.bf.increment_serial("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "00")), int("%s%s" %(datetime.date.today().strftime('%Y%m%d'), "01")) )

    def test_generate_header(self):
        self.bf.generate_file()
        self.assertEqual(self.bf._header_text,"$TTL 3600\n")

    def test_generate_default_declaration(self):
        self.bf.generate_file()
        self.assertEqual(self.bf._declaration_text,"@ IN SOA ns1.mozilla.com. ns2.mozilla.com. (\n\t%s%s\n\t10800\n\t3600\n\t604800\n\t1800\n) IN NS ns1.mozilla.com." % (datetime.date.today().strftime('%Y%m%d'), "00") )

    def test_generate_updated_retry_declaration(self):
        self.bf.refresh = 99999
        self.bf.generate_file()
        self.assertEqual(self.bf._declaration_text,"@ IN SOA ns1.mozilla.com. ns2.mozilla.com. (\n\t%s%s\n\t99999\n\t3600\n\t604800\n\t1800\n) IN NS ns1.mozilla.com." % (datetime.date.today().strftime('%Y%m%d'), "00") )

    def test_entry_list(self):
        self.bf.generate_file()
        self.assertEqual(len(self.bf.entry_list), 256)
        self.assertEqual(self.bf.entry_list[0],"IN PTR unused-10-8-0-0.phx.mozilla.com.")
        self.assertEqual(self.bf.entry_list[-1],"IN PTR unused-10-8-0-255.phx.mozilla.com.")

    """def test_merge(self):
        self.bf.merge_list.append({'index':0, 'entry':'IN PTR foo.bar.mozilla.com'})
        self.bf.generate_file()
        self.assertEqual(self.bf.entry_list[0], 'IN PTR foo.bar.mozilla.com')
        self.assertEqual(self.bf.entry_list[1], 'IN PTR unused-10-8-0-1.phx.mozilla.com.')"""

    def test_set_entry(self):
        self.bf.generate_file()
        self.bf.set_entry(0, 'IN PTR foo.bar.mozilla.com')
        self.assertEqual(self.bf.entry_list[0], 'IN PTR foo.bar.mozilla.com')
        self.assertEqual(self.bf.entry_list[1], 'IN PTR unused-10-8-0-1.phx.mozilla.com.')
        self.assertEqual(self.bf.entry_list[2], 'IN PTR unused-10-8-0-2.phx.mozilla.com.')
        self.assertEqual(len(self.bf.entry_list), 256)

    def test_calculate_previous_hash(self):
        self.bf.generate_file()
        self.bf._calculate_previous_hash()
        self.assertEqual(self.bf.previous_hash, '06766d21490b7c9fca2f13210e76ca8c')

    ## Calculate the hash of the default file before any changes
    def test_calculate_current_hash(self):
        self.bf.generate_file()
        self.bf._calculate_current_hash()
        self.assertEqual(self.bf.current_hash, '06766d21490b7c9fca2f13210e76ca8c')

    def test_compare_hash_with_updates(self):
        self.bf.generate_file()
        self.bf._calculate_current_hash()
        self.bf._calculate_previous_hash()
        self.assertEqual(self.bf.current_hash, self.bf.previous_hash)
        self.bf.set_entry(5, 'IN PTR foo.bar.mozilla.com')
        self.bf.generate_file()
        self.bf._calculate_current_hash()
        self.bf._calculate_previous_hash()
        self.assertEqual('42ef3fbdc9c82e96ed1f54c4466eae53', self.bf.current_hash)
        self.assertNotEqual(self.bf.current_hash, self.bf.previous_hash)

