#!/usr/bin/env python

# Test that bfiles does not conflict with other extensions
# (e.g. bookmarks) that override localrepository.commit().

import os
import common

hgt = common.BfilesTester()

hgt.announce('setup')

# enable just bookmarks at first
hgt.updaterc(
    extraconfig={'extensions': [('bookmarks', '')]})

hgt.hg(['init', 'repo1'])
os.chdir('repo1')

hgt.writefile('a', 'a\n', 'wb')
hgt.hg(['commit', '-A', '-m', 'initial commit'],
       stdout='adding a\n')

# make the bookmark and show it
hgt.announce('create a bookmark')
hgt.hg(['bookmark', 'willmove'])
hgt.hg(['bookmarks'],
       stdout=' * willmove                  0:174a8b07abe3\n')

hgt.announce('move bookmark by committing')
hgt.writefile('a', 'a\n', 'ab')
hgt.hg(['commit', '-m', 'modify and move bookmark'])
hgt.hg(['bookmarks'],
       stdout=' * willmove                  1:7e0cee89986a\n')

hgt.announce('enable bfiles, make another commit, ensure bookmark moved')

# Repeat the entry for bookmarks to ensure that it is loaded after
# bfiles, since the bug we're testing for here only occurred when
# bfiles was loaded first.
hgt.updaterc(
    extraconfig={'extensions':
                 [('kbfiles', hgt.tjoin('..', 'kbfiles')),
                  ('bookmarks', '')]})

hgt.writefile('a', 'a\n', 'ab')
hgt.hg(['commit', '-m', 'modify with bfiles enabled'])
hgt.hg(['bookmarks'],
       stdout=' * willmove                  2:85d5cbe2ba98\n')



