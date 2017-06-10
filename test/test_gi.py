# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division)
from ansible.compat.tests import unittest
# import unittest
import mock
import dconf
import gi
from gi.repository import Gio, GLib

gi.require_version('Gtk', '3.0')

class TestUnitTest(unittest.TestCase):

    def test_unit(self):
        Gio.Settings.list_schemas()
        self.assertEqual(Gio.Settings.list_schemas(), True)
