#!/usr/bin/env python

# Test cloning a repo

import os
import common

hgt = common.BfilesTester()

def rejoin(path):
    '''convert unix path to local convention'''
    return os.path.join(*path.split('/'))

def assertidentical(hgt, file1, file2):
    hgt.asserttrue(os.path.exists(file1) == os.path.exists(file2), 'File existence doesnt match')
    if not os.path.exists(file1):
        return
    with open(file1, 'r') as fd:
        d1 = fd.read()
    with open(file2, 'r') as fd:
        d2 = fd.read()
    hgt.asserttrue(d1 == d2, 'Files differ %s %s %s %s' % (file1, file2, d1, d2))

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

hgt.announce('edit files')
hgt.writefile('big1', '123')
hgt.writefile('sub/big2', '456')
hgt.writefile('normal1', '789')
hgt.writefile('sub/normal2', '012')
hgt.hg(['commit', '-m', 'edited files'])

hgt.announce('clone to repo2')
os.chdir('..')
hgt.hg(['clone', 'repo1', 'repo2'],
        stdout=('updating to branch default\n'
                '7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
files = ['normal1', 'sub/normal2', 'sub/normal3.txt', 'sub/normal4.txt', 'big1', 'sub/big2', 'sub/big3.txt']
for file in files:
    assertidentical(hgt, os.path.join('repo1', file), os.path.join('repo2', file))

hgt.announce('update to rev 0 and check')
os.chdir('repo1')
hgt.hg(['up', '-r', '0'],
        stdout=('2 files updated, 0 files merged, 3 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '0 big files updated, 3 removed\n'))
os.chdir('../repo2')
hgt.hg(['up', '-r', '0'],
        stdout=('2 files updated, 0 files merged, 3 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '0 big files updated, 3 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo1', file), os.path.join('repo2', file))

hgt.announce('update to rev 1 and check')
os.chdir('repo1')
hgt.hg(['up', '-r', '1'],
        stdout=('3 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
os.chdir('../repo2')
hgt.hg(['up', '-r', '1'],
        stdout=('3 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo1', file), os.path.join('repo2', file))

hgt.announce('update to rev 2 and check')
os.chdir('repo1')
hgt.hg(['up', '-r', '2'],
        stdout=('4 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '2 big files updated, 0 removed\n'))
os.chdir('../repo2')
hgt.hg(['up', '-r', '2'],
        stdout=('4 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '2 big files updated, 0 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo1', file), os.path.join('repo2', file))

hgt.announce('clone to repo3')
hgt.hg(['clone', '-U', 'repo2', 'repo3'])
os.chdir('repo3')
hgt.hg(['up'], stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo2', file), os.path.join('repo3', file))

hgt.announce('update to rev 0 and check')
os.chdir('repo2')
hgt.hg(['up', '-r', '0'],
        stdout=('2 files updated, 0 files merged, 3 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '0 big files updated, 3 removed\n'))
os.chdir('../repo3')
hgt.hg(['up', '-r', '0'],
        stdout=('2 files updated, 0 files merged, 3 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '0 big files updated, 3 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo2', file), os.path.join('repo3', file))

hgt.announce('update to rev 1 and check')
os.chdir('repo2')
hgt.hg(['up', '-r', '1'],
        stdout=('3 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
os.chdir('../repo3')
hgt.hg(['up', '-r', '1'],
        stdout=('3 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo2', file), os.path.join('repo3', file))

hgt.announce('update to rev 2 and check')
os.chdir('repo2')
hgt.hg(['up', '-r', '2'],
        stdout=('4 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '2 big files updated, 0 removed\n'))
os.chdir('../repo3')
hgt.hg(['up', '-r', '2'],
        stdout=('4 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '2 big files updated, 0 removed\n'))
os.chdir('..')
for file in files:
    assertidentical(hgt, os.path.join('repo2', file), os.path.join('repo3', file))

os.chdir('repo3')
hgt.hg(['cp', 'sub', 'dir'],
        stdout='''copying sub/normal2 to dir/normal2
copying sub/normal3.txt to dir/normal3.txt
copying sub/normal4.txt to dir/normal4.txt
copying .kbf/sub/big2 to .kbf/dir/big2
copying .kbf/sub/big3.txt to .kbf/dir/big3.txt
''')
hgt.hg(['cp', 'dir', 'dir2'],
        stdout='''copying dir/normal2 to dir2/normal2
copying dir/normal3.txt to dir2/normal3.txt
copying dir/normal4.txt to dir2/normal4.txt
copying .kbf/dir/big2 to .kbf/dir2/big2
copying .kbf/dir/big3.txt to .kbf/dir2/big3.txt
''')
hgt.hg(['commit', '-m', 'copy sub twice'])
os.chdir('..')

hgt.announce('clone again')
hgt.hg(['clone', 'repo3', 'repo4', '-U'])
os.chdir('repo4')
for file in os.listdir('.'):
    hgt.asserttrue(file.startswith('.hg'), 'files shouldnt exist')
hgt.hg(['up'],
        stdout='''17 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
7 big files updated, 0 removed
''')
os.chdir('..')

newfiles = files + ['dir/normal2', 'dir/normal3.txt', 'dir/normal4.txt', 'dir/big2','dir/big3.txt']
newfiles += ['dir2/normal2', 'dir2/normal3.txt', 'dir2/normal4.txt', 'dir2/big2','dir2/big3.txt']
for file in newfiles:
    assertidentical(hgt, os.path.join('repo3', file), os.path.join('repo4', file))
for file in os.listdir('repo3'):
    hgt.asserttrue(file.startswith('.hg') or file.startswith('.kbf') or file in newfiles + ['sub', 'dir', 'dir2'], 'file shouldnt exist')
for file in os.listdir('repo4'):
    hgt.asserttrue(file.startswith('.hg') or file.startswith('.kbf') or file in newfiles + ['sub', 'dir', 'dir2'], 'file shouldnt exist')

os.chdir('repo3')
hgt.hg(['up', '-r', '2'],
        stdout='''0 files updated, 0 files merged, 10 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 4 removed
''')
os.chdir('../repo4')
hgt.hg(['up', '-r', '2'],
        stdout='''0 files updated, 0 files merged, 10 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 4 removed
''')
os.chdir('..')
