#!/usr/bin/env python

# Test that edited bfiles show up as modified

import os
import common

hgt = common.BfilesTester()

def rejoin(path):
    '''convert unix path to local convention'''
    return os.path.join(*path.split('/'))

# add size and patterns for adding as bfiles
hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init', '-q'])
hgt.writefile('normal1', 'foo')
os.mkdir('sub')
hgt.writefile('sub/normal2', 'bar')
hgt.hg(['add', '-q', 'normal1', rejoin('sub/normal2')])
hgt.hg(['commit', '-m', 'add normal files'])

hgt.announce('add bfiles')
hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.hg(['add', '--bf', 'big1', rejoin('sub/big2')])
hgt.hg(['status'], stdout='A big1\nA sub/big2\n')
hgt.hg(['commit', '-m', 'added bfiles'])

hgt.announce('edit big1')
hgt.writefile('big1', 'abcd')
hgt.hg(['status'], stdout='M big1\n')

hgt.announce('edit sub/big2')
hgt.writefile('sub/big2', 'xyz1')
hgt.hg(['status'], stdout='M big1\nM sub/big2\n')

hgt.announce('edit big1 back')
hgt.writefile('big1', 'abc')
hgt.hg(['status'], stdout='M sub/big2\n')

hgt.announce('edit sub/big2 back')
hgt.writefile('sub/big2', 'xyz')
hgt.hg(['status'])
