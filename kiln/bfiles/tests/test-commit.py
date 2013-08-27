#!/usr/bin/env python
#
# Test commit (lots of other tests commit all files so just try committing specific files)
#

import os
import common


hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('test')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
os.mkdir('dir')
os.mkdir('dir/dir')
hgt.writefile('n1', 'n1')
hgt.writefile('dir/n2', 'n2')
hgt.writefile('dir/dir/n3', 'n3')
hgt.writefile('b1', 'b1')
hgt.writefile('dir/b2', 'b2')
hgt.writefile('dir/dir/b3', 'b3')
hgt.hg(['add', 'n1', 'dir/n2', 'dir/dir/n3'])
hgt.hg(['add', '--bf', 'b1', 'dir/b2', 'dir/dir/b3'])
hgt.hg(['status'],
        stdout='''A b1
A dir/b2
A dir/dir/b3
A dir/dir/n3
A dir/n2
A n1
''')
hgt.hg(['commit', '-m', 'adding', '.kbf/b1'], status=255, stderr="abort: Don't commit bfile standin. Commit bfile.\n")
hgt.hg(['status'],
        stdout='''A b1
A dir/b2
A dir/dir/b3
A dir/dir/n3
A dir/n2
A n1
''')
hgt.hg(['commit', '-m', 'adding', 'n1', 'b1'])
hgt.hg(['status'],
        stdout='''A dir/b2
A dir/dir/b3
A dir/dir/n3
A dir/n2
''')
hgt.hg(['commit', '-m', 'adding', 'dir/dir/n3', 'dir/dir/b3'])
hgt.hg(['status'],
        stdout='''A dir/b2
A dir/n2
''')
hgt.hg(['commit', '-m', 'adding', 'dir/b2', 'dir/n2'])
hgt.hg(['status'])
hgt.writefile('b1', 'b11')
hgt.hg(['status'],
        stdout='M b1\n')
hgt.hg(['commit', '-m', 'modifying b1'])
hgt.asserttrue(hgt.readfile('b1') == 'b11', 'file contents dont match')
