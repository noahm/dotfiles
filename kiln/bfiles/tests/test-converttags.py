#!/usr/bin/env python

# Test that kbfconvert handles tags properly

import os
import common

hgt = common.BfilesTester()
hgt.updaterc()
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
hgt.hg(['tag', '-r', '0', 'first'])
hgt.hg(['tag', '-r', '1', 'second'])
hgt.hg(['tag', '-r', '3', 'last'])
hgt.hg(['log', '-r', 'first'],
        stdout='''changeset:   0:d82117283c29
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['log', '-r', 'second'],
        stdout='''changeset:   1:73960f5ccfe2
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

''')
hgt.hg(['log', '-r', 'last'],
        stdout='''changeset:   3:e229b8d1bac1
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

''')
hgt.hg(['log'],
        stdout='''changeset:   4:c4495ce62a60
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag last for changeset e229b8d1bac1

changeset:   3:e229b8d1bac1
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

changeset:   2:d41643b333a9
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag first for changeset d82117283c29

changeset:   1:73960f5ccfe2
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:d82117283c29
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
os.chdir('..')
hgt.hg(['kbfconvert', 'repo1', 'repo2', '-s', '1'], stdout='initializing destination repo2\n')
os.chdir('repo2')
hgt.hg(['log', '-r', 'first'], stdout='''changeset:   0:494d68993338
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['log', '-r', 'second'],
        stdout='''changeset:   1:a633211558b8
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

''')
hgt.hg(['log', '-r', 'last'],
        stdout='''changeset:   3:3c50e5db9993
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

''')
hgt.hg(['log'], stdout='''changeset:   4:d6940222c000
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag last for changeset e229b8d1bac1

changeset:   3:3c50e5db9993
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

changeset:   2:4a283e03a784
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag first for changeset d82117283c29

changeset:   1:a633211558b8
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:494d68993338
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['up', '-r', '0'], stdout='''6 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
hgt.assertfalse(os.path.exists('.hgtags'), "hgtags doesn't match")
hgt.hg(['up', '-r', '1'], stdout='''6 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
4 big files updated, 0 removed
''')
hgt.assertfalse(os.path.exists('.hgtags'), "hgtags doesn't match")
hgt.hg(['up', '-r', '2'], stdout='''1 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('.hgtags') == '494d68993338ddb5b7fd854396a003be5ed72755 first\n', "hgtags doesn't match")
hgt.hg(['up', '-r', '3'], stdout='''1 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('.hgtags') == '494d68993338ddb5b7fd854396a003be5ed72755 first\na633211558b85df9a4e0c18c0777284421721158 second\n', "hgtags doesn't match")
hgt.hg(['up', '-r', '4'], stdout='''1 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
0 big files updated, 0 removed
''')
hgt.asserttrue(hgt.readfile('.hgtags') == '494d68993338ddb5b7fd854396a003be5ed72755 first\na633211558b85df9a4e0c18c0777284421721158 second\n3c50e5db999358097d2b8602f50b2acda3886bc9 last\n', "hgtags doesn't match")

os.chdir('..')
hgt.hg(['kbfconvert', 'repo2', 'repo3', '--tonormal'], stdout='initializing destination repo3\n')
os.chdir('repo3')
hgt.hg(['log', '-r', 'first'], stdout='''changeset:   0:d82117283c29
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['log', '-r', 'second'],
        stdout='''changeset:   1:73960f5ccfe2
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

''')
hgt.hg(['log', '-r', 'last'],
        stdout='''changeset:   3:e229b8d1bac1
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

''')
hgt.hg(['log'], stdout='''changeset:   4:c4495ce62a60
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag last for changeset e229b8d1bac1

changeset:   3:e229b8d1bac1
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

changeset:   2:d41643b333a9
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag first for changeset d82117283c29

changeset:   1:73960f5ccfe2
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:d82117283c29
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['up', '-r', '0'], stdout='6 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.assertfalse(os.path.exists('.hgtags'), "hgtags doesn't match")
hgt.hg(['up', '-r', '1'], stdout='6 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.assertfalse(os.path.exists('.hgtags'), "hgtags doesn't match")
hgt.hg(['up', '-r', '2'], stdout='1 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.asserttrue(hgt.readfile('.hgtags') == 'd82117283c29e97adb8ebbcc5ea8fb7613ad0864 first\n', "hgtags doesn't match")
hgt.hg(['up', '-r', '3'], stdout='1 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.asserttrue(hgt.readfile('.hgtags') == 'd82117283c29e97adb8ebbcc5ea8fb7613ad0864 first\n73960f5ccfe2ca2f74002e55d74f186678f53872 second\n', "hgtags doesn't match")
hgt.hg(['up', '-r', '4'], stdout='1 files updated, 0 files merged, 0 files removed, 0 files unresolved\n')
hgt.asserttrue(hgt.readfile('.hgtags') == 'd82117283c29e97adb8ebbcc5ea8fb7613ad0864 first\n73960f5ccfe2ca2f74002e55d74f186678f53872 second\ne229b8d1bac18cbd3eef20f9433c076fe45fa97d last\n', "hgtags doesn't match")
os.chdir('..')
hgt.hg(['tag', '-R', 'repo3', 'fromroot'])
hgt.hg(['log', '-R', 'repo3'], stdout='''changeset:   5:d9771069dce1
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag fromroot for changeset c4495ce62a60

changeset:   4:c4495ce62a60
tag:         fromroot
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag last for changeset e229b8d1bac1

changeset:   3:e229b8d1bac1
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

changeset:   2:d41643b333a9
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag first for changeset d82117283c29

changeset:   1:73960f5ccfe2
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:d82117283c29
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
hgt.hg(['tag', '-R', 'repo2', 'fromroot'])
hgt.hg(['log', '-R', 'repo2'], stdout='''changeset:   5:e861e23e4324
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag fromroot for changeset d6940222c000

changeset:   4:d6940222c000
tag:         fromroot
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag last for changeset e229b8d1bac1

changeset:   3:3c50e5db9993
tag:         last
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag second for changeset 73960f5ccfe2

changeset:   2:4a283e03a784
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     Added tag first for changeset d82117283c29

changeset:   1:a633211558b8
tag:         second
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add more files

changeset:   0:494d68993338
tag:         first
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     initial commit

''')
