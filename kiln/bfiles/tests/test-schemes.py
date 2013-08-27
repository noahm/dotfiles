#!/usr/bin/env python
#
# Test schemes with kiln

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.announce('setup')
token = kilntest.gettoken()
kilntest.deletetest(hgt, token)
test = kilntest.createtest(hgt, token)
hgt.updaterc({'extensions': [('kilnauth', kilntest.KILNAUTHPATH), ('hgext.schemes', '')], 'schemes': [('localkiln', kilntest.KILNURL + '/'), ('local', 'file://' + '/'.join(os.getcwd().split('\\')) + '/')]})
hgt.hg(['clone', 'localkiln://%s' % test[0][len(kilntest.KILNURL)+1:], 'repo1'],
            stdout='''no changes found
updating to branch default
0 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
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
        stdout='''pushing to localkiln://Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''')
os.chdir('../..')
os.mkdir('repo2')
hgt.hg(['clone', 'repo1', 'repo2'],
            stdout='''updating to branch default
8 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
4 big files updated, 0 removed
''')
common.checkrepos(hgt, 'repo1', 'repo2', [0])
os.chdir('repo2/a')
os.unlink('../.hg/hgrc')
hgt.writefile('n1', 'n11')
hgt.writefile('b/n2', 'n22')
hgt.writefile('b/c/n3', 'n33')
hgt.writefile('../n4', 'n44')
hgt.writefile('b1', 'b11')
hgt.writefile('b/b2', 'b22')
hgt.writefile('b/c/b3', 'b33')
hgt.writefile('../b4', 'b44')
hgt.hg(['commit', '-m', 'edit files'])
hgt.hg(['out', 'local://repo1/', '--bf'],
        stdout='''comparing with local://repo1/
searching for changes
changeset:   1:7235bdef417c
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit files

searching for changes
kbfiles to upload:
a/b1
b4
a/b/b2
a/b/c/b3

''')
hgt.hg(['push', 'local://repo1/'],
        stdout='''pushing to local://repo1/
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 8 changes to 8 files
''')
os.chdir('../..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 1])
