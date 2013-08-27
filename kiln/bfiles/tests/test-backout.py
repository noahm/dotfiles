#!/usr/bin/env python
#
# Every commit needs time stamps so that the commits are unique (Mercurial backout test
# does the same thing).

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
hgt.hg(['init'])
os.mkdir('dir')
os.chdir('dir')
hgt.writefile('n1', 'n1')
hgt.writefile('n2', 'n2')
hgt.writefile('dir/n3', 'n3')
hgt.writefile('dir/dir/n4', 'n4')
hgt.writefile('b1', 'b1')
hgt.writefile('b2', 'b2')
hgt.writefile('dir/b3', 'b3')
hgt.writefile('dir/dir/b4', 'b4')
hgt.hg(['add', 'n1', 'n2', 'dir/n3', 'dir/dir/n4'])
hgt.hg(['add', '--bf', 'b1', 'b2', 'dir/b3', 'dir/dir/b4'])
hgt.hg(['commit', '-m', 'add files', '-d', '0 0'])
hgt.writefile('n1', 'n11')
hgt.writefile('dir/dir/n4', 'n44')
hgt.writefile('b1', 'b11')
hgt.writefile('dir/dir/b4', 'b44')
hgt.hg(['commit', '-m', 'edit files', '-d', '1 0'])
hgt.hg(['remove', 'dir/n3', 'dir/b3'])
hgt.hg(['commit', '-m', 'remove files', '-d', '2 0'])

hgt.announce('backout')
hgt.hg(['status', '-A'],
        stdout='''C dir/b1
C dir/b2
C dir/dir/dir/b4
C dir/dir/dir/n4
C dir/n1
C dir/n2
''')
hgt.hg(['backout', '2', '-d', '3 0'],
        stdout='''getting changed bfiles
0 big files updated, 0 removed
adding ../.kbf/dir/dir/b3
adding dir/n3
changeset 3:ff0972d157df backs out changeset 2:99a2429e853e
''')
hgt.hg(['status', '-A'],
        stdout='''C dir/b1
C dir/b2
C dir/dir/b3
C dir/dir/dir/b4
C dir/dir/dir/n4
C dir/dir/n3
C dir/n1
C dir/n2
''')
hgt.asserttrue(hgt.readfile('dir/n3') == 'n3', 'file changed')
hgt.asserttrue(hgt.readfile('dir/b3') == 'b3', 'file changed')
hgt.hg(['backout', '3', '-d', '4 0'],
        stdout='''getting changed bfiles
0 big files updated, 0 removed
removing ../.kbf/dir/dir/b3
removing dir/n3
changeset 4:965678ed5519 backs out changeset 3:ff0972d157df
''')
hgt.hg(['status', '-A'],
        stdout='''C dir/b1
C dir/b2
C dir/dir/dir/b4
C dir/dir/dir/n4
C dir/n1
C dir/n2
''')
hgt.assertfalse(os.path.exists('dir/n3'), 'file shouldnt exist')
hgt.assertfalse(os.path.exists('dir/b3'), 'file shouldnt exist')
hgt.announce('backout... from the past!')
hgt.hg(['backout', '2', '-d', '5 0', '--merge'],
        stdout='''getting changed bfiles
0 big files updated, 0 removed
adding ../.kbf/dir/dir/b3
adding dir/n3
created new head
changeset 5:df61b823c9a6 backs out changeset 2:99a2429e853e
getting changed bfiles
0 big files updated, 1 removed
merging with changeset 5:df61b823c9a6
2 files updated, 0 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
1 big files updated, 0 removed
''')
hgt.hg(['commit', '-m', 'merge', '-d', '6 0'])
hgt.hg(['backout', '1', '--merge', '-d', '7 0'],
        stdout='''getting changed bfiles
0 big files updated, 0 removed
reverting ../.kbf/dir/b1
reverting ../.kbf/dir/dir/dir/b4
reverting dir/dir/n4
reverting n1
created new head
changeset 7:5e72be42125c backs out changeset 1:837f6fa72847
getting changed bfiles
2 big files updated, 0 removed
merging with changeset 7:5e72be42125c
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('n1') == 'n1', 'file should match start')
hgt.asserttrue(hgt.readfile('n2') == 'n2', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/n3') == 'n3', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/dir/n4') == 'n4', 'file should match start')
hgt.asserttrue(hgt.readfile('b1') == 'b1', 'file should match start')
hgt.asserttrue(hgt.readfile('b2') == 'b2', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/b3') == 'b3', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/dir/b4') == 'b4', 'file should match start')
hgt.hg(['commit', '-m', 'merge', '-d', '8 0'])
hgt.hg(['up', '-r', '0'],
        stdout='''4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('n1') == 'n1', 'file should match start')
hgt.asserttrue(hgt.readfile('n2') == 'n2', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/n3') == 'n3', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/dir/n4') == 'n4', 'file should match start')
hgt.asserttrue(hgt.readfile('b1') == 'b1', 'file should match start')
hgt.asserttrue(hgt.readfile('b2') == 'b2', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/b3') == 'b3', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/dir/b4') == 'b4', 'file should match start')
hgt.hg(['up'],
        stdout='''4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('n1') == 'n1', 'file should match start')
hgt.asserttrue(hgt.readfile('n2') == 'n2', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/n3') == 'n3', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/dir/n4') == 'n4', 'file should match start')
hgt.asserttrue(hgt.readfile('b1') == 'b1', 'file should match start')
hgt.asserttrue(hgt.readfile('b2') == 'b2', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/b3') == 'b3', 'file should match start')
hgt.asserttrue(hgt.readfile('dir/dir/b4') == 'b4', 'file should match start')
hgt.writefile('b1', 'b11')
hgt.hg(['backout', '8', '-d', '9 0'], status=255,
        stderr='abort: outstanding uncommitted changes\n')
