#!/usr/bin/env python

# Test various tricky bfadd corner cases.

import os
import common

hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('normal1', 'foo')
os.mkdir('sub')
hgt.writefile('sub/normal2', 'bar')
hgt.writefile('big1', 'abc')
hgt.writefile('sub/big2', 'xyz')
hgt.hg(['add', 'normal1', 'sub/normal2'])
hgt.hg(['add', '--bf', 'big1', 'sub/big2'])
hgt.hg(['commit', '-m', 'add files'])

hgt.writefile('normal1', 'foo1')
hgt.writefile('sub/normal2', 'bar1')
hgt.writefile('big1', 'abc1')
hgt.writefile('sub/big2', 'xyz1')
hgt.hg(['commit', '-m', 'edit files'])

hgt.hg(['rm', 'normal1', 'big1'])
hgt.hg(['commit', '-m', 'remove files'])

hgt.hg(['mv', 'sub/normal2', 'normal1'])
hgt.hg(['mv', 'sub/big2', 'big1'])
hgt.hg(['commit', '-m', 'move files'])

hgt.hg(['cp', 'normal1', 'sub/normal2'])
hgt.hg(['cp', 'big1', 'sub/big2'])
hgt.hg(['commit', '-m', 'copy files'])

hgt.hg(['archive', '-r', '0', '../archive0'])
hgt.hg(['archive', '-r', '1', '../archive1'])
hgt.hg(['archive', '-r', '2', '../archive2'])
hgt.hg(['archive', '-r', '3', '../archive3'])
hgt.hg(['archive', '-r', '4', '../archive4'])

os.chdir('../archive0')
hgt.asserttrue(hgt.readfile('normal1') == 'foo', 'contents dont match')
hgt.asserttrue(hgt.readfile('sub/normal2') == 'bar', 'contents dont match')
hgt.asserttrue(hgt.readfile('big1') == 'abc', 'contents dont match')
hgt.asserttrue(hgt.readfile('sub/big2') == 'xyz', 'contents dont match')

os.chdir('../archive1')
hgt.asserttrue(hgt.readfile('normal1') == 'foo1', 'contents dont match')
hgt.asserttrue(hgt.readfile('sub/normal2') == 'bar1', 'contents dont match')
hgt.asserttrue(hgt.readfile('big1') == 'abc1', 'contents dont match')
hgt.asserttrue(hgt.readfile('sub/big2') == 'xyz1', 'contents dont match')

os.chdir('../archive2')
hgt.asserttrue(not os.path.exists('normal1'), 'file should not exist')
hgt.asserttrue(hgt.readfile('sub/normal2') == 'bar1', 'contents dont match')
hgt.asserttrue(not os.path.exists('big1'), 'file should not exist')
hgt.asserttrue(hgt.readfile('sub/big2') == 'xyz1', 'contents dont match')

os.chdir('../archive3')
hgt.asserttrue(not os.path.exists('sub/normal2'), 'file should not exist')
hgt.asserttrue(hgt.readfile('normal1') == 'bar1', 'contents dont match')
hgt.asserttrue(not os.path.exists('sub/big2'), 'file should not exist')
hgt.asserttrue(hgt.readfile('big1') == 'xyz1', 'contents dont match')

os.chdir('../archive4')
hgt.asserttrue(hgt.readfile('normal1') == 'bar1', 'contents dont match')
hgt.asserttrue(hgt.readfile('sub/normal2') == 'bar1', 'contents dont match')
hgt.asserttrue(hgt.readfile('big1') == 'xyz1', 'contents dont match')
hgt.asserttrue(hgt.readfile('sub/big2') == 'xyz1', 'contents dont match')
