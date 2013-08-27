#!/usr/bin/env python
#
# Test hg gestalt extension

import os
import common

import hgtest
import kilntest

hgt = common.BfilesTester()

hgt.updaterc({'extensions': [('kilnauth', kilntest.KILNAUTHPATH),
                             ('gestalt', kilntest.GESTALTPATH)]})
hgt.announce('setup')
token = kilntest.gettoken()
kilntest.deletetest(hgt, token)
test = kilntest.createtest(hgt, token)
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['next'], stdout='''You need to create a Mercurial repository.

Run -> hg init
''')
hgt.hg(['init'])
hgt.hg(['next'], stdout='''You have not set a default repository in your configuration file.

Edit your configuration file, .hg/hgrc, and add a default entry in
the [paths] section.
''')
hgt.writefile('.hg/hgrc', '''[paths]
default = %s/Repo/Test/Test/Test
''' % kilntest.KILNURL)
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
Everything is up-to-date.  Write more code!
''' % kilntest.KILNURL)
hgt.writefile('n1', 'n1')
hgt.writefile('n2', 'n2')
hgt.hg(['add', 'n1', 'n2'])
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | uncommitted changes
You have changes in your working copy that should be committed
before updating your local or remote repositories:

Run -> hg commit
''' % kilntest.KILNURL)
hgt.hg(['commit', '-m', 'add files'])
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   1      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
You have changes in your local repository that aren't in your
remote repository. If you want to share your changes, you should:

Run -> hg push
''' % kilntest.KILNURL)
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
Everything is up-to-date.  Write more code!
''' % kilntest.KILNURL)
os.chdir('..')
hgt.hg(['clone', kilntest.KILNURL + '/Repo/Test/Test/Test', 'repo2'], log=False,
        stdout='''requesting all changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
updating to branch default
2 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
os.chdir('repo2')
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
Everything is up-to-date.  Write more code!
''' % kilntest.KILNURL)
hgt.writefile('n3', 'n3')
hgt.writefile('n4', 'n4')
hgt.hg(['add', 'n3', 'n4'])
hgt.hg(['commit', '-m', 'add more files'])
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
os.chdir('../repo1')
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      1   >> | Repository | working copy up-to-date
There are changes in your remote repository that haven't been
included in your local repository. To get your copy up-to-date you should:

Run -> hg pull
''' % kilntest.KILNURL)
hgt.hg(['pull', '../repo2'], stdout='''pulling from ../repo2
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 2 changes to 2 files
(run 'hg update' to get a working copy)
''')
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
You are not at a head.  You probably want to update to tip
before making any changes:

Run -> hg up
''' % kilntest.KILNURL)
hgt.hg(['up'], stdout='''2 files updated, 0 files merged, 0 files removed, 0 files unresolved
''')
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
Everything is up-to-date.  Write more code!
''' % kilntest.KILNURL)
hgt.writefile('n5', 'n5')
hgt.hg(['add', 'n5'])
hgt.hg(['commit', '-m', 'add file to repo1'])
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed one changeset
''' % kilntest.KILNURL)
os.chdir('../repo2')
hgt.writefile('n6', 'n6')
hgt.hg(['add', 'n6'])
hgt.hg(['commit', '-m', 'add file to repo2'])
hgt.hg(['pull', '../repo1'], stdout='''pulling from ../repo1
searching for changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 1 changes to 1 files (+1 heads)
(run 'hg heads' to see heads, 'hg merge' to merge)
''')
hgt.hg(['next'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   1      |   Local    | merge required
| Repository |      0   >> | Repository | working copy up-to-date
You have two heads in your local repository. To resolve this,
you should merge:

Run -> hg merge
''' % kilntest.KILNURL)
hgt.hg(['merge'], stdout='''1 files updated, 0 files merged, 0 files removed, 0 files unresolved
(branch merge, don't forget to commit)
''')
hgt.hg(['commit', '-m', 'merge'])
hgt.hg(['push'], stdout='''pushing to %s/Repo/Test/Test/Test
searching for changes
searching for changes
remote: kiln: successfully pushed 2 changesets
''' % kilntest.KILNURL)
hgt.hg(['wtf'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
Everything is up-to-date.  Write more code!
''' % kilntest.KILNURL)
hgt.hg(['overview'], stdout='''parent repository: %s/Repo/Test/Test/Test
|   Remote   | <<   0      |   Local    | 
| Repository |      0   >> | Repository | working copy up-to-date
''' % kilntest.KILNURL)
hgt.hg(['advice'], stdout='''Everything is up-to-date.  Write more code!
''')
os.chdir('..')
