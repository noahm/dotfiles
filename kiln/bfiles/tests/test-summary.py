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

hgt.announce('summary')
os.chdir('repo1')
hgt.hg(['summary'],
        stdout='''parent: 0:372389b1b261 tip
 add files
branch: default
commit: 2 unknown (clean)
update: (current)
''')
hgt.hg(['summary', '--bf'],
        stdout='''parent: 0:372389b1b261 tip
 add files
branch: default
commit: 2 unknown (clean)
update: (current)
kbfiles: No remote repo
''')
hgt.hg(['summary', '--bf', '--remote'], status=255,
        stderr='abort: repository default not found!\n',
        stdout='''parent: 0:372389b1b261 tip
 add files
branch: default
commit: 2 unknown (clean)
update: (current)
''')
os.chdir('../repo2')
hgt.hg(['summary'],
        stdout='''parent: 1:c44ace51ad7e tip
 edit files
branch: default
commit: 2 unknown (clean)
update: (current)
''')
hgt.hg(['summary', '--bf'],
        stdout='''parent: 1:c44ace51ad7e tip
 edit files
branch: default
commit: 2 unknown (clean)
update: (current)
searching for changes
kbfiles: 1 to upload
''')
hgt.hg(['summary', '--bf', '--remote'],
        stdout='''parent: 1:c44ace51ad7e tip
 edit files
branch: default
commit: 2 unknown (clean)
update: (current)
remote: 1 outgoing
searching for changes
kbfiles: 1 to upload
''')
