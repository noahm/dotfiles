#!/usr/bin/env python

# Test remove

import os
import common

hgt = common.BfilesTester()

def rejoin(path):
    '''convert unix path to local convention'''
    return os.path.join(*path.split('/'))

# add size and patterns for adding as bfiles
hgt.updaterc({'bfiles': [('size', '2'), ('patterns', 'glob:**.dat')]})
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init', '-q'])
hgt.writefile('normal1', 'foo')
os.mkdir('sub')
hgt.writefile('sub/normal2', 'bar')
hgt.writefile('sub/normal3.txt', 'bar2')
hgt.writefile('sub/normal4.txt', 'bar3')
hgt.hg(['add', '-q', 'normal1', rejoin('sub/normal2'), rejoin('sub/normal3.txt'), rejoin('sub/normal4.txt')])
hgt.hg(['commit', '-m', 'add normal files'])

hgt.announce('add bfiles')
hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.writefile('sub/big3.txt', 'xyz')
hgt.hg(['add', '-q', '--bf', 'big1', rejoin('sub/big2'), rejoin('sub/big3.txt')])
hgt.hg(['commit', '-m', 'added bfiles'])

hgt.announce('forget sub/*.txt')
hgt.hg(['forget', 'glob:sub/*.txt'],
        stdout=('removing sub/normal3.txt\n'
                'removing sub/normal4.txt\n'
                'removing sub/big3.txt\n'))
hgt.asserttrue(os.path.exists('sub/normal3.txt'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal4.txt'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big3.txt'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.hg(['status'],
        stdout=('R sub/big3.txt\n'
                'R sub/normal3.txt\n'
                'R sub/normal4.txt\n'))
hgt.hg(['commit', '-m', 'forget bfiles'])
os.unlink('sub/normal3.txt')
os.unlink('sub/normal4.txt')
os.unlink('sub/big3.txt')

hgt.announce('test update')
hgt.hg(['up', '-r', '1'],
        stdout=('3 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '1 big files updated, 0 removed\n'))
hgt.asserttrue(os.path.exists('sub/normal3.txt'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal4.txt'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big3.txt'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.hg(['up'],
        stdout=('0 files updated, 0 files merged, 3 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '0 big files updated, 1 removed\n'))
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')

hgt.announce('forget single normal files')
hgt.hg(['forget', 'normal1'])
hgt.hg(['forget', 'sub/normal2'])
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.hg(['status'],
        stdout=('R normal1\n'
                'R sub/normal2\n'))

hgt.announce('forget single bfiles')
hgt.hg(['forget', 'big1'])
hgt.hg(['forget', 'sub/big2'])
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.hg(['status'],
        stdout=('R big1\n'
                'R normal1\n'
                'R sub/big2\n'
                'R sub/normal2\n'))
hgt.hg(['commit', '-m', 'all gone'])
hgt.hg(['status'],
        stdout='''? big1
? normal1
? sub/big2
? sub/normal2
''')

hgt.announce('setup')
os.chdir('..')
os.mkdir('repo2')
os.chdir('repo2')
hgt.hg(['init'])
os.mkdir('bar')
os.chdir('bar')
os.mkdir('bar')
os.chdir('bar')
os.mkdir('foo')
os.chdir('foo')
hgt.writefile('n1', 'n1')
hgt.writefile('n2.txt', 'n2')
hgt.writefile('../n3.foo', 'n3')
hgt.writefile('b1', 'b1')
hgt.writefile('b2.txt', 'b2')
hgt.writefile('../b3.foo', 'b3')
hgt.hg(['add', 'n1', 'n2.txt', '../n3.foo'])
hgt.hg(['add', '--bf', 'b1', 'b2.txt', '../b3.foo'])
hgt.hg(['status'],
        stdout='''A bar/bar/b3.foo
A bar/bar/foo/b1
A bar/bar/foo/b2.txt
A bar/bar/foo/n1
A bar/bar/foo/n2.txt
A bar/bar/n3.foo
''')
hgt.hg(['commit', '-m', 'add files'])

hgt.announce('test forget and add')
hgt.hg(['forget', 'glob:../*.foo'],
        stdout='''removing ../n3.foo
removing ../b3.foo
''')
hgt.hg(['status'],
        stdout='''R bar/bar/b3.foo
R bar/bar/n3.foo
''')
hgt.hg(['add', '../n3.foo'])
hgt.hg(['add', '--bf', '../b3.foo'])
hgt.hg(['status'])
# Mercurial < 1.6 doesn't return non zero status, but >= 1.6 does so allow both
hgt.hg(['commit', '-m', 'did i change things?'], stdout='nothing changed\n', status = [0,1])
hgt.hg(['forget', '../n3.foo', '../b3.foo'])
hgt.hg(['status'],
        stdout='''R bar/bar/b3.foo
R bar/bar/n3.foo
''')
hgt.hg(['commit', '-m', 'forget files'])
hgt.hg(['status'],
        stdout='''? bar/bar/b3.foo
? bar/bar/n3.foo
''')
hgt.hg(['forget', 'glob:*.txt'],
        stdout='''removing n2.txt
removing b2.txt
''')
hgt.hg(['status'],
        stdout='''R bar/bar/foo/b2.txt
R bar/bar/foo/n2.txt
? bar/bar/b3.foo
? bar/bar/n3.foo
''')
hgt.hg(['commit', '-m', 'forget files'])
hgt.hg(['status'],
        stdout='''? bar/bar/b3.foo
? bar/bar/foo/b2.txt
? bar/bar/foo/n2.txt
? bar/bar/n3.foo
''')
