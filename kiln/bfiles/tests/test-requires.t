Setup
  $ export KBFILES='--config extensions.kbfiles=/home/sp/.kilnext/bfiles/kbfiles'
  $ export KHG="hg $KBFILES"

Requirement not added to new repos
  $ mkdir r1
  $ cd r1
  $ $KHG init
  $ grep kbfiles .hg/requires
  [1]
  $ cd ..

Requirement added to repos with .kbf directories
  $ mkdir r2
  $ cd r2
  $ $KHG init
  $ mkdir .kbf
  $ echo "0000000000000000000000000000000000000000" > .kbf/f1
  $ hg add .kbf/f1
  $ hg com -m "m1"
  $ grep kbfiles .hg/requires
  [1]
  $ $KHG status
  ! f1
  $ grep kbfiles .hg/requires
  kbfiles
  $ cd ..

Requirement added when cloning kbfiles repos
  $ mkdir r3
  $ cd r3
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add --bf f1
  $ $KHG com -m "m1"
  $ cd ..
  $ $KHG clone r3 r3c
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  getting changed bfiles
  1 big files updated, 0 removed
  $ grep kbfiles r3c/.hg/requires
  kbfiles

Requirement added when committing a bfile
  $ mkdir r4
  $ cd r4
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add --bf f1
  $ $KHG com -m "m1"
  $ grep kbfiles .hg/requires
  kbfiles
  $ cd ..

Requirement added when pulling bfiles into a non-kbfiles repo
  $ mkdir r5
  $ cd r5
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add f1
  $ $KHG com -m "m1"
  $ cd ..
  $ $KHG clone r5 r6
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd r6
  $ grep kbfiles .hg/requires
  [1]
  $ echo c2 > f2
  $ $KHG add --bf f2
  $ $KHG com -m "m2"
  $ cd ../r5
  $ $KHG pull ../r6
  pulling from ../r6
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ grep kbfiles .hg/requires
  kbfiles
  $ cd ..

Requirement added when pushing bfiles into a non-kbfiles repo
  $ mkdir r7
  $ cd r7
  $ $KHG init
  $ echo c1 > f1
  $ $KHG add f1
  $ $KHG com -m "m1"
  $ cd ..
  $ $KHG clone r7 r8
  updating to branch default
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd r8
  $ echo c2 > f2
  $ $KHG add --bf f2
  $ $KHG com -m "m2"
  $ $KHG push ../r7
  pushing to ../r7
  searching for changes
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  $ cd ../r7
  $ grep kbfiles .hg/requires
  kbfiles
  $ cd ..

Requirement blocks non-kbfiles clients
  $ mkdir r9
  $ cd r9
  $ hg init
  $ echo kbfiles >> .hg/requires
  $ hg st
  abort: unknown repository format: requires features 'kbfiles' (upgrade Mercurial)!
  [255]
