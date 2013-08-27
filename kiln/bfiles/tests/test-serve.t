Setup
  $ export KBFILES='--config extensions.kbfiles=$TESTDIR/../kbfiles'
  $ export KHG="hg $KBFILES"

Clone tests setup
  $ mkdir r1
  $ cd r1
  $ $KHG init
  $ echo c1 > f1
  $ echo c2 > f2
  $ $KHG add --bf f1
  $ $KHG add f2
  $ $KHG com -m "m1"
  $ cd ..

Clone over http
  $ $KHG serve -R r1 -d -p 8001 --pid-file serve.pid
  $ $KHG --config kilnbfiles.systemcache=$PWD/cache1 clone http://localhost:8001 r2
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 2 changes to 2 files
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  getting changed bfiles
  1 big files updated, 0 removed
  $ ls $PWD/cache1 | diff r2/.kbf/f1 -
  $ kill $(cat serve.pid)

Clone over ssh
  $ $KHG --config kilnbfiles.systemcache=$PWD/cache2 clone -e "python $TESTDIR/dummyssh" --remotecmd "$KHG" ssh://user@dummy/r1 r3
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 2 changes to 2 files
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  getting changed bfiles
  1 big files updated, 0 removed

Pull tests setup
  $ mkdir r4
  $ cd r4
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add f1
  $ $KHG com -m "m1"
  $ echo c2 > f2
  $ $KHG add --bf f2
  $ $KHG com -m "m2"
  $ cd ..

Pull over http
  $ $KHG serve -R r4 -d -p 8001 --pid-file serve.pid
  $ $KHG clone http://localhost:8001 -r 0 r5
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd r5
  $ $KHG pull
  pulling from http://localhost:8001/
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ $KHG --config kilnbfiles.systemcache=$PWD/../cache3 up
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  getting changed bfiles
  1 big files updated, 0 removed
  $ ls $PWD/../cache3 | diff .kbf/f2 -
  $ cd ..
  $ kill $(cat serve.pid)

Pull over ssh
  $ $KHG clone -e "python $TESTDIR/dummyssh" --remotecmd "$KHG" ssh://user@dummy/r4 -r 0 r6
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd r6
  $ cat >> .hg/hgrc <<!
  > [ui]
  > remotecmd=$KHG
  > ssh=python $TESTDIR/dummyssh
  > !
  $ $KHG pull
  pulling from ssh://user@dummy/r4
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ $KHG --config kilnbfiles.systemcache=$PWD/../cache4 up
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  getting changed bfiles
  1 big files updated, 0 removed
  $ ls $PWD/../cache4 | diff .kbf/f2 -
  $ cd ..

Push tests setup
  $ mkdir r7
  $ cd r7
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add f1
  $ $KHG com -m "m1"
  $ cd ..

Push over http
  $ cat >> r7/.hg/hgrc <<!
  > [web]
  > allow_push = *
  > push_ssl = false
  > !
  $ $KHG --config kilnbfiles.systemcache=$PWD/cache5 serve -R r7 -d -p 8001 --pid-file serve.pid
  $ $KHG clone http://localhost:8001 r8
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd r8
  $ echo c2 > f2
  $ $KHG add --bf f2
  $ $KHG com -m "m2"
  $ $KHG push
  pushing to http://localhost:8001/
  searching for changes
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  $ ls $PWD/../cache5 | diff .kbf/f2 -
  $ cd ..
  $ kill $(cat serve.pid)

Push over ssh
  $ $KHG clone -e "python $TESTDIR/dummyssh" --remotecmd "$KHG" ssh://user@dummy/r7 r9
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 2 files
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  getting changed bfiles
  1 big files updated, 0 removed
  $ cd r9
  $ cat >> .hg/hgrc <<!
  > [ui]
  > remotecmd=$KHG --config kilnbfiles.systemcache=$PWD/../cache6
  > ssh=python $TESTDIR/dummyssh
  > !
  $ echo c3 > f3
  $ $KHG add --bf f3
  $ $KHG com -m "m3"
  $ $KHG push
  pushing to ssh://user@dummy/r7
  searching for changes
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  $ ls $PWD/../cache6 | diff .kbf/f3 -
  $ cd ..
