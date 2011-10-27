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

import datetime, time
try:
    import hashlib as md5
except:
    import md5
class BindFile:
    name = "@"
    ttl = 3600
    file_class = "IN"
    soa = "ns1.mozilla.com. ns2.mozilla.com."
    nameservers = ["ns1.mozilla.com."]
    serial = "%s%s" % (datetime.date.today().strftime('%Y%m%d'), '00')
    refresh = 10800
    retry = 3600
    expire = 604800
    min = 1800
    header_options = ['$TTL 3600']
    default_placeholder = "IN PTR unused-10-8-0-%i.phx.mozilla.com."
    entry_list = []
    _entry_output = ""
    previous_hash = ""
    current_hash = ""
    ##Merge list will be a list of dictionary objects. The dictionary will be structured as follows {'index':0,'entry':'hostname entry as to overwrite the default'}
    merge_list = []
    output_file = ""
    previous_md5_hash = ""
    current_md5_hash = ""
    filename = "0.8.10.in-addr.arpa"
    def __init__(self):
        self._header_text = ""
        self._declaration_text = ""
        self.entry_list = []
        

    def generate_file(self, output=False):
        self._generate_header()
        self._generate_declaration()
        self._build_entry_list()
        self._output_entry_list()
        if self.output_file != "":
            self.output_file = ""
        self.output_file += self._header_text
        self.output_file += self._declaration_text
        self.output_file += self._declaration_break
        self.output_file += self._entry_output

        if output is True:
            print self.output_file

    def write_file(self):
        fh = open(self.filename, 'w')
        fh.write(self.output_file)
        fh.close()

    @property
    def _declaration_break(self):
        return "\n;PAGEBREAK\n"

    def _merge_lists(self):
        if len(self.merge_list) > 0:
            for line in self.merge_list:
                self.entry_list[line['index']] = line['entry']

    def _generate_header(self):
        self._header_text = "\n".join(self.header_options)
        self._header_text += "\n"

    def _generate_declaration(self):
        self._declaration_text = "%s %s SOA %s (\n\t%s\n\t%i\n\t%i\n\t%i\n\t%i\n) IN NS %s" % (self.name, self.file_class, self.soa, self.serial, self.refresh, self.retry, self.expire, self.min, "\nIN NS ".join(self.nameservers) )

    def build_entry_list(self):
        self._build_entry_list()

    def _build_entry_list(self):
        for i in range(0,256):
            self.entry_list.append(self.default_placeholder % i)

    def _output_entry_list(self):
        counter = 0
        for i in self.entry_list:
            self._entry_output += "\n%i %s" % (counter, i)
            counter += 1
    def set_entry(self, index, value):
        try:
            self.entry_list[index] = value
        except Exception, e:
            print "Exception is %s" % (e)

    def _calculate_previous_hash(self):
        calculate_text = open(self.filename).read().split(self._declaration_break)[1].strip()
        self.previous_hash = md5.md5(calculate_text).hexdigest()

    def _calculate_current_hash(self):
        calculate_text = self.output_file.split(self._declaration_break)[1].strip()
        self.current_hash = md5.md5(calculate_text).hexdigest()

    @property
    def _date_stamp(self):
        return datetime.date.today().strftime('%Y%m%d')

    @property
    def default_serial(self):
        return "%s%s" % (self._date_stamp,"00")

    def increment_serial(self, input_serial=None):
        if input_serial is None:
            input_serial = self.serial
        input_serial = str(input_serial)
        input_date = input_serial[:8]
        input_counter = int(input_serial[-2:])
        ## Test if the current_serial date stamp matches the current date
        ## If not just return the date stamp with 00 appended
        if int(input_date) < int(self._date_stamp):
            return_serial = "%s%s" % (self._date_stamp, "00")
        elif int(input_date) == int(self._date_stamp):
            input_counter += 1
            if input_counter < 10:
                incremented_counter = "0%i" % (input_counter)
            else:
                incremented_counter = input_counter
            return_serial = "%s%s" % (input_date, incremented_counter)
        else:
            return_serial = input_serial
        return int(return_serial)
        








