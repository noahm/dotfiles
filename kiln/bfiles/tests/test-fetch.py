#!/usr/bin/env python
#
# Test the fetch extension. Always give it a specific message because the message
# it automatically adds includes the path which is randomly generated.
import os
import common

hgt = common.BfilesTester()

# add size and patterns for adding as bfiles
hgt.updaterc({'extensions':[('fetch','')]})
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
os.chdir('repo1')
hgt.writefile('n1', 'n11')
hgt.writefile('b1', 'b11')
hgt.hg(['commit', '-m', 'edit files'])
os.chdir('..')

hgt.announce('fetch')
os.chdir('repo2')
hgt.hg(['fetch', '../repo1', '-d', '1 0', '-m', 'automated merge'],
        stdout='''pulling from ../repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
2 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
''')
hgt.hg(['mv', 'dir/n2', 'n2'])
hgt.hg(['mv', 'dir/b2', 'b2'])
hgt.hg(['commit', '-m', 'move files'])
os.chdir('../repo1')
hgt.writefile('dir/n2', 'n22')
hgt.writefile('dir/b2', 'b22')
hgt.hg(['commit', '-m', 'edit files'])
hgt.hg(['fetch', '../repo2', '-d', '2 0', '-m', 'automated merge'],
        stdout='''pulling from ../repo2
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files (+1 heads)
updating to 3:04650d35496d
2 files updated, 0 files merged, 2 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 1 removed
merging with 2:6db24b20137f
merging b2 and dir/b2 to b2
merging n2 and dir/n2 to n2
0 files updated, 2 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 0 removed
new changeset 4:dacf855d6b8a merges remote changes with local
''')
