#!/usr/bin/env python
#
# Test hg log -v, etc.

import os
import common

hgt = common.BfilesTester()

hgt.updaterc()
hgt.announce('setup')
os.mkdir('repo1')
os.chdir('repo1')
hgt.hg(['init'])
hgt.writefile('n1', 'n1')
hgt.hg(['add', 'n1'])
hgt.hg(['commit', '-m', 'add file'])
hgt.writefile('b1', 'b1')
hgt.hg(['add', '--bf', 'b1'])
hgt.hg(['commit', '-m', 'add bfile'])
hgt.writefile('n1', 'n11')
hgt.hg(['commit', '-m', 'modify file'])
hgt.writefile('b1', 'b11')
hgt.hg(['commit', '-m', 'modify bfile'])
hgt.hg(['rm', 'n1'])
hgt.hg(['commit', '-m', 'remove file'])
hgt.hg(['rm', 'b1'])
hgt.hg(['commit', '-m', 'remove bfile'])
hgt.hg(['log', '-v'], stdout='''changeset:   5:91f26d170c01
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
files:       b1
description:
remove bfile


changeset:   4:1f704517a6d2
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
files:       n1
description:
remove file


changeset:   3:62dcfdef9d8f
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
files:       b1
description:
modify bfile


changeset:   2:890752364659
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
files:       n1
description:
modify file


changeset:   1:506e2e74bf85
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
files:       b1
description:
add bfile


changeset:   0:10e46e544c56
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
files:       n1
description:
add file


''')
hgt.hg(['log', '-p'], stdout='''changeset:   5:91f26d170c01
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove bfile

diff -r 1f704517a6d2 -r 91f26d170c01 b1
Binary file b1 has changed

changeset:   4:1f704517a6d2
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove file

diff -r 62dcfdef9d8f -r 1f704517a6d2 n1
--- a/n1	Thu Jan 01 00:00:00 1970 +0000
+++ /dev/null	Thu Jan 01 00:00:00 1970 +0000
@@ -1,1 +0,0 @@
-n11
\ No newline at end of file

changeset:   3:62dcfdef9d8f
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify bfile

diff -r 890752364659 -r 62dcfdef9d8f b1
Binary file b1 has changed

changeset:   2:890752364659
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify file

diff -r 506e2e74bf85 -r 890752364659 n1
--- a/n1	Thu Jan 01 00:00:00 1970 +0000
+++ b/n1	Thu Jan 01 00:00:00 1970 +0000
@@ -1,1 +1,1 @@
-n1
\ No newline at end of file
+n11
\ No newline at end of file

changeset:   1:506e2e74bf85
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add bfile

diff -r 10e46e544c56 -r 506e2e74bf85 b1
Binary file b1 has changed

changeset:   0:10e46e544c56
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add file

diff -r 000000000000 -r 10e46e544c56 n1
--- /dev/null	Thu Jan 01 00:00:00 1970 +0000
+++ b/n1	Thu Jan 01 00:00:00 1970 +0000
@@ -0,0 +1,1 @@
+n1
\ No newline at end of file

''')
hgt.hg(['log', '--stat'], stdout='''changeset:   5:91f26d170c01
tag:         tip
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove bfile

 b1 |    0 
 1 files changed, 0 insertions(+), 0 deletions(-)

changeset:   4:1f704517a6d2
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     remove file

 n1 |  1 -
 1 files changed, 0 insertions(+), 1 deletions(-)

changeset:   3:62dcfdef9d8f
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify bfile

 b1 |    0 
 1 files changed, 0 insertions(+), 0 deletions(-)

changeset:   2:890752364659
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     modify file

 n1 |  2 +-
 1 files changed, 1 insertions(+), 1 deletions(-)

changeset:   1:506e2e74bf85
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add bfile

 b1 |    0 
 1 files changed, 0 insertions(+), 0 deletions(-)

changeset:   0:10e46e544c56
user:        test
date:        Thu Jan 01 00:00:00 1970 +0000
summary:     add file

 n1 |  1 +
 1 files changed, 1 insertions(+), 0 deletions(-)

''')
