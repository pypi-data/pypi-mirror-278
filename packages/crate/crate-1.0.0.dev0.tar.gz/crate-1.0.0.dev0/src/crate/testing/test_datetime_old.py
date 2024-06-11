# -*- coding: utf-8; -*-
#
# Licensed to CRATE Technology GmbH ("Crate") under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  Crate licenses
# this file to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
# However, if you have executed another commercial license agreement
# with Crate these terms will supersede the license and you may use the
# software solely pursuant to the terms of the relevant commercial agreement.

import os
import sys
import unittest
from datetime import datetime, date
from unittest import TestCase, mock

import time_machine


class DateTodayTest(TestCase):
    """
    `date.today()` returns the current local date, as advertised in the
    documentation [1]. Thus, it depends on the system time zone.

    The following test cases demonstrate that the test suite previously
    failed around midnight, where the UTC vs. non-UTC days overlapped,
    and when running on machines with non-UTC time zone.

    On the other hand, `datetime.utcnow().date()` works equally well in all
    situations, so we want to use that within the SQLAlchemy test cases.

    Funny enough, the problem is not observable on Linux?

    [1] https://docs.python.org/3/library/datetime.html#datetime.date.today
    """

    @mock.patch.dict(os.environ, {"TZ": "UTC"})
    @time_machine.travel("2022-07-22T00:42:00+0200")
    def test_date_today_depends_on_system_timezone_success_on_utc(self):
        today_local = date.today()
        today_utc = datetime.utcnow().date()
        self.assertEqual(today_local, today_utc)
        self.assertEqual(today_local, date(2022, 7, 21))
        self.assertEqual(today_utc, date(2022, 7, 21))

    @unittest.skipIf(sys.platform == "linux", "Problem not observable on Linux")
    @mock.patch.dict(os.environ, {"TZ": "Europe/Prague"})
    @time_machine.travel("2022-07-22T00:42:00+0200")
    def test_date_today_depends_on_system_timezone_failure_on_non_utc(self):
        today_local = date.today()
        today_utc = datetime.utcnow().date()
        self.assertNotEqual(today_local, today_utc)
        self.assertEqual(today_local, date(2022, 7, 22))
        self.assertEqual(today_utc, date(2022, 7, 21))

    @mock.patch.dict(os.environ, {"TZ": "UTC"})
    @time_machine.travel("2022-07-22T00:42:00+0200")
    def test_date_today_utc(self):
        today_local = date.today()
        self.assertEqual(today_local, date(2022, 7, 21))

    @unittest.skipIf(sys.platform == "linux", "Problem not observable on Linux")
    @mock.patch.dict(os.environ, {"TZ": "Europe/Prague"})
    @time_machine.travel("2022-07-22T00:42:00+0200")
    def test_date_today_non_utc(self):
        today_local = date.today()
        self.assertEqual(today_local, date(2022, 7, 22))

    @mock.patch.dict(os.environ, {"TZ": "UTC"})
    @time_machine.travel("2022-07-22T00:42:00+0200")
    def test_utcnow_date_utc(self):
        today_utc = datetime.utcnow().date()
        self.assertEqual(today_utc, date(2022, 7, 21))

    @mock.patch.dict(os.environ, {"TZ": "Europe/Prague"})
    @time_machine.travel("2022-07-22T00:42:00+0200")
    def test_utcnow_date_non_utc(self):
        today_utc = datetime.utcnow().date()
        self.assertEqual(today_utc, date(2022, 7, 21))
