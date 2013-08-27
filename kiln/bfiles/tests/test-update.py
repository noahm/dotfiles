#!/usr/bin/env python

# Test update/update -c/update -C

import os
import common

hgt = common.BfilesTester()

def rejoin(path):
    '''convert unix path to local convention'''
    return os.path.join(*path.split('/'))

def checkfiles(rev):
    strrev = str(rev)
    hgt.asserttrue(hgt.readfile('normal1') == 'n1' + strrev, 'files dont match')
    hgt.asserttrue(hgt.readfile('sub/normal2') == 'n2' + strrev, 'files dont match')
    hgt.asserttrue(hgt.readfile('sub/normal3.txt') == 'n3' + strrev, 'files dont match')
    hgt.asserttrue(hgt.readfile('big1') == 'b1' + strrev, 'files dont match')
    hgt.asserttrue(hgt.readfile('sub/big2') == 'b2' + strrev, 'files dont match')
    if rev == 2:
        hgt.assertfalse(os.path.exists('sub/normal4.txt'), 'removed file exists')
        hgt.assertfalse(os.path.exists('sub/big3.txt'), 'removed file exists')
    else:
        hgt.asserttrue(hgt.readfile('sub/big3.txt') == 'b3' + strrev, 'files dont match')
        hgt.asserttrue(hgt.readfile('sub/normal4.txt') == 'n4' + strrev, 'files dont match')

# add size and patterns for adding as bfiles
hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init', '-q'])
hgt.writefile('normal1', 'n10')
os.mkdir('sub')
hgt.writefile('sub/normal2', 'n20')
hgt.writefile('sub/normal3.txt', 'n30')
hgt.writefile('sub/normal4.txt', 'n40')
hgt.hg(['add', 'normal1', rejoin('sub/normal2'), rejoin('sub/normal3.txt'), rejoin('sub/normal4.txt')])
hgt.writefile('big1', 'b10')
hgt.writefile('sub/big2', 'b20')
hgt.writefile('sub/big3.txt', 'b30')
hgt.hg(['add', '--bf', 'big1', rejoin('sub/big2'), rejoin('sub/big3.txt')])
hgt.hg(['commit', '-m', 'added bfiles'])
checkfiles(0)

hgt.writefile('normal1', 'n11')
hgt.writefile('sub/normal2', 'n21')
hgt.writefile('sub/normal3.txt', 'n31')
hgt.writefile('sub/normal4.txt', 'n41')
hgt.writefile('big1', 'b11')
hgt.writefile('sub/big2', 'b21')
hgt.writefile('sub/big3.txt', 'b31')
hgt.hg(['commit', '-m', 'edit 1'])
checkfiles(1)

hgt.writefile('normal1', 'n12')
hgt.writefile('sub/normal2', 'n22')
hgt.writefile('sub/normal3.txt', 'n32')
hgt.writefile('big1', 'b12')
hgt.writefile('sub/big2', 'b22')
hgt.hg(['remove', 'sub/big3.txt', 'sub/normal4.txt'])
hgt.hg(['commit', '-m', 'edit 2 and remove'])
checkfiles(2)

hgt.writefile('normal1', 'n13')
hgt.writefile('sub/normal2', 'n23')
hgt.writefile('sub/normal3.txt', 'n33')
hgt.writefile('sub/normal4.txt', 'n43')
hgt.writefile('big1', 'b13')
hgt.writefile('sub/big2', 'b23')
hgt.writefile('sub/big3.txt', 'b33')
hgt.hg(['add', 'sub/normal4.txt'])
hgt.hg(['add', '--bf', 'sub/big3.txt'])
hgt.hg(['commit', '-m', 'edit 3 and add'])
checkfiles(3)

hgt.announce('update to revision 0 and back')
hgt.hg(['up', '-r', '0'],
        stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
checkfiles(0)
hgt.hg(['up'],
        stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))

hgt.announce('change files and update check')
hgt.writefile('big1', 'b14')
hgt.hg(['up', '--check', '-r', '1'],
            stderr='abort: uncommitted local changes\n', status=255)
hgt.hg(['up', '-C'],
        stdout=('0 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '1 big files updated, 0 removed\n'))
checkfiles(3)
hgt.writefile('normal1', 'n14')
hgt.hg(['up', '-c', '-r' ,'2'],
            stderr='abort: uncommitted local changes\n', status=255)
hgt.hg(['up', '-C'],
        stdout=('1 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '0 big files updated, 0 removed\n'))
checkfiles(3)
hgt.writefile('sub/big3.txt', 'tomissoooooooocool')
hgt.hg(['up', '--check', '-r', '0'],
            stderr='abort: uncommitted local changes\n', status=255)
hgt.hg(['up', '-C'],
        stdout=('0 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '1 big files updated, 0 removed\n'))
checkfiles(3)

hgt.announce('change files and update clean')
hgt.writefile('big1', 'b14')
hgt.hg(['up', '-C', '-r', '0'],
            stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
checkfiles(0)
hgt.hg(['up'],
            stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
checkfiles(3)
hgt.writefile('normal1', 'n14')
hgt.hg(['up', '-C', '-r' ,'1'],
            stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
checkfiles(1)
hgt.hg(['up'],
        stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
checkfiles(3)
hgt.writefile('sub/big3.txt', 'tomissoooooooocool')
hgt.hg(['up', '--clean', '-r', '2'],
            stdout=('5 files updated, 0 files merged, 2 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '2 big files updated, 1 removed\n'))
checkfiles(2)
hgt.hg(['up'],
        stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
checkfiles(3)

hgt.announce('change bfile and normal update')
hgt.writefile('sub/big2', 'WOW')
os.mkdir('dir')
os.chdir('dir')
hgt.hg(['up', '-y', '-r', '0'],
         stdout='''merging sub/big2
bfile sub/big2 has a merge conflict
keep (l)ocal or take (o)ther? l
6 files updated, 1 files merged, 0 files removed, 0 files unresolved
getting changed bfiles
2 big files updated, 0 removed
''')
os.chdir('..')
hgt.asserttrue(hgt.readfile('normal1') == 'n10', 'files dont match')
hgt.asserttrue(hgt.readfile('sub/normal2') == 'n20', 'files dont match')
hgt.asserttrue(hgt.readfile('sub/normal3.txt') == 'n30', 'files dont match')
hgt.asserttrue(hgt.readfile('sub/normal4.txt') == 'n40', 'files dont match')
hgt.asserttrue(hgt.readfile('big1') == 'b10', 'files dont match')
hgt.asserttrue(hgt.readfile('sub/big2') == 'WOW', 'files dont match')
hgt.asserttrue(hgt.readfile('sub/big3.txt') == 'b30', 'files dont match')
os.chdir('dir')
hgt.hg(['up', '--clean'],
         stdout=('7 files updated, 0 files merged, 0 files removed, 0 files unresolved\n'
                'getting changed bfiles\n'
                '3 big files updated, 0 removed\n'))
os.chdir('..')
checkfiles(3)
hgt.writefile('big1', 'b12')
hgt.writefile('normal1', 'n12')
os.chdir('dir')
hgt.hg(['up', '-y', '-r', '2'],
         stdout='''5 files updated, 0 files merged, 2 files removed, 0 files unresolved
getting changed bfiles
1 big files updated, 1 removed
''')
os.chdir('..')
checkfiles(2)
