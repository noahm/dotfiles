#!/usr/bin/env python

# Test various tricky bfadd corner cases.

import os
import common

hgt = common.BfilesTester()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
os.mkdir('dir')
os.mkdir('dir/a')
os.mkdir('dir/b')
os.mkdir('dir/b/c')
os.mkdir('z')
hgt.writefile('foo.dat', 'stuffnthings')
hgt.writefile('foo', 'stuffnthings')
hgt.writefile('dir/big.dat', 'a'*(1024*1024*3))
hgt.writefile('dir/big', 'a'*(1024*1024*3))
hgt.writefile('dir/a/small.dat', 'small')
hgt.writefile('dir/a/small', 'small')
hgt.hg(['add'],
        stdout='''adding dir/a/small
adding dir/a/small.dat
adding dir/big
adding dir/big.dat
adding foo
adding foo.dat
''')
hgt.hg(['commit', '-m', 'initial commit'])
hgt.writefile('dir/b/medium.dat', 'b'*(1024*1024))
hgt.writefile('dir/b/medium', 'b'*(1024*1024))
hgt.writefile('dir/b/c/foo.dat', 'foo')
hgt.writefile('dir/b/c/foo', 'foo')
hgt.writefile('z/bigbig.dat', 'c'*(1024*1024*5))
hgt.writefile('z/bigbig', 'c'*(1024*1024*5))
hgt.hg(['add'],
        stdout='''adding dir/b/c/foo
adding dir/b/c/foo.dat
adding dir/b/medium
adding dir/b/medium.dat
adding z/bigbig
adding z/bigbig.dat
''')
hgt.hg(['commit', '-m', 'add more files'])
hgt.writefile('foo.dat', 'stuffnthings2')
hgt.writefile('foo', 'stuffnthings2')
hgt.writefile('z/bigbig.dat', 'd'*(1024*1024*5))
hgt.writefile('z/bigbig', 'd'*(1024*1024*5))
hgt.hg(['commit', '-m', 'edit some files'])
hgt.hg(['mv', 'z', 'dir'],
        stdout='''moving z/bigbig to dir/z/bigbig
moving z/bigbig.dat to dir/z/bigbig.dat
''')
hgt.hg(['commit', '-m', 'move files'])
hgt.hg(['rm', 'dir/b'],
        stdout='''removing dir/b/c/foo
removing dir/b/c/foo.dat
removing dir/b/medium
removing dir/b/medium.dat
''')
hgt.hg(['commit', '-m', 'remove some files'])
hgt.hg(['log'],
        stdout='''changeset:   4:c6ddff0dd76c
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove some files

changeset:   3:9769c20e1daa
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move files

changeset:   2:a73f17a91216
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit some files

changeset:   1:73960f5ccfe2
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:d82117283c29
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
os.chdir('..')

hgt.updaterc()
hgt.hg(['kbfconvert', '-s', '100', 'repo1', 'repo2'],
        stdout='initializing destination repo2\n')

os.chdir('repo2')
hgt.hg(['log'], stdout='''changeset:   4:c6ddff0dd76c
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove some files

changeset:   3:9769c20e1daa
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move files

changeset:   2:a73f17a91216
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit some files

changeset:   1:73960f5ccfe2
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:d82117283c29
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['up'], stdout='8 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.assertfalse(os.path.exists('.kbf'), "bfile standins shouldn't exist")

os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 1, 2, 3, 4])

hgt.updaterc({'kilnbfiles': [('size', '2'), ('patterns', 'glob:**.dat')]})
hgt.hg(['kbfconvert', 'repo1', 'repo3'],
        stdout='initializing destination repo3\n')

os.chdir('repo3')
hgt.assertfalse(os.path.exists('.kbf'), 'nothing should exist yet')
hgt.hg(['log'], stdout='''changeset:   4:41232093a631
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove some files

changeset:   3:188a0c00241d
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move files

changeset:   2:925bcdcffc5e
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit some files

changeset:   1:01c6a9ec7e2a
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:629107d2b19c
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['up'],
        stdout='''8 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
6 big files updated, 0 removed
''')
hgt.asserttrue(os.path.exists('.kbf'), 'bfile standins should exist')
hgt.asserttrue(os.path.exists('.kbf/foo.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/big.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/big'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/a/small.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/z/bigbig.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/z/bigbig'), 'standin should exist')
hgt.assertfalse(os.path.exists('.kbf/foo'), "standin shouldn't exist")
hgt.assertfalse(os.path.exists('.kbf/dir/a/small'), "standin shouldn't exist")
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo3', [0, 1, 2, 3, 4])

hgt.hg(['kbfconvert', 'repo1', 'repo4', 'glob:**'],
        stdout='initializing destination repo4\n')

os.chdir('repo4')
hgt.hg(['log'], stdout='''changeset:   4:953a55e2a0ec
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove some files

changeset:   3:0a3a55055f88
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     move files

changeset:   2:8fab379a648e
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     edit some files

changeset:   1:10660481ee75
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:3325a02c4986
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['up'],
        stdout='''8 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
8 big files updated, 0 removed
''')
hgt.asserttrue(os.path.exists('.kbf'), 'bfile standins should exist')
hgt.asserttrue(os.path.exists('.kbf'), 'bfile standins should exist')
hgt.asserttrue(os.path.exists('.kbf/foo.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/big.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/big'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/a/small.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/z/bigbig.dat'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/z/bigbig'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/foo'), 'standin should exist')
hgt.asserttrue(os.path.exists('.kbf/dir/a/small'), 'standin should exist')
os.chdir('..')
common.checkrepos(hgt, 'repo1', 'repo4', [0, 1, 2, 3, 4])

hgt.hg(['kbfconvert', 'repo2', 'repo5', '--tonormal'], stdout='initializing destination repo5\n')
common.checkrepos(hgt, 'repo1', 'repo5', [0, 1, 2, 3, 4])
os.chdir('repo5')
hgt.hg(['up'], stdout='0 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.assertfalse(os.path.exists('.kbf'), 'there should not be any standins')
os.chdir('..')

hgt.hg(['kbfconvert', 'repo3', 'repo6', '--tonormal'], stdout='initializing destination repo6\n')
common.checkrepos(hgt, 'repo1', 'repo6', [0, 1, 2, 3, 4])
os.chdir('repo6')
hgt.hg(['up'], stdout='0 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.assertfalse(os.path.exists('.kbf'), 'there should not be any standins')
os.chdir('..')

hgt.hg(['kbfconvert', 'repo4', 'repo7', '--tonormal'], stdout='initializing destination repo7\n')
common.checkrepos(hgt, 'repo4', 'repo7', [0, 1, 2, 3, 4])
os.chdir('repo7')
hgt.hg(['up'], stdout='0 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.assertfalse(os.path.exists('.kbf'), 'there should not be any standins')
os.chdir('..')
