#!/usr/bin/env python
#
# Test basic kiln interaction

import os
import common
import time

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
hgt.hg(['push'],
        stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
# edit to time so that server doesn't have it cached
contents = str(time.clock())
hgt.writefile('n1', contents)
hgt.writefile('b1', contents )
hgt.hg(['commit', '-m', 'edit n1 and b1'])

# turn bfiles off for testing
hgt.announce('test with no bfiles')
hgt.updaterc({'extensions': [('kbfiles', '!')]})
os.chdir('../..')
hgt.hg(['clone', test[0], 'repo2'],
        stdout='requesting all changes\n', log=False,
        stderr='abort: HTTP Error 400: To access this repository, install the kiln-bfiles extension from %s/Tools\n' % kilntest.KILNURL, status=255)
os.chdir('repo1')
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
remote: ERROR: Big file a/b1 at revision 1 has not been uploaded to the kiln server.
remote: ERROR: All big files must be uploaded to the kiln server before the repository is changed.
remote: transaction abort!
remote: rollback completed
remote: abort: pretxnchangegroup hook failed
''' % kilntest.KILNURL, status=1)
