#!/usr/bin/env python

# Test copy and rename

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
hgt.hg(['init', '-q'])
hgt.writefile('normal1', 'n1')
hgt.writefile('normal2', 'n2')
hgt.writefile('normal3.txt', 'n3')
hgt.writefile('normal4.txt', 'n4')
hgt.hg(['add', 'normal1', 'normal2', 'normal3.txt', 'normal4.txt'])
hgt.writefile('big1', 'b1')
hgt.writefile('big2', 'b2')
hgt.writefile('big3.txt', 'b3')
hgt.writefile('big4.txt', 'b4')
hgt.hg(['add', '--bf', 'big1', 'big2', 'big3.txt', 'big4.txt'])
hgt.hg(['commit', '-m', 'added files'])

hgt.announce('copy all to directory')
os.mkdir('dir')
hgt.hg(['copy', 'glob:*', 'dir'],
        stdout=('copying normal1 to dir/normal1\n'
                'copying normal2 to dir/normal2\n'
                'copying normal3.txt to dir/normal3.txt\n'
                'copying normal4.txt to dir/normal4.txt\n'
                'copying .kbf/big1 to .kbf/dir/big1\n'
                'copying .kbf/big2 to .kbf/dir/big2\n'
                'copying .kbf/big3.txt to .kbf/dir/big3.txt\n'
                'copying .kbf/big4.txt to .kbf/dir/big4.txt\n'))
checkfile('dir/normal1', 'n1')
checkfile('dir/normal2', 'n2')
checkfile('dir/normal3.txt', 'n3')
checkfile('dir/normal4.txt', 'n4')
checkfile('dir/big1', 'b1')
checkfile('dir/big2', 'b2')
checkfile('dir/big3.txt', 'b3')
checkfile('dir/big4.txt', 'b4')
hgt.hg(['status'],
        stdout=('A dir/big1\n'
                'A dir/big2\n'
                'A dir/big3.txt\n'
                'A dir/big4.txt\n'
                'A dir/normal1\n'
                'A dir/normal2\n'
                'A dir/normal3.txt\n'
                'A dir/normal4.txt\n'))
hgt.hg(['commit', '-m', 'added copies'])
hgt.hg(['status'])

hgt.announce('copy some to directory')
os.mkdir('dir2')
hgt.hg(['copy', 'glob:*.txt', 'dir2'],
        stdout=('copying normal3.txt to dir2/normal3.txt\n'
                'copying normal4.txt to dir2/normal4.txt\n'
                'copying .kbf/big3.txt to .kbf/dir2/big3.txt\n'
                'copying .kbf/big4.txt to .kbf/dir2/big4.txt\n'))
checkfile('dir2/normal3.txt', 'n3')
checkfile('dir2/normal4.txt', 'n4')
checkfile('dir2/big3.txt', 'b3')
checkfile('dir2/big4.txt', 'b4')
hgt.assertfalse(os.path.exists('dir2/normal1'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir2/normal2'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir2/big1'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir2/big2'), 'file should not exist')
hgt.hg(['status'],
        stdout=('A dir2/big3.txt\n'
                'A dir2/big4.txt\n'
                'A dir2/normal3.txt\n'
                'A dir2/normal4.txt\n'))
hgt.hg(['commit', '-m', 'added some'])
hgt.hg(['status'])

hgt.announce('rewrite root files and copy all to dir2')
hgt.writefile('normal1', 'n11')
hgt.writefile('normal2', 'n22')
hgt.writefile('normal3.txt', 'n33')
hgt.writefile('normal4.txt', 'n44')
hgt.writefile('big1', 'b11')
hgt.writefile('big2', 'b22')
hgt.writefile('big3.txt', 'b33')
hgt.writefile('big4.txt', 'b44')
hgt.hg(['commit', '-m', 'edit'])
hgt.hg(['copy', 'glob:*', 'dir2'],
        stdout=('copying normal1 to dir2/normal1\n'
                'copying normal2 to dir2/normal2\n'
                'copying .kbf/big1 to .kbf/dir2/big1\n'
                'copying .kbf/big2 to .kbf/dir2/big2\n'),
        stderr=('dir2/normal3.txt: not overwriting - file exists\n'
                'dir2/normal4.txt: not overwriting - file exists\n'
                '.kbf/dir2/big3.txt: not overwriting - file exists\n'
                '.kbf/dir2/big4.txt: not overwriting - file exists\n'))
hgt.hg(['status'],
        stdout=('A dir2/big1\n'
                'A dir2/big2\n'
                'A dir2/normal1\n'
                'A dir2/normal2\n'))
hgt.hg(['commit', '-m', 'copy again'])
hgt.hg(['status'])
checkfile('dir2/normal1', 'n11')
checkfile('dir2/normal2', 'n22')
checkfile('dir2/normal3.txt', 'n3')
checkfile('dir2/normal4.txt', 'n4')
checkfile('dir2/big1', 'b11')
checkfile('dir2/big2', 'b22')
checkfile('dir2/big3.txt', 'b3')
checkfile('dir2/big4.txt', 'b4')
checkfile('normal1', 'n11')
checkfile('normal2', 'n22')
checkfile('normal3.txt', 'n33')
checkfile('normal4.txt', 'n44')
checkfile('big1', 'b11')
checkfile('big2', 'b22')
checkfile('big3.txt', 'b33')
checkfile('big4.txt', 'b44')

hgt.announce('copy files by name to dir3')
os.mkdir('dir3')
hgt.hg(['copy', 'normal1', 'normal3.txt', 'big1', 'big3.txt', 'dir3'])
hgt.hg(['status'],
         stdout=('A dir3/big1\n'
                 'A dir3/big3.txt\n'
                 'A dir3/normal1\n'
                 'A dir3/normal3.txt\n'))
hgt.hg(['commit', '-m', 'copy individual'])
hgt.hg(['status'])
checkfile('dir3/normal1', 'n11')
checkfile('dir3/normal3.txt', 'n33')
checkfile('dir3/big1', 'b11')
checkfile('dir3/big3.txt', 'b33')
hgt.assertfalse(os.path.exists('dir3/normal2'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir3/normal4.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir3/big2'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir3/big4.txt'), 'file should not exist')

hgt.announce('rename some files to dir4')
os.mkdir('dir4')
hgt.hg(['rename', 'glob:*.txt', 'dir4'],
        stdout=('moving normal3.txt to dir4/normal3.txt\n'
               'moving normal4.txt to dir4/normal4.txt\n'
               'moving .kbf/big3.txt to .kbf/dir4/big3.txt\n'
               'moving .kbf/big4.txt to .kbf/dir4/big4.txt\n'))
hgt.hg(['status'],
        stdout=('A dir4/big3.txt\n'
                'A dir4/big4.txt\n'
                'A dir4/normal3.txt\n'
                'A dir4/normal4.txt\n'
                'R big3.txt\n'
                'R big4.txt\n'
                'R normal3.txt\n'
                'R normal4.txt\n'))
checkfile('dir4/normal3.txt', 'n33')
checkfile('dir4/normal4.txt', 'n44')
checkfile('dir4/big3.txt', 'b33')
checkfile('dir4/big4.txt', 'b44')
hgt.assertfalse(os.path.exists('dir4/normal1'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir4/normal2'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir4/big1'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir4/big2'), 'file should not exist')
hgt.assertfalse(os.path.exists('normal3.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('normal4.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('big3.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('big4.txt'), 'file should not exist')


hgt.announce('rename remaining files to dir5')
os.mkdir('dir5')
hgt.hg(['rename', 'glob:*', 'dir5'],
        stdout=('moving normal1 to dir5/normal1\n'
               'moving normal2 to dir5/normal2\n'
               'moving .kbf/big1 to .kbf/dir5/big1\n'
               'moving .kbf/big2 to .kbf/dir5/big2\n'))
hgt.hg(['status'],
         stdout=('A dir4/big3.txt\n'
                 'A dir4/big4.txt\n'
                 'A dir4/normal3.txt\n'
                 'A dir4/normal4.txt\n'
                 'A dir5/big1\n'
                 'A dir5/big2\n'
                 'A dir5/normal1\n'
                 'A dir5/normal2\n'
                 'R big1\n'
                 'R big2\n'
                 'R big3.txt\n'
                 'R big4.txt\n'
                 'R normal1\n'
                 'R normal2\n'
                 'R normal3.txt\n'
                 'R normal4.txt\n'))
hgt.hg(['commit', '-m', 'rename to dir5'])
hgt.hg(['status'])
checkfile('dir5/normal1', 'n11')
checkfile('dir5/normal2', 'n22')
checkfile('dir5/big1', 'b11')
checkfile('dir5/big2', 'b22')
hgt.assertfalse(os.path.exists('dir5/normal3.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir5/normal4.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir5/big3.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('dir5/big4.txt'), 'file should not exist')
hgt.assertfalse(os.path.exists('normal1'), 'file should not exist')
hgt.assertfalse(os.path.exists('normal2'), 'file should not exist')
hgt.assertfalse(os.path.exists('big1'), 'file should not exist')
hgt.assertfalse(os.path.exists('big2'), 'file should not exist')

hgt.announce('big copy')
os.mkdir('bdir1')
hgt.hg(['copy', 'dir', 'dir2', 'bdir1'],
        stdout=('copying dir/normal1 to bdir1/dir/normal1\n'
                'copying dir/normal2 to bdir1/dir/normal2\n'
                'copying dir/normal3.txt to bdir1/dir/normal3.txt\n'
                'copying dir/normal4.txt to bdir1/dir/normal4.txt\n'
                'copying dir2/normal1 to bdir1/dir2/normal1\n'
                'copying dir2/normal2 to bdir1/dir2/normal2\n'
                'copying dir2/normal3.txt to bdir1/dir2/normal3.txt\n'
                'copying dir2/normal4.txt to bdir1/dir2/normal4.txt\n'
                'copying .kbf/dir/big1 to .kbf/bdir1/dir/big1\n'
                'copying .kbf/dir/big2 to .kbf/bdir1/dir/big2\n'
                'copying .kbf/dir/big3.txt to .kbf/bdir1/dir/big3.txt\n'
                'copying .kbf/dir/big4.txt to .kbf/bdir1/dir/big4.txt\n'
                'copying .kbf/dir2/big1 to .kbf/bdir1/dir2/big1\n'
                'copying .kbf/dir2/big2 to .kbf/bdir1/dir2/big2\n'
                'copying .kbf/dir2/big3.txt to .kbf/bdir1/dir2/big3.txt\n'
                'copying .kbf/dir2/big4.txt to .kbf/bdir1/dir2/big4.txt\n'))
hgt.hg(['status'],
    stdout=('A bdir1/dir/big1\n'
            'A bdir1/dir/big2\n'
            'A bdir1/dir/big3.txt\n'
            'A bdir1/dir/big4.txt\n'
            'A bdir1/dir/normal1\n'
            'A bdir1/dir/normal2\n'
            'A bdir1/dir/normal3.txt\n'
            'A bdir1/dir/normal4.txt\n'
            'A bdir1/dir2/big1\n'
            'A bdir1/dir2/big2\n'
            'A bdir1/dir2/big3.txt\n'
            'A bdir1/dir2/big4.txt\n'
            'A bdir1/dir2/normal1\n'
            'A bdir1/dir2/normal2\n'
            'A bdir1/dir2/normal3.txt\n'
            'A bdir1/dir2/normal4.txt\n'))
hgt.hg(['commit', '-m', 'big copy1'])
hgt.hg(['status'])

hgt.announce('big rename')
os.mkdir('bdir2')
os.mkdir('bdir2/dir')
os.chdir('bdir2')
hgt.hg(['copy', '../dir3', '../dir4', '../dir5', 'dir'],
    stdout=('copying ../dir3/normal1 to dir/dir3/normal1\n'
            'copying ../dir3/normal3.txt to dir/dir3/normal3.txt\n'
            'copying ../dir4/normal3.txt to dir/dir4/normal3.txt\n'
            'copying ../dir4/normal4.txt to dir/dir4/normal4.txt\n'
            'copying ../dir5/normal1 to dir/dir5/normal1\n'
            'copying ../dir5/normal2 to dir/dir5/normal2\n'
            'copying ../.kbf/dir3/big1 to ../.kbf/bdir2/dir/dir3/big1\n'
            'copying ../.kbf/dir3/big3.txt to ../.kbf/bdir2/dir/dir3/big3.txt\n'
            'copying ../.kbf/dir4/big3.txt to ../.kbf/bdir2/dir/dir4/big3.txt\n'
            'copying ../.kbf/dir4/big4.txt to ../.kbf/bdir2/dir/dir4/big4.txt\n'
            'copying ../.kbf/dir5/big1 to ../.kbf/bdir2/dir/dir5/big1\n'
            'copying ../.kbf/dir5/big2 to ../.kbf/bdir2/dir/dir5/big2\n'))
hgt.hg(['status'],
    stdout=('A bdir2/dir/dir3/big1\n'
            'A bdir2/dir/dir3/big3.txt\n'
            'A bdir2/dir/dir3/normal1\n'
            'A bdir2/dir/dir3/normal3.txt\n'
            'A bdir2/dir/dir4/big3.txt\n'
            'A bdir2/dir/dir4/big4.txt\n'
            'A bdir2/dir/dir4/normal3.txt\n'
            'A bdir2/dir/dir4/normal4.txt\n'
            'A bdir2/dir/dir5/big1\n'
            'A bdir2/dir/dir5/big2\n'
            'A bdir2/dir/dir5/normal1\n'
            'A bdir2/dir/dir5/normal2\n'))
hgt.hg(['commit', '-m', 'big copy2'])
hgt.hg(['status', '-A'],
            stdout='''C bdir1/dir/big1
C bdir1/dir/big2
C bdir1/dir/big3.txt
C bdir1/dir/big4.txt
C bdir1/dir/normal1
C bdir1/dir/normal2
C bdir1/dir/normal3.txt
C bdir1/dir/normal4.txt
C bdir1/dir2/big1
C bdir1/dir2/big2
C bdir1/dir2/big3.txt
C bdir1/dir2/big4.txt
C bdir1/dir2/normal1
C bdir1/dir2/normal2
C bdir1/dir2/normal3.txt
C bdir1/dir2/normal4.txt
C bdir2/dir/dir3/big1
C bdir2/dir/dir3/big3.txt
C bdir2/dir/dir3/normal1
C bdir2/dir/dir3/normal3.txt
C bdir2/dir/dir4/big3.txt
C bdir2/dir/dir4/big4.txt
C bdir2/dir/dir4/normal3.txt
C bdir2/dir/dir4/normal4.txt
C bdir2/dir/dir5/big1
C bdir2/dir/dir5/big2
C bdir2/dir/dir5/normal1
C bdir2/dir/dir5/normal2
C dir/big1
C dir/big2
C dir/big3.txt
C dir/big4.txt
C dir/normal1
C dir/normal2
C dir/normal3.txt
C dir/normal4.txt
C dir2/big1
C dir2/big2
C dir2/big3.txt
C dir2/big4.txt
C dir2/normal1
C dir2/normal2
C dir2/normal3.txt
C dir2/normal4.txt
C dir3/big1
C dir3/big3.txt
C dir3/normal1
C dir3/normal3.txt
C dir4/big3.txt
C dir4/big4.txt
C dir4/normal3.txt
C dir4/normal4.txt
C dir5/big1
C dir5/big2
C dir5/normal1
C dir5/normal2
''')

hgt.announce('single copy')
hgt.writefile('foo', 'stuff')
hgt.hg(['add', 'foo'])
hgt.hg(['commit', '-m', 'added foo'])
hgt.hg(['cp', 'foo', 'bar'])

hgt.announce('single copy2')
hgt.writefile('foo2', 'stuff')
hgt.hg(['add', '--bf', 'foo2'])
hgt.hg(['commit', '-m', 'added foo2'])
hgt.hg(['cp', 'foo2', 'bar2'])

hgt.announce('relative rename')
os.chdir('..')
os.mkdir('repo2')
os.chdir('repo2')
hgt.hg(['init'])
os.mkdir('a')
os.mkdir('dest')
os.chdir('a')
os.mkdir('b')
os.mkdir('c')
os.mkdir('b/b')
hgt.writefile('n1', 'n1')
hgt.writefile('b/n2', 'n2')
hgt.writefile('c/n3', 'n3')
hgt.writefile('b/b/n4', 'n4')
hgt.hg(['add'],
        stdout='''adding b/b/n4
adding b/n2
adding c/n3
adding n1
''')
hgt.writefile('b1', 'b1')
hgt.writefile('b/b2', 'b2')
hgt.writefile('c/b3', 'b3')
hgt.writefile('b/b/b4', 'b4')
hgt.hg(['add', '--bf'],
        stdout='''adding b/b/b4 as bfile
adding b/b2 as bfile
adding b1 as bfile
adding c/b3 as bfile
''')
hgt.hg(['commit', '-m', 'add files'])
hgt.hg(['rename', '.', '../dest'],
        stdout='''moving b/b/n4 to ../dest/a/b/b/n4
moving b/n2 to ../dest/a/b/n2
moving c/n3 to ../dest/a/c/n3
moving n1 to ../dest/a/n1
moving ../.kbf/a/b/b/b4 to ../.kbf/dest/a/b/b/b4
moving ../.kbf/a/b/b2 to ../.kbf/dest/a/b/b2
moving ../.kbf/a/b1 to ../.kbf/dest/a/b1
moving ../.kbf/a/c/b3 to ../.kbf/dest/a/c/b3
''')
hgt.hg(['status'],
        stdout='''A dest/a/b/b/b4
A dest/a/b/b/n4
A dest/a/b/b2
A dest/a/b/n2
A dest/a/b1
A dest/a/c/b3
A dest/a/c/n3
A dest/a/n1
R a/b/b/b4
R a/b/b/n4
R a/b/b2
R a/b/n2
R a/b1
R a/c/b3
R a/c/n3
R a/n1
''')

hgt.announce('relative rename without bfiles')
os.chdir('..')
os.mkdir('repo2')
os.chdir('repo2')
hgt.hg(['init'])
os.mkdir('a')
os.mkdir('dest')
os.chdir('a')
os.mkdir('b')
os.mkdir('c')
os.mkdir('b/b')
hgt.writefile('n1', 'n1')
hgt.writefile('b/n2', 'n2')
hgt.writefile('c/n3', 'n3')
hgt.writefile('b/b/n4', 'n4')
hgt.hg(['add'],
        stdout='''adding b/b/n4
adding b/n2
adding c/n3
adding n1
''')
hgt.hg(['commit', '-m', 'add files'])
hgt.hg(['rename', '.', '../dest'],
        stdout='''moving b/b/n4 to ../dest/a/b/b/n4
moving b/n2 to ../dest/a/b/n2
moving c/n3 to ../dest/a/c/n3
moving n1 to ../dest/a/n1
''')
os.chdir('..')
hgt.hg(['status'],
        stdout='''A dest/a/b/b/n4
A dest/a/b/n2
A dest/a/c/n3
A dest/a/n1
R a/b/b/n4
R a/b/n2
R a/c/n3
R a/n1
''')
