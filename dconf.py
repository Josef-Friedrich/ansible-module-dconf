#!/usr/bin/python

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
            'schema': {'required': True},
            'key': {'required': True},
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
