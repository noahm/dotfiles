#!/usr/bin/env python

# Test hg purge

import os
import common

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('purge', '')]})
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('b1', 'b1')
hgt.writefile('n1', 'n1')
hgt.writefile('n2', 'n2')
hgt.hg(['add', '--bf', 'b1'])
hgt.hg(['add', 'n1'])
hgt.hg(['commit', '-m', 'add some files'])
hgt.hg(['purge'])
hgt.asserttrue(os.path.exists('b1'), 'missing b1')
hgt.asserttrue(hgt.readfile('b1') == 'b1', 'wrong file contents')
hgt.writefile('b2', 'b2')
hgt.hg(['purge'])
hgt.assertfalse(os.path.exists('b2'), 'failed to purge b2')
hgt.writefile('b2', 'b2')
hgt.hg(['add', '--bf', 'b2'])
hgt.hg(['purge'])
hgt.asserttrue(os.path.exists('b2'), 'missing b2')
hgt.asserttrue(hgt.readfile('b2') == 'b2', 'wrong file contents')
hgt.hg(['commit', '-m', 'add another bfile'])
hgt.writefile('b2', 'b22')
hgt.hg(['purge'])
hgt.asserttrue(os.path.exists('b2'), 'missing b2')
hgt.asserttrue(hgt.readfile('b2') == 'b22', 'wrong file contents')
os.chdir('..')
