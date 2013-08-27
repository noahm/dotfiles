#!/usr/bin/env python

# Test status

import os
import common

hgt = common.BfilesTester()

def checkfile(file, contents):
    hgt.asserttrue(hgt.readfile(file) == contents, 'file contents dont match')

# add size and patterns for adding as bfiles
hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
os.mkdir('dir')
os.chdir('dir')
os.mkdir('dir')
hgt.writefile('dir/a', 'a')
hgt.writefile('dir/b', 'b')
hgt.writefile('dir/c', 'c')
hgt.writefile('dir/d', 'd')
hgt.writefile('dir/e', 'e')
hgt.writefile('dir/f', 'f')
hgt.writefile('dir2/a', 'a')
hgt.writefile('dir2/b', 'b')
hgt.writefile('dir2/c', 'c')
hgt.writefile('dir2/d', 'd')
hgt.writefile('dir2/e', 'e')
hgt.writefile('dir2/f', 'f')
hgt.writefile('a', 'a')
hgt.writefile('b', 'b')
hgt.writefile('c', 'c')
hgt.writefile('d', 'd')
hgt.writefile('e', 'e')
hgt.writefile('f', 'f')
hgt.hg(['add', '--bf', 'dir/b', 'dir/c', 'dir/d', 'dir/f'])
hgt.hg(['add', 'dir2/b', 'dir2/c', 'dir2/d', 'dir2/f'])
hgt.hg(['add', '--bf', 'b', 'c', 'd', 'f'])
hgt.hg(['commit', '-m', 'added files'])
hgt.hg(['add', '--bf', 'dir/a'])
hgt.hg(['add', 'dir2/a'])
hgt.hg(['add', '--bf', 'a'])
hgt.writefile('dir/b', 'bb')
hgt.writefile('dir2/b', 'bb')
hgt.writefile('b', 'bb')
hgt.hg(['rm', 'dir/d'])
hgt.hg(['rm', 'dir2/d'])
hgt.hg(['rm', 'd'])
os.unlink('dir/f')
os.unlink('dir2/f')
os.unlink('f')
hgt.hg(['status'],
        stdout='''M dir/b
M dir/dir/b
M dir/dir2/b
A dir/a
A dir/dir/a
A dir/dir2/a
R dir/d
R dir/dir/d
R dir/dir2/d
! dir/dir/f
! dir/dir2/f
! dir/f
? dir/dir/e
? dir/dir2/e
? dir/e
''')
hgt.hg(['status', '-A'],
        stdout='''M dir/b
M dir/dir/b
M dir/dir2/b
A dir/a
A dir/dir/a
A dir/dir2/a
R dir/d
R dir/dir/d
R dir/dir2/d
! dir/dir/f
! dir/dir2/f
! dir/f
? dir/dir/e
? dir/dir2/e
? dir/e
C dir/c
C dir/dir/c
C dir/dir2/c
''')
hgt.hg(['status', '-m'],
        stdout='''M dir/b
M dir/dir/b
M dir/dir2/b
''')
hgt.hg(['status', '-a'],
        stdout='''A dir/a
A dir/dir/a
A dir/dir2/a
''')
hgt.hg(['status', '-r'],
        stdout='''R dir/d
R dir/dir/d
R dir/dir2/d
''')
hgt.hg(['status', '-d'],
        stdout='''! dir/dir/f
! dir/dir2/f
! dir/f
''')
hgt.hg(['status', '-c'],
        stdout='''C dir/c
C dir/dir/c
C dir/dir2/c
''')
hgt.hg(['status', '-u'],
        stdout='''? dir/dir/e
? dir/dir2/e
? dir/e
''')
