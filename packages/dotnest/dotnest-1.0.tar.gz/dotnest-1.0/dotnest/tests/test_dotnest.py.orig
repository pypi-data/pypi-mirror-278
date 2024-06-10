#!/usr/bin/python3
import copy

data = {
    'subdict': {
        'arrrr': ["there", "she", "blows",]
    },
    'list': [
        {'name': 'element1'}, {'name': 'element2'}
    ]
}


def test_dotnest():
    try:
        import dotnest
    except Exception:
        assert False, "failed to load module"

    basic_data = [1,2,3]
    dn = dotnest.DotNest(basic_data)
    assert dn.data == basic_data, "failed to have initial data value"

    dn.data = copy.deepcopy(data)
    assert dn.data == data, "reset data succeeded"


def test_dotnest_access():
    import dotnest

    dn = dotnest.DotNest(copy.deepcopy(data))
    assert dn.get(['subdict', 'arrrr', 0]) == "there"
    assert dn.get(['list', 1, 'name']) == "element2"

    dn.set(['list', 1, 'name'], "new element")
    assert dn.get(['list', 1, 'name']) == "new element"

    dn.set(['list', 1, 'name'], [1, 2, 3])
    assert dn.get(['list', 1, 'name', 2]) == 3


def test_dotnest_test_str_to_int():
    import dotnest

    dn = dotnest.DotNest(copy.deepcopy(data))
    assert dn.get(['subdict', 'arrrr', '0']) == "there"


def test_dotnest_str_to_list():
    import dotnest

    dn = dotnest.DotNest(copy.deepcopy(data))
    assert dn.parse_keys("a.b.c") == ['a', 'b', 'c']
    # .1 could be a dict string or int for a list:
    # TODO: .1 could be int for a dict too...
    assert dn.parse_keys("a.1.c") == ['a', '1', 'c']


def test_dotnest_usedotted():
    import dotnest

    dn = dotnest.DotNest(copy.deepcopy(data))
    assert dn.get('subdict.arrrr.0') == "there"
    assert dn.get('list.1.name') == "element2"

    dn.set('list.1.name', "new element")
    assert dn.get('list.1.name') == "new element"

    dn.set('list.1.name', [1, 2, 3])
    assert dn.get('list.1.name.2') == 3


def test_dotnest_equals():
    import dotnest

    dn1 = dotnest.DotNest(copy.deepcopy(data))
    dn2 = dotnest.DotNest(copy.deepcopy(data))

    assert dn1 == dn2

    dn1.set('list.1.name', 'bogus')
    assert dn1 != dn2
