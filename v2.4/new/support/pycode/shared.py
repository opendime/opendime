# Shared code for balance and trustme
import os, sys

def BTC(t):
    return "%d.%08d BTC" % (t // 1E8, t % 1E8)

def find_root():
    spots = [__file__ + '/../..', __file__ +'/..', '.', '..',
                'A:\\', 'B:\\', 'C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\',
                '/Volumes/OPENDIME', '/Volumes/OPENDIME 1', '/Volumes/OPENDIME 2' ]

    if len(sys.argv) >= 2:
        spots.insert(0, sys.argv[-1])
        spots.insert(0, os.path.dirname(sys.argv[-1]))

    tries = []
    for fn in spots:
        path = os.path.normpath(fn + '/support/opendime.png').replace('/', os.sep)
        tries.append(path)
        if os.path.isfile(path):
            return os.path.abspath(os.path.dirname(os.path.dirname(path)))

    raise RuntimeError("Cannot find path to Opendime. Checked:\n\n  " + '\n  '.join(tries))

