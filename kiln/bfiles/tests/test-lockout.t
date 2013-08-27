Setup
  $ export KBFILES='--config extensions.kbfiles=/home/sp/.kilnext/bfiles/kbfiles'
  $ export KHG="hg $KBFILES"

Non-kbfiles clients not locked out from kbfiles servers on non-kbfiles repos
  $ mkdir r1
  $ cd r1
  $ hg init
  $ echo c1 > f1
  $ hg add f1
  $ hg com -m "m1"
  $ cd ..
  $ $KHG serve -R r1 -d -p 8001 --pid-file serve.pid
  $ hg clone http://localhost:8001 r2
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ kill $(cat serve.pid)

kbfiles clients still work with non-kbfiles servers
  $ hg serve -R r1 -d -p 8001 --pid-file serve.pid
  $ $KHG clone http://localhost:8001 r3
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ kill $(cat serve.pid)

Non-kbfiles clients locked out from kbfiles servers serving kbfiles repos
  $ mkdir r4
  $ cd r4
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add --bf f1
  $ $KHG com -m "m1"
  $ cd ..
  $ $KHG serve -R r4 -d -p 8001 --pid-file serve.pid
  $ hg clone http://localhost:8001 r5 2>/dev/null
  [1]
  $ kill $(cat serve.pid)

kbfiles clients refuse to push kbfiles repos to non-kbfiles servers
  $ mkdir r6
  $ cd r6
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add f1
  $ $KHG com -m "m1"
  $ cat >> .hg/hgrc <<!
  > [web]
  > push_ssl = false
  > allow_push = *
  > !
  $ cd ..
  $ $KHG clone r6 r7
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd r7
  $ echo c2 > f2
  $ $KHG add --bf f2
  $ $KHG com -m "m2"
  $ hg -R ../r6 serve -d -p 8001 --pid-file ../serve.pid
  $ $KHG push http://localhost:8001
  pushing to http://localhost:8001/
  searching for changes
  abort: remotestore: could not put $TESTTMP/r7/.hg/kilnbfiles/4cdac4d8b084d0b599525cf732437fb337d422a8 to remote store http://localhost:8001/
  [255]
  $ cd ..
  $ kill $(cat serve.pid)

