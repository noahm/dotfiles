#!/usr/bin/env python
#
# Test basic kiln interaction

import os
import common


hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('test with bfiles')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('foo', 'blah')
hgt.hg(['add', '--bf', 'foo'])
hgt.hg(['addremove'], status=255, stderr='abort: addremove cannot be run on a repo with bfiles\n')
hgt.hg(['commit', '-m', 'added foo'])
hgt.hg(['addremove'], status=255, stderr='abort: addremove cannot be run on a repo with bfiles\n')

hgt.announce('test without bfiles')
hgt.updaterc({'extensions': [('kbfiles', '!')]})
os.chdir('..')
os.mkdir('repo2')
os.chdir('repo2')
hgt.hg(['init'])
hgt.writefile('foo', 'blah')
hgt.hg(['add', 'foo'])
hgt.hg(['addremove'])
hgt.hg(['commit', '-m', 'added foo'])
hgt.hg(['addremove'])
