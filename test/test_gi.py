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
        # Gio.Settings.list_schemas()
        # travis: 'org.freedesktop.ColorHelper', 'org.gtk.Settings.ColorChooser', 'org.gtk.Settings.FileChooser'
        # self.assertEqual(Gio.Settings.list_schemas(), True)

        # local and travis: 'display-gamma', 'profile-upload-uri', 'display-whitepoint', 'sample-delay'
        #self.assertEqual(Gio.Settings('org.freedesktop.ColorHelper').list_keys(), True)

        self.assertEqual(str(Gio.Settings('org.freedesktop.ColorHelper').get_value('sample-delay')), '400')
