#!/usr/bin/env python
#
# Test rollback

import os
import common

hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init', '-q'])
hgt.writefile('b1', 'b1')
hgt.hg(['add', '--bf', 'b1'])
hgt.hg(['commit', '-m', 'add bfile'])
hgt.hg(['rollback'],
        stdout='''repository tip rolled back to revision -1 (undo commit)
working directory now based on revision -1
''')
hgt.hg(['status'], stdout='''A b1
''')
hgt.hg(['commit', '-m', 'add bfile'])
hgt.writefile('b2', 'b2')
hgt.hg(['add', '--bf', 'b2'])
hgt.hg(['commit', '-m', 'add another bfile'])
hgt.hg(['rollback'],
        stdout='''repository tip rolled back to revision 0 (undo commit)
working directory now based on revision 0
''')
hgt.hg(['status'], stdout='''A b2
''')
hgt.hg(['commit', '-m', 'add another bfile'])
hgt.writefile('b2', 'b22')
hgt.hg(['commit', '-m', 'modify bfile'])
hgt.hg(['rollback'],
       stdout='''repository tip rolled back to revision 1 (undo commit)
working directory now based on revision 1
''')
hgt.hg(['status'], stdout='''M b2
''')
hgt.asserttrue(hgt.readfile('b2') == 'b22', 'file changed')
hgt.hg(['commit', '-m', 'modify bfile'])
hgt.hg(['rm', 'b2'])
hgt.hg(['commit', '-m', 'delete bfile'])
hgt.hg(['rollback'],
       stdout='''repository tip rolled back to revision 2 (undo commit)
working directory now based on revision 2
''')
hgt.hg(['status'], stdout='''! b2
''')
hgt.asserttrue(hgt.readfile('.kbf/b2') == 'ad280552ca89b1d13baa498ef352e1eabaafdf28\n', 'file changed')
