#!/usr/bin/env python
#
# Test caseguard extension

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('caseguard', kilntest.CASEGUARDPATH)]})
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('abc', 'abc')
hgt.hg(['add', 'abc'])
hgt.hg(['casecheck'])
hgt.writefile('ABC', 'ABC')
hgt.hg(['add', 'ABC'], status=255, stderr='''abort: possible case-folding collision for ABC
''')
hgt.hg(['add', 'ABC', '-o'], stderr='''warning: possible case-folding collision for ABC
''')
hgt.writefile('com1', 'com1')
hgt.hg(['add', 'com1'], status=255, stderr='''abort: filename contains 'com1', which is reserved on Windows: 'com1'
''')
hgt.hg(['add', 'com1', '-o'], stderr='''warning: filename contains 'com1', which is reserved on Windows: 'com1'
''')
hgt.writefile('a<b', 'a<b')
hgt.hg(['add', 'a<b'], status=255, stderr='''abort: filename contains '<', which is reserved on Windows: 'a<b'
''')
hgt.hg(['add', 'a<b', '-o'], stderr='''warning: filename contains '<', which is reserved on Windows: 'a<b'
''')
hgt.writefile('Abc', 'Abc')
hgt.writefile('abC', 'abC')
hgt.hg(['add', '-o', 'Abc', 'abC'], stderr='''warning: possible case-folding collision for Abc
warning: possible case-folding collision for abC
''')
hgt.writefile('ABc', 'ABc')
hgt.hg(['add', '-U', 'ABc'])
hgt.writefile('aBC', 'aBC')
hgt.hg(['add', '-o', 'aBC'], stderr='''warning: possible case-folding collision for aBC
''')
hgt.hg(['casecheck'], '''ABc collides with ABC
Abc collides with ABC
filename contains '<', which is reserved on Windows: 'a<b'
aBC collides with ABC
abC collides with ABC
abc collides with ABC
filename contains 'com1', which is reserved on Windows: 'com1'
''')
os.chdir('..')
