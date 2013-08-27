#!/usr/bin/env python
#
# Test summary

import os
import common

hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('n1', 'n1')
hgt.writefile('b1', 'b1')
os.mkdir('dir')
hgt.writefile('dir/n2', 'n2')
hgt.writefile('dir/b2', 'b2')
hgt.hg(['add', 'n1', 'dir/n2'])
hgt.hg(['add', '--bf'],
        stdout='''adding b1 as bfile
adding dir/b2 as bfile
''')
hgt.hg(['commit', '-m', 'add files'])
os.chdir('..')
hgt.hg(['clone', 'repo1', 'repo2'],
        stdout='''updating to branch default
4 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
os.chdir('repo2')
hgt.writefile('n1', 'n11')
hgt.writefile('b1', 'b11')
hgt.hg(['commit', '-m', 'edit files'])
os.chdir('..')

hgt.announce('outgoing')
os.chdir('repo1')
if common.version >= (1, 8, 0):
    hgt.hg(['out'], status=255, stdout='comparing with default-push\n', stderr='abort: repository default-push not found!\n')
    hgt.hg(['out', '--bf'], status=255, stdout='comparing with default-push\n', stderr='abort: repository default-push not found!\n')
else:
    hgt.hg(['out'], status=255, stderr='abort: repository default-push not found!\n')
    hgt.hg(['out', '--bf'], status=255, stderr='abort: repository default-push not found!\n')
os.chdir('../repo2')
hgt.hg(['out'],
        stdout='''comparing with $HGTMP/test-outgoing.py/repo1
searching for changes
changeset:   1:c44ace51ad7e
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit files

''')
hgt.hg(['out', '--bf'],
        stdout='''comparing with $HGTMP/test-outgoing.py/repo1
searching for changes
changeset:   1:c44ace51ad7e
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit files

searching for changes
kbfiles to upload:
b1

''')
