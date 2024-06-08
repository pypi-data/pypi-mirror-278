if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.file_utils import auto_rename


def tests():
    print('test file utils')
    cat_path = rc_dir / 'cat.png'
    renamed_cat_path = str(cat_path).replace('.png', '(1).png')
    print(renamed_cat_path)
    assert auto_rename(cat_path) == Path(renamed_cat_path)
    assert auto_rename(str(cat_path)) == renamed_cat_path


if __name__ == '__main__':
    tests()
