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
os.mkdir('sub2')
hgt.writefile('sub/normal2', 'bar')
hgt.writefile('sub/normal3.txt', 'bar2')
hgt.writefile('sub/normal4.txt', 'bar3')
hgt.hg(['add', '-q', 'normal1', rejoin('sub/normal2'), rejoin('sub/normal3.txt'), rejoin('sub/normal4.txt')])
hgt.hg(['commit', '-m', 'add normal files'])

hgt.announce('add bfiles')
hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.writefile('sub/big3.txt', 'xyz')
hgt.writefile('sub/big4', 'xyz')
hgt.writefile('sub2/big5', 'xyz')
hgt.hg(['add', '-q', '--bf', 'big1', rejoin('sub/big2'), rejoin('sub/big3.txt'), rejoin('sub/big4'), rejoin('sub2/big5')])
hgt.hg(['commit', '-m', 'added bfiles'])

hgt.announce('remove sub/*.txt')
hgt.hg(['remove', 'glob:sub/*.txt'],
        stdout=('removing sub/normal3.txt\n'
                'removing sub/normal4.txt\n'
                'removing sub/big3.txt\n'))
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big4'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub2/big5'), 'added file doesnt exist')
hgt.hg(['status'],
        stdout=('R sub/big3.txt\n'
                'R sub/normal3.txt\n'
                'R sub/normal4.txt\n'))
hgt.hg(['commit', '-m', 'remove bfiles'])

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
hgt.asserttrue(os.path.exists('sub/big4'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub2/big5'), 'added file doesnt exist')
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
hgt.asserttrue(os.path.exists('sub/big4'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub2/big5'), 'added file doesnt exist')

hgt.announce('remove single normal files and add')
hgt.hg(['remove', 'normal1', 'sub/normal2'])
hgt.writefile('normal1', 'foo')
hgt.writefile('sub/normal2', 'bar')
hgt.hg(['add', 'normal1', 'sub/normal2'])
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big4'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub2/big5'), 'added file doesnt exist')
hgt.hg(['status'])

hgt.announce('remove single bfile and commit with full path')
hgt.hg(['remove', 'sub/big4'])
hgt.hg(['status'],stdout=('R sub/big4\n'))
hgt.hg(['commit', '-m', 'removing big4', 'sub/big4'])
hgt.assertfalse(os.path.exists('sub/big4'), 'removed file exists')
hgt.hg(['status'])

hgt.announce('remove single bfile and commit with partial path')
hgt.hg(['remove', 'sub2/big5'])
hgt.hg(['status'],stdout=('R sub2/big5\n'))
hgt.assertfalse(os.path.exists("sub2"), 'removed directory structure exists')
hgt.hg(['commit', '-m', 'removing big5', 'sub2'])
hgt.assertfalse(os.path.exists('sub2/big5'), 'removed file exists')
hgt.hg(['status'])

hgt.announce('remove single bfiles and add')
hgt.hg(['remove', 'big1', 'sub/big2'])
hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.hg(['add', '--bf', 'big1', 'sub/big2'])
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.asserttrue(os.path.exists('normal1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/normal2'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.hg(['status'])

hgt.announce('remove single normal files')
hgt.hg(['remove', 'normal1'])
hgt.hg(['remove', 'sub/normal2'])
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('normal1'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal2'), 'removed file exists')
hgt.asserttrue(os.path.exists('big1'), 'added file doesnt exist')
hgt.asserttrue(os.path.exists('sub/big2'), 'added file doesnt exist')
hgt.hg(['status'],
        stdout=('R normal1\n'
                'R sub/normal2\n'))

hgt.announce('remove single bfiles')
hgt.hg(['remove', 'big1'])
hgt.hg(['remove', 'sub/big2'])
hgt.assertfalse(os.path.exists('sub/normal3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
hgt.assertfalse(os.path.exists('normal1'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/normal2'), 'removed file exists')
hgt.assertfalse(os.path.exists('big1'), 'removed file exists')
hgt.assertfalse(os.path.exists('sub/big2'), 'removed file exists')
hgt.hg(['status'],
        stdout=('R big1\n'
                'R normal1\n'
                'R sub/big2\n'
                'R sub/normal2\n'))
hgt.hg(['commit', '-m', 'all gone'])
hgt.hg(['status'])
