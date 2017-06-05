#!/usr/bin/python

# (c) 2017, Josef Friedrich <josef@friedrich.rocks>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dconf
short_description: Ansible module for setting dconf / gsettings entries.
description:
    - dconf U(https://wiki.gnome.org/Projects/dconf) and gsettings
      are command line utilities to manage configurations for the gnome
      desktop.

author: "Josef Friedrich (@Josef-Friedrich)"
options:
    key:
        description:
            - E. g.: dash-max-icon-size
        required: true
    schema:
        description:
            - E. g.: org.gnome.shell.extensions.dash-to-dock
        required: true
    value:
        description:
            - string value: BOTTOM
            - integer values: 46
            - boolean values: yes, no, true, false
        required: true
'''

EXAMPLES = '''
# Set a string value
- dconf:
    key: dock-position
    value: BOTTOM
    schema: org.gnome.shell.extensions.dash-to-dock

# Set a integer value
- dconf:
    key: dash-max-icon-size
    value: 64
    schema: org.gnome.shell.extensions.dash-to-dock

# Set a boolean value
- dconf:
    key: show-apps-at-top
    value: yes
    schema: org.gnome.shell.extensions.dash-to-dock
'''


import os
import subprocess
from ansible.module_utils.basic import AnsibleModule
import gi
from gi.repository import Gio, GLib
gi.require_version('Gtk', '3.0')

def g_variant(value):
    try:
        value = int(value)
        return GLib.Variant('i', value)
    except ValueError:
        pass
    if isinstance(value, str):
        if value.lower() == 'no' or value.lower() == 'false':
            return GLib.Variant('b', False)
        elif value.lower() == 'yes' or value.lower() == 'true':
            return GLib.Variant('b', True)
        else:
            return GLib.Variant('s', value)
    elif isinstance(value, list):
        return GLib.Variant('as', value)


def set_env():
    env = 'DBUS_SESSION_BUS_ADDRESS'
    proc = 'gnome-session'
    pid = subprocess.check_output(['pgrep', '-n', proc]).strip()
    cmd = 'grep -z ' + env + ' /proc/' + pid + '/environ | cut -d= -f2-'
    output = subprocess.check_output(['/bin/sh', '-c', cmd])
    os.environ[env] = output.strip().replace('\0', '')


def main():

    module = AnsibleModule(
        argument_spec={
            'key': {'required': True},
            'schema': {'required': True},
            'value': {'required': True},
        },
        supports_check_mode=True,
    )

    p = module.params

    set_env()

    changed = False
    schema = Gio.Settings(p['schema'])
    old_value = schema.get_value(p['key'])
    new_value = g_variant(p['value'])

    if old_value != new_value:
        schema.set_value(p['key'], g_variant(p['value']))
        changed = True
        new_value = schema.get_value(p['key'])

    module.exit_json(changed=changed,
                     key=p['key'],
                     schema=p['schema'],
                     old_value_input=p['value'],
                     old_value=str(old_value),
                     new_value=str(new_value))


if __name__ == '__main__':
    main()
