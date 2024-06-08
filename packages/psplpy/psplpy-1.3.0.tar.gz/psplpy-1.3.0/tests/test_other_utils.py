if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.other_utils import is_sys, recursive_convert


def tests():
    print('test other utils')
    assert is_sys(is_sys.LINUX) is True
    assert is_sys(is_sys.WINDOWS) is False

    data = [1, (2, [3, 4])]
    assert recursive_convert(data, to=list) == [1, [2, [3, 4]]]
    assert recursive_convert(data, to=tuple) == (1, (2, (3, 4)))


if __name__ == '__main__':
    tests()
