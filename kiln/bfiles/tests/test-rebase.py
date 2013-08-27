#!/usr/bin/python
#
# Test rebasing
#

import os
import common

hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('n1', 'n1')
hgt.hg(['add'],
        stdout='adding n1\n')
hgt.hg(['commit', '-m', 'add n1 in repo1'])
hgt.writefile('b1', 'b1')
hgt.hg(['add', '--bf', 'b1'])
hgt.hg(['commit', '-m', 'add bfile b1 in repo1'])
os.chdir('..')
hgt.hg(['clone', 'repo1', 'repo2'],
        stdout='''updating to branch default
2 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
''')
os.chdir('repo1')
hgt.writefile('b1', 'b11')
hgt.hg(['commit', '-m', 'modify bfile b1 in repo1'])
os.chdir('../repo2')
hgt.writefile('n1', 'n11')
hgt.hg(['commit', '-m', 'modify n1 in repo2'])
hgt.hg(['pull', '--rebase'],
        stdout='''pulling from $HGTMP/test-rebase.py/repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 1 changes to 1 files (+1 heads)
getting changed bfiles
1 big files updated, 0 removed
saved backup bundle to $HGTMP/test-rebase.py/repo2/.hg/strip-backup/f525225f596a-backup.hg
nothing to rebase
''')
hgt.hg(['out', '--bf'],
        stdout='''comparing with $HGTMP/test-rebase.py/repo1
searching for changes
changeset:   3:05e3d87e7926
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify n1 in repo2

searching for changes
kbfiles to upload:

''')
hgt.writefile('n1', 'n111')
hgt.hg(['commit', '-m', 'modify n1'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with $HGTMP/test-rebase.py/repo1
searching for changes
changeset:   3:05e3d87e7926
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify n1 in repo2

changeset:   4:930afbf48fd0
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify n1

searching for changes
kbfiles to upload:

''')
hgt.hg(['update', '--clean'],
        stdout='''0 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('b1') == 'b11', "file contents don't match")

# Now do the exact same thing with the rebase command instead of pull --rebase
os.chdir('..')
os.mkdir('repo3')
os.chdir('repo3')
hgt.hg(['init'])
hgt.writefile('n1', 'n1')
hgt.hg(['add'],
        stdout='adding n1\n')
hgt.hg(['commit', '-m', 'add n1 in repo3'])
hgt.writefile('b1', 'b1')
hgt.hg(['add', '--bf', 'b1'])
hgt.hg(['commit', '-m', 'add bfile b1 in repo3'])
os.chdir('..')
hgt.hg(['clone', 'repo3', 'repo4'],
        stdout='''updating to branch default
2 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
''')
os.chdir('repo3')
hgt.writefile('b1', 'b11')
hgt.hg(['commit', '-m', 'modify bfile b1 in repo3'])
os.chdir('../repo4')
hgt.writefile('n1', 'n11')
hgt.hg(['commit', '-m', 'modify n1 in repo4'])
hgt.hg(['pull'],
        stdout='''pulling from $HGTMP/test-rebase.py/repo3
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 1 changes to 1 files (+1 heads)
(run \'hg heads\' to see heads, \'hg merge\' to merge)
''')

hgt.hg(['rebase'],
        stdout='''getting changed bfiles
1 big files updated, 0 removed
saved backup bundle to $HGTMP/test-rebase.py/repo4/.hg/strip-backup/f2a8d31d0111-backup.hg
''')
hgt.hg(['out', '--bf'],
        stdout='''comparing with $HGTMP/test-rebase.py/repo3
searching for changes
changeset:   3:417329feeb39
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify n1 in repo4

searching for changes
kbfiles to upload:

''')
hgt.writefile('n1', 'n111')
hgt.hg(['commit', '-m', 'modify n1'])
hgt.hg(['out', '--bf'],
        stdout='''comparing with $HGTMP/test-rebase.py/repo3
searching for changes
changeset:   3:417329feeb39
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify n1 in repo4

changeset:   4:8cdec458685b
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify n1

searching for changes
kbfiles to upload:

''')
hgt.hg(['update', '--clean'],
        stdout='''0 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('b1') == 'b11', "file contents don't match")
