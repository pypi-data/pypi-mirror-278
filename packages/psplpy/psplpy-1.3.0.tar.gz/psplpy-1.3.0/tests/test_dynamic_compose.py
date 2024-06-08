if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.dynamic_compose import DynamicCompose

dc_rc_dir = rc_dir / 'dynamic_compose'
dc_compose_dir = dc_rc_dir / '.compose'
compose_dumped_file = dc_compose_dir / 'compose-dumped.yml'
dockerfile_dumped_file = dc_compose_dir / 'Dockerfile-dumped'


def tests():
    DynamicCompose.CWD = dc_rc_dir
    dc = DynamicCompose()
    print(dc.env)
    dc.compose_dir = dc_compose_dir

    dc.format_compose()
    dc.format_dockerfile()
    dc.dump()

    assert compose_dumped_file.read_text().strip() == dc.compose_file.read_text().strip()
    # dc.compose_file.unlink()
    assert dockerfile_dumped_file.read_text().strip() == dc.dockerfile_file.read_text().strip()
    # dc.dockerfile_file.unlink()

    dc.up()


if __name__ == '__main__':
    tests()
