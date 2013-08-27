#!/usr/bin/env python

# Test various tricky bfadd corner cases.

import os
import common

hgt = common.BfilesTester()

def rejoin(path):
    '''convert unix path to local convention'''
    return os.path.join(*path.split('/'))

# add size and patterns for adding as bfiles
hgt.updaterc({'kilnbfiles': [('size', '2'), ('patterns', 'glob:**.dat')]})
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init', '-q'])
hgt.writefile('normal1', 'foo')
os.mkdir('sub')
hgt.writefile('sub/normal2', 'bar')
hgt.hg(['add', '-q', 'normal1', rejoin('sub/normal2')])
hgt.hg(['commit', '-m', 'add normal files'])

hgt.announce('add existing normal files')
hgt.hg(['add', '--bf', 'normal1', rejoin('sub/normal2')],
       stderr=('normal1 already tracked!\n'
               'sub/normal2 already tracked!\n'))
hgt.hg(['status'], stdout='')           # clean

hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.announce('add bfiles')
hgt.hg(['add', '--bf', 'big1', rejoin('sub/big2')])
hgt.asserttrue(os.path.exists('.kbf/big1'), 'standin exists')
hgt.asserttrue(os.path.exists('.kbf/sub/big2'), 'standin exists')
hgt.hg(['status'], stdout='A big1\nA sub/big2\n')
hgt.hg(['commit', '-m', 'added bfiles'])

hgt.announce('add existing bfiles')
hgt.hg(['add', '--bf', 'big1', rejoin('sub/big2')],
        stderr='big1 already a bfile\nsub/big2 already a bfile\n')
hgt.hg(['status'], stdout='')           # clean

hgt.announce('recursive add on existing subdirectory')
os.mkdir(rejoin('sub/deep'))
hgt.writefile(rejoin('sub/big3'), '1\n')
hgt.writefile(rejoin('sub/big4'), '2\n')
hgt.writefile(rejoin('sub/deep/big5'), '3\n')
hgt.hg(['add', '--bf', '-v', 'sub'],
       stdout=('adding sub/big3 as bfile\n'
               'adding sub/big4 as bfile\n'
               'adding sub/deep/big5 as bfile\n'))
hgt.hg(['status'],
       stdout=('A sub/big3\n'
               'A sub/big4\n'
               'A sub/deep/big5\n'))
hgt.hg(['commit', '-m', 'Add a whole subdir of big files'])

hgt.announce('status after committing an add')
hgt.hg(['status'], stdout='')           # clean

hgt.announce('adding bfiles and normal files with hgrc settings')
os.mkdir('dir')
hgt.writefile(rejoin('dir/small'), 'small')
hgt.writefile(rejoin('dir/dict.dat'), 'dictionary')
hgt.writefile(rejoin('dir/blah.dat'), 'foo')
hgt.writefile(rejoin('dir/foo'), 'normal')
hgt.writefile(rejoin('dir/bigfile'), 'a'*(1024*1024*3))
hgt.hg(['add', 'dir'],
        stdout=('adding dir/bigfile as bfile\n'
             'adding dir/blah.dat as bfile\n'
             'adding dir/dict.dat as bfile\n'
             'adding dir/foo\n'
             'adding dir/small\n'))
hgt.hg(['status'],
        stdout=('A dir/bigfile\n'
             'A dir/blah.dat\n'
             'A dir/dict.dat\n'
             'A dir/foo\n'
             'A dir/small\n'))
hgt.hg(['commit', '-m', 'Added some stuff'])

hgt.announce('adding bfiles and normal files with size setting')
os.mkdir('dir2')
hgt.writefile(rejoin('dir2/small'), 'small')
hgt.writefile(rejoin('dir2/dict.dat'), 'dictionary')
hgt.writefile(rejoin('dir2/blah.dat'), 'foo')
hgt.writefile(rejoin('dir2/foo'), 'normal')
hgt.writefile(rejoin('dir2/bigfile'), 'a'*(1024*1024*3))
hgt.hg(['add', '--bfsize', '10', 'dir2'],
        stdout=('adding dir2/blah.dat as bfile\n'
             'adding dir2/dict.dat as bfile\n'
             'adding dir2/bigfile\n'
             'adding dir2/foo\n'
             'adding dir2/small\n'))
hgt.hg(['status'],
        stdout=('A dir2/bigfile\n'
             'A dir2/blah.dat\n'
             'A dir2/dict.dat\n'
             'A dir2/foo\n'
             'A dir2/small\n'))
hgt.hg(['commit', '-m', 'Added some stuff'])

hgt.writefile('blah.dat', 'stuff')
os.mkdir('dir3')
os.chdir('dir3')
hgt.writefile('foo', 'stuff')
hgt.writefile('bar.dat', 'stuff')
hgt.hg(['add', 'foo'])
hgt.hg(['add'],
        stdout=('adding ../blah.dat as bfile\n'
                'adding bar.dat as bfile\n'))
hgt.hg(['status'],
        stdout=('A blah.dat\n'
                'A dir3/bar.dat\n'
                'A dir3/foo\n'))
