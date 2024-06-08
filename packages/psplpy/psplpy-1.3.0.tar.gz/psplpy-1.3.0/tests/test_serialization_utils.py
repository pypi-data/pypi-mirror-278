import random

if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.serialization_utils import Serializer, Compressor


def tests():
    serializer = Serializer()
    serializer.compressor = Compressor(Compressor.ZLIB)

    lzma_serializer = Serializer()
    bench_data = {}
    rand_round = 10000
    for i in range(rand_round):
        bench_data[str(random.randint(0, rand_round))] = random.uniform(0, rand_round)
    p = PerfCounter()

    serialized_data = serializer.dump_pickle(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_pickle')
    serialized_data = serializer.dump_pickle(bench_data, to_b64=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_pickle(to_b64)')
    serialized_data = serializer.dump_pickle(bench_data, compress=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_pickle(zlib)')
    serialized_data = serializer.dump_pickle(bench_data, compress=True, to_b64=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_pickle(zlib, to_b64)')
    serialized_data = lzma_serializer.dump_pickle(bench_data, compress=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_pickle(lzma)')

    serialized_data = serializer.dump_json(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_json')
    serialized_data = serializer.dump_json(bench_data, compress=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_json(zlib)')
    serialized_data = lzma_serializer.dump_json(bench_data, compress=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_json(lzma)')

    serialized_data = serializer.dump_yaml(bench_data)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_yaml')
    serialized_data = serializer.dump_yaml(bench_data, compress=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_yaml(zlib)')
    serialized_data = lzma_serializer.dump_yaml(bench_data, compress=True)
    print(f'len: {len(serialized_data)},\t elapsed: {p.elapsed():.4f},\t dumps_yaml(lzma)')


    python_data = {1: '100', 2: 200, 3: ['你好', [3.14, None, False]]}

    dumps_data = serializer.dump_json(python_data, minimum=True)
    loads_data = serializer.load_json(dumps_data, trans_key_to_num=True)
    assert dumps_data == b'{"1":"100","2":200,"3":["\xe4\xbd\xa0\xe5\xa5\xbd",[3.14,null,false]]}', dumps_data
    assert loads_data == python_data

    dumps_data = serializer.dump_json(python_data, compress=True)
    loads_data = serializer.load_json(dumps_data, decompress=True, trans_key_to_num=True)
    assert dumps_data == (b"x\x9c\xab\xe6R\x00\x02%C%+ a`\xa0\xa4\x03\xe1\x1b\x01\xf9F\x06\x06P\x9e1\x90\x17\rf\x82"
                          b"\xb9O\xf6.x\xbat/T)\x08 \xe4@\xc0X\xcf\xd0D\x07E$\xaf4'\x07U$-1\xa78\x15.\x12\xcb\x05!k"
                          b"\x01E \x1ab"), dumps_data
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_pickle(loads_data)
    loads_data = serializer.load_pickle(dumps_data)
    assert dumps_data == (b'\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01\x8c\x03100\x94K\x02K\xc8K\x03]\x94('
                          b'\x8c\x06\xe4\xbd\xa0\xe5\xa5\xbd\x94]\x94(G@\t\x1e\xb8Q\xeb\x85\x1fN\x89eeu.'), loads_data
    assert loads_data == python_data

    dumps_data = serializer.dump_pickle(loads_data, compress=True, to_b64=True)
    loads_data = serializer.load_pickle(dumps_data, decompress=True, from_b64=True)
    assert dumps_data == b'eJxrYJmqzwABtVM0vBl7mA0NDKZ4M3mf8GaOnaLRw/Zk74KnS/dOAbLdHTjldgS+bpX360xNLdUDAOePE5o=', dumps_data
    assert loads_data == python_data, loads_data

    dumps_data = serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml(dumps_data)
    assert dumps_data == (b"1: '100'\n2: 200\n3:\n- \xe4\xbd\xa0\xe5\xa5\xbd\n"
                          b"- - 3.14\n  - null\n  - false\n"), dumps_data
    assert loads_data == python_data

    serializer = Serializer(path=tmp_file, data_type=dict)
    loads_data = serializer.load_json()
    assert loads_data == dict(), loads_data

    serializer.dump_json(python_data)
    loads_data = serializer.load_json(trans_key_to_num=True)
    assert loads_data == python_data, loads_data

    serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml()
    assert loads_data == python_data, loads_data

    serializer.dump_pickle(python_data)
    loads_data = serializer.load_pickle()
    assert loads_data == python_data, loads_data

    serializer = Serializer(path=tmp_file, embedded=True)
    serializer.dump_pickle(python_data, compress=True, to_b64=True)
    loads_data = serializer.load_pickle(decompress=True, from_b64=True)
    print(tmp_file.read_bytes().decode(errors='backslashreplace'))
    assert loads_data == python_data, loads_data

    serializer.dump_json(python_data)
    loads_data = serializer.load_json(trans_key_to_num=True)
    print(tmp_file.read_bytes().decode(errors='backslashreplace'))
    assert loads_data == python_data, loads_data

    serializer.dump_yaml(python_data)
    loads_data = serializer.load_yaml()
    print(tmp_file.read_bytes().decode(errors='backslashreplace'))
    assert loads_data == python_data, loads_data

    tmp_file.unlink()


if __name__ == '__main__':
    tests()
