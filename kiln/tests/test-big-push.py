#!/usr/bin/env python
#
# Test big-push extension

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('kilnauth', kilntest.KILNAUTHPATH),
                             ('big-push', kilntest.BIGPUSHPATH)]})
hgt.announce('setup')
token = kilntest.gettoken()
kilntest.deletetest(hgt, token)
test = kilntest.createtest(hgt, token)
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
hgt.writefile('n2', 'n2')
hgt.hg(['add', 'n2'])
hgt.hg(['commit', '-m', 'add another file'])
hgt.hg(['push', '--chunked'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
for i in range(3, 25):
    hgt.writefile('n%d' % i, 'dummy')
    hgt.hg(['add', 'n%d' % i])
    hgt.hg(['commit', '-m', 'changeset %d' % i])
hgt.hg(['push', '--chunked'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
searching for changes
searching for changes
remote: kiln: successfully pushed 2 changesets
searching for changes
searching for changes
remote: kiln: successfully pushed 4 changesets
searching for changes
searching for changes
remote: kiln: successfully pushed 8 changesets
searching for changes
searching for changes
remote: kiln: successfully pushed 7 changesets
''' % kilntest.KILNURL)
hgt.hg(['pull'], stdout='''pulling from %s/Repo/Test/Test/Test
searching for changes
no changes found
''' % kilntest.KILNURL)
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
no changes found
''' % kilntest.KILNURL)
os.chdir('..')
hgt.hg(['clone', kilntest.KILNURL + '/Repo/Test/Test/Test', 'repo2'], log=False,
       stdout='''requesting all changes
adding changesets
adding manifests
adding file changes
added 24 changesets with 24 changes to 24 files
updating to branch default
24 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
