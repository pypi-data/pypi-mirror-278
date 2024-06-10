# The problem

Say you have a configuration file, or command line options, or
[whatever].  And you want to have user-specified elements reference
deep portions of a structure that you've defined, read in from yaml or
json, or [whatever].  How?

# This solution

(because there are likely others)

Users don't understand complex syntax, so this makes it easy to
access deep dict or arrays with keys and numbers separated by a "."
character.

# A working demonstration

``` python
import dotnest

data = {
    'subdict': {
        'arrrr': ["there", "she", "blows",]
    },
    'list': [
        {'name': 'element1'}, {'name': 'element2'}
    ]
}

dn = dotnest.DotNest(data)
print(dn.get("subdict.arrrr.1"))       # she
print(dn.get("list.1.name"))           # element1

dn.set("subdict.newentry", "bar")
print(dn.get("subdict.newentry"))      # bar
print(dn.get("list.0"))                # {'name': 'element1'}
```

# Used by

This class can be best married with tools that read in and need to
referenc YAML or JSON as mentioned.  As such, the original source of
this effort comes from the package that converts from a netbox nestetd
structure to ansible: [nb2an].

[nb2an]: https://github.com/hardaker/nb2an
[whatever]: https://en.wikipedia.org/wiki/Special:Random
