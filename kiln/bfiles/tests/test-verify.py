#!/usr/bin/env python
#
# Test verify

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

hgt.announce('verify')
os.chdir('repo1')
hgt.hg(['verify', '--bf'],
        stdout='''checking changesets
checking manifests
crosschecking files in changesets and manifests
checking files
4 files, 1 changesets, 4 total revisions
searching 1 changesets for big files
verified existence of 2 revisions of 2 big files
''')
os.chdir('../repo2')
hgt.hg(['verify', '--bf'],
        stdout='''checking changesets
checking manifests
crosschecking files in changesets and manifests
checking files
4 files, 2 changesets, 6 total revisions
searching 1 changesets for big files
verified existence of 2 revisions of 2 big files
''')
hgt.hg(['push', '../repo1'],
        stdout='''pushing to ../repo1
searching for changes
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
''')
hgt.hg(['verify', '--bf', '--bfa'],
        stdout='''checking changesets
checking manifests
crosschecking files in changesets and manifests
checking files
4 files, 2 changesets, 6 total revisions
searching 2 changesets for big files
verified existence of 3 revisions of 2 big files
''')
hgt.hg(['verify', '--bf', '--bfc', '--bfa'],
    stdout='''checking changesets
checking manifests
crosschecking files in changesets and manifests
checking files
4 files, 2 changesets, 6 total revisions
searching 2 changesets for big files
verified contents of 3 revisions of 2 big files
''')
os.chdir('../repo1')
hgt.hg(['verify', '--bf', '--bfc'],
        stdout='''checking changesets
checking manifests
crosschecking files in changesets and manifests
checking files
4 files, 2 changesets, 6 total revisions
searching 1 changesets for big files
verified contents of 2 revisions of 2 big files
''')
hgt.hg(['verify', '--bf', '--bfc', '--bfa'],
        stdout='''checking changesets
checking manifests
crosschecking files in changesets and manifests
checking files
4 files, 2 changesets, 6 total revisions
searching 2 changesets for big files
verified contents of 3 revisions of 2 big files
''')
