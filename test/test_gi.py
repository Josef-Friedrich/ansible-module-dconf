# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division)
from ansible.compat.tests import unittest
# import unittest
import mock
import dconf
import gi
import os
from gi.repository import Gio, GLib

gi.require_version('Gtk', '3.0')

class TestUnitTest(unittest.TestCase):

    def test_get_value(self):
        # Gio.Settings.list_schemas()
        # travis: 'org.freedesktop.ColorHelper', 'org.gtk.Settings.ColorChooser', 'org.gtk.Settings.FileChooser'
        # self.assertEqual(Gio.Settings.list_schemas(), True)

        # local and travis: 'display-gamma', 'profile-upload-uri', 'display-whitepoint', 'sample-delay'
        #self.assertEqual(Gio.Settings('org.freedesktop.ColorHelper').list_keys(), True)

        self.assertEqual(str(Gio.Settings('org.freedesktop.ColorHelper').get_value('sample-delay')), '400')


    def test_new_schema(self):
        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            directory=os.path.abspath(os.path.join('test', 'schemas')),
            parent=Gio.SettingsSchemaSource.get_default(),
            trusted=False,
        )
        schema = schema_source.lookup(schema_id='rocks.friedrich.test', recursive=False)
        settings = Gio.Settings.new_full(schema, None, None)
        settings.set_boolean('mybool', True)
        self.assertEqual(str(settings.get_value('mybool')), 'true')
        settings.set_string('mystring', 'troll')
        self.assertEqual(str(settings.get_value('mystring')), "'troll'")
