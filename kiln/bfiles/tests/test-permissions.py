#!/usr/bin/env python

# Test various tricky bfadd corner cases.

import os
import common
import stat

hgt = common.BfilesTester()

windows = os.name == 'nt'

mask = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO

# add size and patterns for adding as bfiles
hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('n1', 'n1')
hgt.writefile('b1', 'b1')
os.mkdir('dir')
os.mkdir('dir/dir')
hgt.writefile('dir/n2', 'n2')
hgt.writefile('dir/b2', 'b2')
hgt.writefile('dir/dir/n3', 'n3')
hgt.writefile('dir/dir/b3', 'n3')
hgt.hg(['add', 'n1', 'dir/n2', 'dir/dir/n3'])
hgt.hg(['add', '--bf', 'b1', 'dir/b2', 'dir/dir/b3'])
os.chmod('n1', 0755)
os.chmod('dir/n2', 0644)
os.chmod('dir/dir/n3', 0755)
os.chmod('b1', 0755)
os.chmod('dir/b2', 0644)
os.chmod('dir/dir/b3', 0755)
hgt.hg(['commit', '-m', 'initial add'])
if windows:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/n2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/dir/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/dir/n3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/dir/b3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/dir/dir/b3').st_mode & mask == 0666, 'permissions dont match')
else:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/n2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/b2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/dir/b2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/dir/n3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('dir/dir/b3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/dir/dir/b3').st_mode & mask == 0755, 'permissions dont match')

hgt.hg(['mv', 'dir', 'foo'],
        stdout='''moving dir/dir/n3 to foo/dir/n3
moving dir/n2 to foo/n2
moving .kbf/dir/b2 to .kbf/foo/b2
moving .kbf/dir/dir/b3 to .kbf/foo/dir/b3
''')
hgt.hg(['commit', '-m' ,'move files'])
if windows:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/n2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/n3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/b3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/dir/b3').st_mode & mask == 0666, 'permissions dont match')
else:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/n2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/b2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/b2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/n3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/b3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/dir/b3').st_mode & mask == 0755, 'permissions dont match')

os.chmod('n1', 0644)
os.chmod('b1', 0644)
os.chmod('foo/n2', 0755)
os.chmod('foo/b2', 0755)

# Also change a file so on windows there are changes
hgt.writefile('foo/dir/n3', 'n33')
hgt.writefile('foo/dir/n3', 'b33')
hgt.hg(['commit', '-m', 'change permissions'])
if windows:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/n2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/n3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/b3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/dir/b3').st_mode & mask == 0666, 'permissions dont match')
else:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/n2').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/b2').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/b2').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/n3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/b3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/dir/b3').st_mode & mask == 0755, 'permissions dont match')

if windows:
    hgt.hg(['backout', '-r', '2'],
        stdout='''getting changed bfiles
0 big files updated, 0 removed
reverting foo/dir/n3
changeset 3:8abd5724a95c backs out changeset 2:df964af3433e
''')
else:
    hgt.hg(['backout', '-r', '2'],
        stdout='''getting changed bfiles
0 big files updated, 0 removed
reverting .kbf/b1
reverting .kbf/foo/b2
reverting foo/dir/n3
reverting foo/n2
reverting n1
changeset 3:879e115336d5 backs out changeset 2:257706c1f69f
''')
if windows:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/n2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/b2').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/n3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/b3').st_mode & mask == 0666, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/dir/b3').st_mode & mask == 0666, 'permissions dont match')
else:
    hgt.asserttrue(os.stat('n1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('b1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/b1').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/n2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/b2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/b2').st_mode & mask == 0644, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/n3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('foo/dir/b3').st_mode & mask == 0755, 'permissions dont match')
    hgt.asserttrue(os.stat('.kbf/foo/dir/b3').st_mode & mask == 0755, 'permissions dont match')

os.chdir('..')
hgt.hg(['clone', 'repo1', 'repo2'],
        stdout='''updating to branch default
6 files updated, 0 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
3 big files updated, 0 removed
''')
common.checkrepos(hgt, 'repo1', 'repo2', [0, 1, 2, 3])
