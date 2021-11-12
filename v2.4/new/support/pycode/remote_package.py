# Use modules without first installing them. A bit hacky.
#
# WARNING: github.com is used to download file, but over HTTPS, and we check the hash.
#
from __future__ import print_function
import sys, tarfile, zipfile, hashlib, io, zipimport, tempfile
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

def _load_remote_module(name, ver_attr, min_ver, url, expect_hash):
    if name in sys.modules:
        return
    try:
        mod = __import__(name, globals(), locals())
        ver = tuple(int(i) for i in getattr(mod, ver_attr, '-1').split('.'))
        assert len(ver) == len(min_ver)
        assert ver >= min_ver
        return
    except (ImportError, AssertionError):
        pass

    print("Downloading %s (wait)..." % name)
    tgz = urlopen(url).read()
    assert hashlib.sha256(tgz).hexdigest() == expect_hash, "File corrupt!"

    tmp = tempfile.NamedTemporaryFile(suffix='.zip')
    with zipfile.ZipFile(tmp.name, 'w') as zf:
        with tarfile.open(fileobj=io.BytesIO(tgz), mode='r:gz') as tf:
            for ti in tf:
                path = ti.path.split('/')
                if len(path) <= 1 or path[1] != name: continue
                ff = tf.extractfile(ti)
                if not ff: continue
                zf.writestr('/'.join(path[1:]), ff.read())

    # updates sys.modules[]
    zipimport.zipimporter(tmp.name).load_module(name)

    # need to make the lifetime of the tempfile longer
    globals()[name + expect_hash] = tmp

def load_remote_module(name):

    if name == 'pycoin':
        _load_remote_module(name,
            'version', (0, 76),
            'https://github.com/richardkiss/pycoin/archive/0.76.tar.gz',
            'ffccd9709dafd53c4ea4b208879eb8872c4cea1cd9586599d9ad3fc411404a21')

    if name == 'ecdsa':
        _load_remote_module(name,
            '__version__', (0, 13),
            'https://github.com/warner/python-ecdsa/archive/python-ecdsa-0.13.tar.gz',
            '3a5139eaeab5c46f309d71cbfb5ce27cdf9f7c6b0b2d9f6f51e839a0207e381c')
