#!/usr/bin/env python
#
# Test hg kiln -t and path guessing

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('kilnauth', kilntest.KILNAUTHPATH),
                             ('kiln', kilntest.KILNPATH)],
              'hostfingerprints': [('developers.kilnhg.com', 'fe:ab:65:89:7c:6f:1a:21:a8:39:54:6c:2a:cb:ca:ae:e9:e5:f0:01')],
              'kiln_scheme': [('kiln', kilntest.KILNURL + '/Repo')]})
hgt.announce('setup')
token = kilntest.gettoken()
kilntest.deletetest(hgt, token)
test = kilntest.createtest(hgt, token)
testurl, ixParent = test
hgt.hg(['clone', kilntest.KILNURL + '/Repo/Test/Test/Test', 'repo1'], log=False,
        stdout='''no changes found
updating to branch default
0 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
os.chdir('repo1')
hgt.writefile('n1', 'n1')
hgt.hg(['add', 'n1'])
hgt.hg(['commit', '-m', 'add file'])
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
testbranch = kilntest.createtestbranch(hgt, token, ixParent)
hgt.hg(['kiln', '-t'], '''The following Kiln targets are available for this repository:

    %s/Repo/Test/Test/Test
    %s/Repo/Test/Test/TestBranch
''' % (kilntest.KILNURL, kilntest.KILNURL))
hgt.writefile('n2', 'n2')
hgt.hg(['add', 'n2'])
hgt.hg(['commit', '-m', 'add to central repository'])
hgt.hg(['push', 'Test'], status=255, stderr='''abort: Test matches more than one Kiln repository:

    %s/Repo/Test/Test/Test
    %s/Repo/Test/Test/TestBranch

''' % (kilntest.KILNURL, kilntest.KILNURL))
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
hgt.writefile('n3', 'n3')
hgt.hg(['add', 'n3'])
hgt.hg(['commit', '-m', 'add to branch repository'])
hgt.hg(['outgoing', 'TestBranch'], stdout='''comparing with %s/Repo/Test/Test/TestBranch
searching for changes
changeset:   1:ab1d97532947
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add to central repository

changeset:   2:b2faa98b26f6
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add to branch repository

''' % kilntest.KILNURL)
hgt.hg(['push', 'TestBranch'], stdout='''pushing to %s/Repo/Test/Test/TestBranch
searching for changes
searching for changes
remote: kiln: successfully pushed 2 changesets
''' % kilntest.KILNURL)
os.chdir('..')
hgt.hg(['clone', kilntest.KILNURL + '/Repo/Test/Test/Test', 'repo2'], log=False,
        stdout='''requesting all changes
adding changesets
adding manifests
adding file changes
added 2 changesets with 2 changes to 2 files
updating to branch default
2 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
os.chdir('repo2')
hgt.hg(['incoming', 'TestBranch'], stdout='''comparing with %s/Repo/Test/Test/TestBranch
searching for changes
changeset:   2:b2faa98b26f6
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add to branch repository

''' % kilntest.KILNURL)
hgt.hg(['pull', 'TestBranch'], stdout='''pulling from %s/Repo/Test/Test/TestBranch
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 1 changes to 1 files
(run 'hg update' to get a working copy)
''' % kilntest.KILNURL)
os.chdir('..')

