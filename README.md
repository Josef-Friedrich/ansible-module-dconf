# ansible-module-dconf

```
> DCONF

  dconf https://wiki.gnome.org/Projects/dconf and gsettings are command line
  utilities to manage configurations for the gnome desktop.

Options (= is mandatory):

= key
        The name of the key.
        E. g.: dash-max-icon-size

= schema
        E. g.: org.gnome.shell.extensions.dash-to-dock

= value
        The name of the schema.
        string value: BOTTOM
        integer values: 46
        boolean values: yes, no, true, false


EXAMPLES:


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

RETURN VALUES:


key:
    description: The name of the key.
    returned: always
    type: string
    sample: dash-max-icon-size
new_value:
    description: The new value in the serialized Gvariant format.
    returned: always
    type: string
    sample: 'BOTTOM'
old_value_input:
    description: The old value as specified.
    returned: always
    type: string
    sample: BOTTOM
old_value:
    description: The old value in the serialized Gvariant format.
    returned: always
    type: string
    sample: 'BOTTOM'
schema:
    description: The name of the schema.
    returned: always
    type: string
    sample: org.gnome.shell.extensions.dash-to-dock


MAINTAINERS: Josef Friedrich (@Josef-Friedrich)

METADATA:
	Status: ['preview']
	Supported_by: community
```

# Development

## Test functionality

```
/usr/local/src/ansible/hacking/test-module -m dconf.py -a
```

## Test documentation

```
source /usr/local/src/ansible/hacking/env-setup
/usr/local/src/ansible/test/sanity/validate-modules/validate-modules --arg-spec --warnings dconf.py
```

## Generate documentation

```
ansible-doc -M . dconf
```
