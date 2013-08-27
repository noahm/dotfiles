#!/usr/bin/env python

# Test various tricky bfadd corner cases.

import os
import common

hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('normal1', 'foo')
os.mkdir('sub')
hgt.writefile('sub/normal2', 'bar')
hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.hg(['add', 'normal1', 'sub/normal2'])
hgt.hg(['add', '--bf', 'big1', 'sub/big2'])
hgt.hg(['commit', '-m', 'add files'])

hgt.writefile('normal1', 'foo1')
hgt.writefile('sub/normal2', 'bar1')
hgt.writefile('big1', 'abc1')
hgt.writefile('sub/big2', 'xyz1')
hgt.hg(['commit', '-m', 'edit files'])

hgt.writefile('normal1', 'foo2')
hgt.writefile('sub/normal2', 'bar2')
hgt.writefile('big1', 'abc2')
hgt.writefile('sub/big2', 'xyz2')
hgt.hg(['commit', '-m', 'edit files'])

hgt.writefile('normal1', 'foo3')
hgt.writefile('sub/normal2', 'bar3')
hgt.writefile('big1', 'abc3')
hgt.writefile('sub/big2', 'xyz3')
hgt.hg(['commit', '-m', 'edit files'])

hgt.writefile('normal1', 'foo4')
hgt.writefile('sub/normal2', 'bar4')
hgt.writefile('big1', 'abc4')
hgt.writefile('sub/big2', 'xyz4')
hgt.hg(['commit', '-m', 'edit files'])

hgt.announce('bisect')
hgt.hg(['up', '-r', '0', '-q'])
hgt.hg(['bisect', '-g'])
hgt.hg(['up', '-q'])
hgt.hg(['bisect', '-b'],
    stdout='''Testing changeset 2:04f4251bb360 (4 changesets remaining, ~2 tests)
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.writefile('big1', 'blah')
hgt.hg(['bisect', '-g'], stdout='Testing changeset 3:bbc1532f9dcf (2 changesets remaining, ~1 tests)\n', stderr='abort: outstanding uncommitted changes\n', status=255)
hgt.hg(['revert', '-a'], stdout='reverting .kbf/big1\n')
hgt.hg(['bisect', '-g'], stdout='''Testing changeset 3:bbc1532f9dcf (2 changesets remaining, ~1 tests)
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.hg(['bisect', '-b'],
        stdout='''The first bad revision is:
changeset:   3:bbc1532f9dcf
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit files

''')
hgt.hg(['up'],
        stdout='''4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')

hgt.announce('more changes')
hgt.hg(['mv', 'sub', 'dir'],
        stdout='''moving sub/normal2 to dir/normal2
moving .kbf/sub/big2 to .kbf/dir/big2
''')
hgt.hg(['commit', '-m', 'move sub to dir'])
hgt.hg(['rm', 'normal1', 'big1'])
hgt.hg(['cp', 'dir/normal2', 'normal1'])
hgt.hg(['cp', 'dir/big2', 'big1'])
hgt.hg(['commit', '-m', 'remove and copy'])

hgt.announce('bisect again')
hgt.hg(['bisect', '-r'])
hgt.hg(['bisect', '-b'])
hgt.hg(['up', '-r', '1'],
        stdout='''4 files updated, 0 files merged, 2 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 1 removed
''')
hgt.hg(['bisect', '-g'],
        stdout='''Testing changeset 3:bbc1532f9dcf (5 changesets remaining, ~2 tests)
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.hg(['bisect', '-g'],
        stdout='''Testing changeset 4:de7b6579c9e2 (3 changesets remaining, ~1 tests)
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.hg(['bisect', '-g'],
        stdout='''Testing changeset 5:5e56aef38802 (2 changesets remaining, ~1 tests)
2 files updated, 0 files merged, 2 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 1 removed
''')
hgt.hg(['bisect', '-g'],
        stdout='''The first bad revision is:
changeset:   6:4847c1b5966e
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove and copy

''')
hgt.hg(['up'],
        stdout='''2 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
''')
