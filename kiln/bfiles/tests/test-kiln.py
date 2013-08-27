#!/usr/bin/env python
#
# Test basic kiln interaction

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('kilnauth', kilntest.KILNAUTHPATH)]})
hgt.announce('setup')
token = kilntest.gettoken()
kilntest.deletetest(hgt, token)
test = kilntest.createtest(hgt, token)
# Don't log this because command depends on path to kiln which can change
hgt.hg(['clone', test[0], 'repo1'],
            stdout='''no changes found
updating to branch default
0 files updated, 0 files merged, 0 files removed, 0 files unresolved
''', log=False)
os.chdir('repo1')
os.mkdir('a')
os.mkdir('a/b')
os.mkdir('a/b/c')
os.chdir('a')
hgt.writefile('n1', 'n1')
hgt.writefile('b/n2', 'n2')
hgt.writefile('b/c/n3', 'n3')
hgt.writefile('../n4', 'n4')
hgt.writefile('b1', 'b1')
hgt.writefile('b/b2', 'b2')
hgt.writefile('b/c/b3', 'b3')
hgt.writefile('../b4', 'b4')
hgt.hg(['add', 'n1', 'b/n2', 'b/c/n3', '../n4'])
hgt.hg(['add', '--bf'],
        stdout='''adding b/b2 as bfile
adding b/c/b3 as bfile
adding b1 as bfile
adding ../b4 as bfile
''')
hgt.hg(['commit', '-m', 'add files'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   0:da6857b8d2bf
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add files

searching for changes
kbfiles to upload:
a/b1
b4
a/b/b2
a/b/c/b3

''' % kilntest.KILNURL)
hgt.hg(['summary', '--remote', '--bf'],
        stdout='''parent: 0:da6857b8d2bf tip
 add files
branch: default
commit: 4 unknown (clean)
update: (current)
remote: 1 outgoing
searching for changes
kbfiles: 4 to upload
''')
hgt.hg(['push'],
        stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
no changes found
searching for changes
kbfiles: No remote repo
''' % kilntest.KILNURL)

os.chdir('../..')
hgt.hg(['clone', test[0], 'repo2'], log=False,
        stdout='''requesting all changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 8 changes to 8 files
updating to branch default
8 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
4 big files updated, 0 removed
''')
os.chdir('repo2')
hgt.hg(['in'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
no changes found
''' % kilntest.KILNURL, status=1)
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
no changes found
searching for changes
kbfiles: No remote repo
''' % kilntest.KILNURL)
hgt.writefile('n4', 'n44')
hgt.writefile('b4', 'b44')
hgt.hg(['commit', '-m', 'edit n4 and b4'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   1:8499483c24d0
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit n4 and b4

searching for changes
kbfiles to upload:
b4

''' % kilntest.KILNURL)
hgt.hg(['push'],
        stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
os.chdir('../repo1')
hgt.hg(['in'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   1:8499483c24d0
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit n4 and b4

''' % kilntest.KILNURL)
hgt.hg(['out'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
no changes found
''' % kilntest.KILNURL)
hgt.hg(['mv', 'n4', 'b4', 'a'])
hgt.hg(['commit', '-m', 'move n4 and b4'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   1:6b693340d9c6
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move n4 and b4

searching for changes
kbfiles to upload:
a/b4

''' % kilntest.KILNURL)
# A line of the output message from the below command changes from stdout
# to stderr at some version after Mercurial 1.6. Just don't check stdout/stderr.
hgt.hg(['push'], stdout=hgtest.ANYTHING, stderr=hgtest.ANYTHING, status=[1, 255])
hgt.hg(['pull'],
        stdout='''pulling from %s/Repo/Test/Test/Test
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''' % kilntest.KILNURL)
hgt.hg(['merge'],
        stdout='''merging a/b4 and b4 to a/b4
merging a/n4 and n4 to a/n4
0 files updated, 2 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
getting changed bfiles
1 big files updated, 0 removed
''')
hgt.hg(['commit', '-m', 'merge'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   1:6b693340d9c6
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move n4 and b4

changeset:   3:01193a291cb0
tag:         tip
parent:      1:6b693340d9c6
parent:      2:8499483c24d0
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     merge

searching for changes
kbfiles to upload:
a/b4

''' % kilntest.KILNURL)
hgt.hg(['summary', '--remote', '--bf'],
        stdout='''parent: 3:01193a291cb0 tip
 merge
branch: default
commit: 4 unknown (clean)
update: (current)
remote: 2 outgoing
searching for changes
kbfiles: 1 to upload
''')
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed 2 changesets
''' % kilntest.KILNURL)
os.chdir('../repo2')
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
no changes found
searching for changes
kbfiles: No remote repo
''' % kilntest.KILNURL)
hgt.hg(['in'], stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   2:6b693340d9c6
parent:      0:da6857b8d2bf
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move n4 and b4

changeset:   3:01193a291cb0
tag:         tip
parent:      2:6b693340d9c6
parent:      1:8499483c24d0
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     merge

''' % kilntest.KILNURL)
hgt.hg(['pull'], stdout='''pulling from %s/Repo/Test/Test/Test
searching for changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 4 changes to 2 files
(run 'hg update' to get a working copy)
''' % kilntest.KILNURL)
hgt.hg(['in'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
no changes found
''' % kilntest.KILNURL, status=1)
hgt.hg(['up'],
        stdout='''2 files updated, 0 files merged, 2 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 1 removed
''')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3])
os.chdir('repo2')
hgt.writefile('a/n1', 'n11')
hgt.writefile('a/b1', 'b11')
hgt.hg(['commit', '-m', 'edit n1 and b1'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   4:fdb0cdc62a97
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit n1 and b1

searching for changes
kbfiles to upload:
a/b1

''' % kilntest.KILNURL)
os.chdir('../repo1')
hgt.hg(['pull', '../repo2'],
        stdout='''pulling from ../repo2
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
(run 'hg update' to get a working copy)
''')
hgt.hg(['up'],
        stdout='''2 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
''')
hgt.writefile('a/b/n2', 'n22')
hgt.writefile('a/b/b2', 'b22')
hgt.hg(['commit', '-m', 'edit n22 and b22'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with %s/Repo/Test/Test/Test
searching for changes
changeset:   4:fdb0cdc62a97
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit n1 and b1

changeset:   5:f79826fcf061
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit n22 and b22

searching for changes
kbfiles to upload:
a/b1
a/b/b2

''' % kilntest.KILNURL)
hgt.hg(['summary', '--remote', '--bf'],
        stdout='''parent: 5:f79826fcf061 tip
 edit n22 and b22
branch: default
commit: 4 unknown (clean)
update: (current)
remote: 2 outgoing
searching for changes
kbfiles: 2 to upload
''')
hgt.hg(['push'],
        stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed 2 changesets
''' % kilntest.KILNURL)
os.chdir('../repo2')
hgt.hg(['pull'],
        stdout='''pulling from %s/Repo/Test/Test/Test
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
(run 'hg update' to get a working copy)
''' % kilntest.KILNURL)
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 3, 4, 5])
