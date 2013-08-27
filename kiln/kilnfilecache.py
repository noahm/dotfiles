# Copyright (C) 2011, 2012 Fog Creek Software.  All rights reserved.
#
# This extension is used internally by Kiln Importer.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

'''fix a _filecache invalidation bug so hg convert works

See

  * http://our.fogbugz.com/f/cases/2338914/importer-does-not-work-with-hg-2-3-1 and
  * http://www.selenic.com/pipermail/mercurial-devel/2012-November/046159.html

  for more details.  Until Mercurial fixes this bug or accepts my patch,
this bug affects any tags in this revset:

  *  hg log -r 'descendants(9f94358) and tag()' --template '{tags}\n'

As of writing, that's every 2.3 release and 2.4-rc and 2.4.
'''

from mercurial import util

def reposetup(ui, repo):
    if util.version()[:3] < '2.3':
        # This bug was first introduced in 9f94358f9f93, which
        # occurred between 2.3-rc and 2.3.
        return

    from mercurial import localrepo
    if not issubclass(repo.__class__, localrepo.localrepository):
        return

    class kilnfilecacherepo(repo.__class__):
        def destroyed(self, *args, **kwargs):
            # By saving _filecache before it's cleared, we can
            # restore it and then call invalidate() afterward so
            # localrepo can delattr() the relevant attributes off
            # the repo object.  See my mercurial-devel patch for
            # more details.
            oldfilecache = dict(self._filecache)
            super(kilnfilecacherepo, self).destroyed(*args, **kwargs)
            self._filecache = oldfilecache
            self.invalidate()

    repo.__class__ = kilnfilecacherepo
