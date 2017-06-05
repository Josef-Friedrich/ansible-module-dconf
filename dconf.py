#!/usr/bin/python

import os
import subprocess
from ansible.module_utils.basic import AnsibleModule
import gi
from gi.repository import Gio, GLib
gi.require_version('Gtk', '3.0')

def set_env():
    pid = subprocess.check_output(["pgrep", "-n", "gnome-session"]).strip()
    cmd = "grep -z DBUS_SESSION_BUS_ADDRESS /proc/" + pid + "/environ | cut -d= -f2-"
    value = subprocess.check_output(['/bin/sh', '-c', cmd]).strip().replace("\0", "")
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = value

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

    schema = Gio.Settings(p['schema'])
    schema.set_value(p['key'], GLib.Variant('s', p['value']))
    output = schema.get_value(p['key'])

    module.exit_json(changed=True, msg=str(output))

if __name__ == '__main__':
    main()
