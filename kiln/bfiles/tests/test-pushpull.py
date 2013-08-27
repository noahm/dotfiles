#!/usr/bin/env python

# Test push pull

import os
import common

hgt = common.BfilesTester()

# add size and patterns for adding as bfiles
hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
os.mkdir('dir')
hgt.writefile('b1', 'b1')
hgt.writefile('n1', 'n1')
hgt.writefile('dir/b2', 'b2')
hgt.writefile('dir/n2', 'n2')
hgt.hg(['add', '--bf', 'b1', 'dir/b2'])
hgt.hg(['add', 'n1', 'dir/n2'])
hgt.hg(['commit', '-m', 'added files'])
os.chdir('..')
hgt.hg(['clone', 'repo1', 'repo2'],
        stdout='''updating to branch default
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
common.checkrepos(hgt, 'repo1', 'repo2', [0])

hgt.announce('push and merge')
os.chdir('repo2')
hgt.writefile('dir/b2', 'b3')
hgt.writefile('dir/n2', 'n3')
hgt.writefile('b3', 'b3')
hgt.writefile('n3', 'n3')
hgt.hg(['add', '--bf', 'b3'])
hgt.hg(['add', 'n3'])
hgt.hg(['commit', '-m', 'changed and add'])
os.chdir('../repo1')
hgt.writefile('b1', 'b2')
hgt.writefile('n1', 'n2')
hgt.writefile('dir/b4', 'b4')
hgt.writefile('dir/n4', 'n4')
hgt.hg(['add', '--bf', 'dir/b4'])
hgt.hg(['add', 'dir/n4'])
hgt.hg(['commit', '-m', 'changed and add'])
hgt.hg(['pull', '../repo2'],
        stdout='''pulling from ../repo2
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 4 changes to 4 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''')
hgt.hg(['merge'],
        stdout='''4 files updated, 0 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.asserttrue(os.path.exists('b3'), 'merged bfile should exist')
hgt.asserttrue(os.path.exists('.kbf/b3'), 'merged bfile should exist')
hgt.hg(['commit', '-m', 'merge'])
hgt.hg(['push', '../repo2'],
        stdout='''pushing to ../repo2
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 4 changes to 4 files
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3])

hgt.announce('just push')
os.chdir('repo2')
hgt.hg(['remove', 'b3'])
hgt.writefile('b1', 'tomrocks')
hgt.hg(['commit', '-m', 'update files'])
hgt.hg(['push', '../repo1'],
        stdout='''pushing to ../repo1
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 1 changes to 1 files
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4])

os.chdir('repo1')
hgt.writefile('dir/b1.foo', 'foo1')
hgt.writefile('dir/b2.foo', 'foo1')
hgt.writefile('dir/b3.foo', 'foo1')
hgt.writefile('dir/b4.foo', 'foo1')
hgt.writefile('dir/b5', 'should not add')
hgt.writefile('dir/blahblah', 'should not add')
hgt.writefile('dir/stuffnthings', 'should not add')
hgt.hg(['add', '--bf', 'glob:**.foo'],
        stdout='''adding dir/b1.foo as bfile
adding dir/b2.foo as bfile
adding dir/b3.foo as bfile
adding dir/b4.foo as bfile
''')
hgt.hg(['commit', '-m', 'add some files'])
hgt.hg(['status', '-A'],
        stdout='''? dir/b5
? dir/blahblah
? dir/stuffnthings
C b1
C dir/b1.foo
C dir/b2
C dir/b2.foo
C dir/b3.foo
C dir/b4
C dir/b4.foo
C dir/n2
C dir/n4
C n1
C n3
''')
os.unlink('dir/b5')
os.unlink('dir/blahblah')
os.unlink('dir/stuffnthings')
hgt.hg(['status', '-A'],
        stdout='''C b1
C dir/b1.foo
C dir/b2
C dir/b2.foo
C dir/b3.foo
C dir/b4
C dir/b4.foo
C dir/n2
C dir/n4
C n1
C n3
''')
hgt.hg(['push', '../repo2'],
        stdout='''pushing to ../repo2
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 4 changes to 4 files
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4, 5])

hgt.announce('rename edit')
os.chdir('repo1')
hgt.writefile('dir/b2.foo', 'foo2')
hgt.writefile('n1', 'change normal1')
hgt.hg(['commit', '-m', 'edit b2.foo and n1'])
os.chdir('../repo2')
hgt.hg(['rename', 'dir/b2.foo', 'dir/b2222.foo'])
hgt.hg(['rename', 'n1', 'n1111'])
hgt.hg(['commit', '-m', 'rename b2.foo and n1'])
hgt.hg(['pull', '../repo1'],
        stdout='''pulling from ../repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''')
hgt.hg(['heads'],
        stdout='''changeset:   7:4ca7018cd3ad
tag:         tip
parent:      5:9ac6c128161c
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit b2.foo and n1

changeset:   6:09ca64279b78
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     rename b2.foo and n1

''')
hgt.hg(['merge'],
        stdout='''merging dir/b2222.foo and dir/b2.foo to dir/b2222.foo
merging n1111 and n1 to n1111
0 files updated, 2 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
1 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('dir/b2222.foo') == 'foo2', 'merge failed')
hgt.hg(['commit', '-m', 'merge'])
os.chdir('../repo1')
hgt.hg(['pull', '../repo2'],
        stdout='''pulling from ../repo2
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 4 changes to 2 files
(run 'hg update' to get a working copy)
''')
hgt.hg(['up'],
        stdout='''2 files updated, 0 files merged, 2 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 1 removed
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4, 5, 8])

hgt.announce('both edit to same value')
os.chdir('repo2')
hgt.writefile('dir/b3.foo', 'change')
hgt.writefile('n3', 'change')
# Set date because otherwise the two commits will be identical
# because the test suite normally changes dates to one value
hgt.hg(['commit', '-m', 'change dir/b3.foo and n3', '-d', '2007-1-1'])
os.chdir('../repo1')
hgt.writefile('dir/b3.foo', 'change')
hgt.writefile('n3', 'change')
hgt.hg(['commit', '-m', 'change dir/b3.foo and n3', '-d', '2006-1-1'])
hgt.hg(['pull', '../repo2'],
        stdout='''pulling from ../repo2
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 0 changes to 2 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''')
hgt.hg(['merge'],
        stdout='''0 files updated, 0 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.hg(['commit', '-m', 'merge'])
os.chdir('../repo2')
hgt.hg(['pull', '../repo1'],
        stdout='''pulling from ../repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 0 changes to 2 files
(run 'hg update' to get a working copy)
''')
hgt.hg(['up'],
        stdout='''0 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4, 5, 8, 11])

hgt.announce('delete edit')
os.chdir('repo1')
hgt.hg(['rm', 'dir/b3.foo', 'n3'])
hgt.hg(['commit', '-m', 'remove dir/b3.foo and n3'])
os.chdir('../repo2')
hgt.writefile('dir/b3.foo', 'changechange')
hgt.writefile('n3', 'changechange')
hgt.hg(['commit', '-m', 'edit dir/b3.foo and n3'])
hgt.hg(['pull', '../repo1'],
        stdout='''pulling from ../repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 0 changes to 0 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''')
hgt.hg(['merge'],
        stdout=''' local changed .kbf/dir/b3.foo which remote deleted
use (c)hanged version or (d)elete? c
 local changed n3 which remote deleted
use (c)hanged version or (d)elete? c
0 files updated, 0 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.hg(['commit', '-m', 'merge'])
hgt.hg(['push', '../repo1'],
        stdout='''pushing to ../repo1
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 2 changes to 2 files
''')
os.chdir('../repo1')
hgt.hg(['up'],
        stdout='''2 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4, 5, 8, 11, 14])

hgt.announce('copy edit')
os.chdir('repo1')
hgt.hg(['cp', 'dir/b3.foo', 'dir/b3333.foo'])
hgt.hg(['cp', 'n3', 'n3333'])
hgt.hg(['commit', '-m', 'copy dir/b3.foo and n3'])
os.chdir('../repo2')
hgt.writefile('dir/b3.foo', 'changechangechange')
hgt.writefile('n3', 'changechangechange')
hgt.hg(['commit', '-m', 'edit dir/b3.foo and n3'])
hgt.hg(['pull', '../repo1'],
        stdout='''pulling from ../repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''')
hgt.hg(['merge'],
        stdout='''merging dir/b3.foo and dir/b3333.foo to dir/b3333.foo
merging n3 and n3333 to n3333
0 files updated, 2 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
1 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('dir/b3.foo') == 'changechangechange', 'merge failed')
hgt.asserttrue(hgt.readfile('dir/b3333.foo') == 'changechangechange', 'merge failed')
hgt.hg(['commit', '-m', 'merge'])
hgt.hg(['push', '../repo1'],
        stdout='''pushing to ../repo1
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 4 changes to 4 files
''')
os.chdir('../repo1')
hgt.hg(['up'],
        stdout='''4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4, 5, 8, 11, 14, 17])

hgt.announce('no default path error')
os.mkdir('repo3')
os.chdir('repo3')
hgt.hg(['init'])
hgt.hg(['pull', '../repo1'],
        stdout='''pulling from ../repo1
requesting all changes
adding changesets
adding manifests
adding file changes
added 18 changesets with 33 changes to 16 files
(run 'hg update' to get a working copy)
''')
hgt.writefile('.hg/hgrc', '''[kilnbfiles]
systemcache = .
''')
hgt.hg(['up'],
        stdout='''13 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''', stderr='''b1: Can't get file locally
(no default or default-push path set in hgrc)
dir/b1.foo: Can't get file locally
(no default or default-push path set in hgrc)
dir/b2: Can't get file locally
(no default or default-push path set in hgrc)
dir/b2222.foo: Can't get file locally
(no default or default-push path set in hgrc)
dir/b3.foo: Can't get file locally
(no default or default-push path set in hgrc)
dir/b3333.foo: Can't get file locally
(no default or default-push path set in hgrc)
dir/b4: Can't get file locally
(no default or default-push path set in hgrc)
dir/b4.foo: Can't get file locally
(no default or default-push path set in hgrc)
''')
