#!/usr/bin/env python
#
# Test kilnpath extension

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('kilnauth', kilntest.KILNAUTHPATH),
                             ('kilnpath', kilntest.KILNPATHPATH)],
              'kiln_scheme': [('kiln', kilntest.KILNURL + '/Repo')]})
hgt.announce('setup')
token = kilntest.gettoken()
kilntest.deletetest(hgt, token)
test = kilntest.createtest(hgt, token)
hgt.hg(['clone', 'kiln://Test/Test/Test', 'repo1'],
        stdout='''no changes found
updating to branch default
0 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
os.chdir('repo1')
hgt.hg(['pull'], stdout='''pulling from kiln://Test/Test/Test
no changes found
''')
hgt.hg(['pull', 'kiln://Test/Test/Test'], stdout='''pulling from kiln://Test/Test/Test
no changes found
''')
hgt.writefile('n1', 'n1')
hgt.hg(['add', 'n1'])
hgt.hg(['commit', '-m', 'add file'])
hgt.hg(['push'], stdout='''pushing to kiln://Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''')
hgt.writefile('n2', 'n2')
hgt.hg(['add', 'n2'])
hgt.hg(['commit', '-m', 'add another file'])
hgt.hg(['push', 'kiln://Test/Test/Test'], stdout='''pushing to kiln://Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''')
os.chdir('..')
