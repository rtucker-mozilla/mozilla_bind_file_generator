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
        pass

    def test_initial(self):
        bf = BindFile() 
        self.assertNotEqual(bf, None)

    def test_initial_serial(self):
        bf = BindFile() 
        self.assertEqual(bf.serial, bf.default_serial)

    def test_initial_name(self):
        bf = BindFile() 
        self.assertEqual(bf.name, "@")

    def test_get_date_stamp(self):
        bf = BindFile() 
        self.assertEqual(bf._date_stamp, datetime.date.today().strftime('%Y%m%d'))

    def test_get_default_serial(self):
        bf = BindFile() 
        self.assertEqual(bf.default_serial, "%s%s" %(datetime.date.today().strftime('%Y%m%d'), "00") )
    
    def test_increment_serial(self):
        bf = BindFile() 
        self.assertEqual(bf.increment_serial(2000102100), 2011102100)

    def test_increment_serial_more_than_10(self):
        bf = BindFile() 
        self.assertEqual(bf.increment_serial(2011102111), 2011102112)

    def test_increment_serial_less_than_10(self):
        bf = BindFile() 
        self.assertEqual(bf.increment_serial(2011102101), 2011102102)

    def test_increment_serial_00(self):
        bf = BindFile() 
        self.assertEqual(bf.increment_serial(2011102100), 2011102101)

    def test_generate_header(self):
        bf = BindFile() 
        bf.generate_file()
        self.assertEqual(bf._header_text,"$TTL 3600\n")

    def test_generate_default_declaration(self):
        bf = BindFile() 
        bf.generate_file()
        self.assertEqual(bf._declaration_text,"@ IN SOA ns.mozilla.org. sysadmins.mozilla.org. (\n\t2011102100\n\t10800\n\t3600\n\t604800\n\t1800\n) IN NS ns.mozilla.org.")

    def test_generate_updated_retry_declaration(self):
        bf = BindFile() 
        bf.refresh = 99999
        bf.generate_file()
        self.assertEqual(bf._declaration_text,"@ IN SOA ns.mozilla.org. sysadmins.mozilla.org. (\n\t2011102100\n\t99999\n\t3600\n\t604800\n\t1800\n) IN NS ns.mozilla.org.")

    def test_entry_list(self):
        bf = BindFile() 
        bf._build_entry_list()
        self.assertEqual(len(bf.entry_list), 256)
        self.assertEqual(bf.entry_list[0],"IN PTR unused-10-8-0-0.phx.mozilla.com.")
        self.assertEqual(bf.entry_list[-1],"IN PTR unused-10-8-0-255.phx.mozilla.com.")

    def test_output(self):
        bf = BindFile() 
        bf.merge_list.append({'index':1, 'entry':'foo.bar.mozilla.com'})
        bf.generate_file()
        self.assertEqual(bf.entry_list[0], 'foo.bar.mozilla.com')
        self.assertEqual(bf.entry_list[1], 'IN PTR unused-10-8-0-1.phx.mozilla.com.')
