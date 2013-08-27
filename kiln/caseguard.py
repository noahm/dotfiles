# Portions copyright (C) 2011 Fog Creek Software.
# Portions copyright (C) 2010 Alexandru Totolici
# http://hackd.net/projects/caseguard/
#
# This Mercurial extension prevents users from adding:
# * filenames that differ only by case (i.e. 'FOO' and 'foo')
# * Windows-reserved filenames.
#
# Some filesystems cannot handle situations where files differ only by case.
# If such files are present (added from a filesystem that doesn't have this
# limitation) Mercurial will report a case-folding collision when the user
# tries to update. For more information, please see:
# http://mercurial.selenic.com/wiki/CaseFolding
#
# The operations that caseguard currently handles are 'add' and 'addremove'.
#
# To enable the "caseguard" extension globally, put these lines in your
# ~/.hgrc:
#  [extensions]
#  caseguard = /path/to/caseguard.py
#
# You may optionally add a section in the config file that specifies what
# options you want to have always enabled:
#
#   [caseguard]
#   override = true
#   nowincheck = true
#
# You cannot enable -U/--unguard in the config file since this effectively
# disables the extension.
#
# Please note that having override always enabled will revert all commands
# to their normal behaviour. However, if you pass --verbose you will get a
# listing of the files that would cause problems.
#
# NOTE: renaming file1 to FILE1 and running addremove will NOT change what the
# repository tracks. All changes must be committed before caseguard will
# allow files to be added (this means 'hg rm foo; hg add FOO' will fail).
#
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

'''guard against case-fold collisions and Windows name incompatibilities'''

import re
from mercurial import commands, extensions, cmdutil, util
from mercurial.i18n import _

try:
    from mercurial import scmutil
    disablecaseguard = hasattr(scmutil, 'checkportable')
except ImportError:
    disablecaseguard = False

casewarn = _('case-collision danger')
namewarn = _('Windows-incompatible filenames detected')

winbanpat = re.compile('((com[1-9](\..*)?)|(lpt[1-9](\..*)?)|(con(\..*)?)|'
    '(aux(\..*)?)|''(prn(\..*)?)|(nul(\..*)?)|(clock\$))\Z', re.IGNORECASE)
badchars = ':*?"<>|'

def _defaultloglevel(ui, abortonfail):
    if abortonfail:
        def doabort(msg):
            raise util.Abort(msg)
        return doabort
    else:
        def dowarn(msg):
            ui.warn(_('warning: %s\n') % msg)
        return dowarn

def _wincheck(ui, f, loglevel=None, abortonfail=False):
    if loglevel == None:
        loglevel = _defaultloglevel(ui, abortonfail)
    if winbanpat.match(f):
        loglevel(_('filename contains \'%s\', which is reserved on Windows: \'%s\'') % (f, f))

def _charcheck(ui, f, loglevel=None, abortonfail=False):
    if loglevel == None:
        loglevel = _defaultloglevel(ui, abortonfail)
    for c in f:
        if c in badchars:
            loglevel(_('filename contains \'%s\', which is reserved on Windows: \'%s\'') % (c, f))

def _casecollide(ui, repo, *pats, **opts):
    '''check the case of the given file against the repository. Return True
    on collisions and (optionally) print a list of problem-files.'''
    override = opts['override'] or ui.configbool('caseguard', 'override')
    nowinchk = opts['nowincheck'] or ui.configbool('caseguard', 'nowincheck')

    loglevel = _defaultloglevel(ui, not override)

    if len(set(s.lower() for s in pats)) != len(pats):
        colliding = True
        ui.note(_('file list contains a possible case-fold collision\n'))

    added = repo.status()[1] + repo.status()[3]
    exclst = [item[0] for item in repo['.'].manifest().iteritems()] + added
    chklst = [item.lower() for item in exclst]
    mtch = dict(zip(chklst, exclst))
    m = cmdutil.match(repo, pats, opts)

    for f in repo.walk(m):
        flwr = f.lower()
        _wincheck(ui, f, loglevel)
        _charcheck(ui, f, loglevel)
        if f not in repo.dirstate and f not in exclst and flwr in mtch:
            loglevel(_('possible case-folding collision for %s') % f)
        mtch[flwr] = f

def reallyadd(orig, ui, repo, *pats, **opts):
    '''wrap the add command so it enforces that filenames differ in
    more than just case
    '''
    if disablecaseguard:
        if opts['unguard']:
            ui.setconfig('ui', 'portablefilenames', 'ignore')
        elif opts['override']:
            ui.setconfig('ui', 'portablefilenames', 'warn')
        else:
            ui.setconfig('ui', 'portablefilenames', 'abort')
    if not opts['unguard'] and not disablecaseguard:
        _casecollide(ui, repo, *pats, **opts)
    return orig(ui, repo, *pats, **opts)

def casecheck(ui, repo, *pats, **opts):
    if not repo.local():
        ui.note(_('Only local repositories can be checked'))
        return
    '''check an existing local repository for filename issues (caseguard)'''
    try:
        # Mercurial >= 1.9
        m = scmutil.match(repo[0], pats, opts)
    except ImportError:
        # Mercurial <= 1.8
        m = cmdutil.match(repo, pats, opts)

    seen = dict()

    def dostatus(msg):
        ui.status('%s\n' % msg)

    for f in repo.walk(m):
        if f in repo.dirstate:
            badname = _wincheck(ui, f, dostatus) or \
                        _charcheck(ui, f, dostatus)
            if f.lower() in seen:
                dostatus(_('%s collides with %s') % (f, seen[f.lower()]))
            else:
                seen[f.lower()] = f
                if not badname:
                    ui.note(_('\t[OK] %s\n') % f)

wraplist = [extensions.wrapcommand(commands.table, 'add', reallyadd),
    extensions.wrapcommand(commands.table, 'addremove', reallyadd)]

# Mercurial 1.9 and later has case-checking built in when files are
# added, so only provide it in the extension for earlier versions.
for wrapcmd in wraplist:
    if disablecaseguard:
        wrapcmd[1].append(('o', 'override', False, _('ignored (present for compatibility'
        ' with Mercurial 1.8 and earlier)')))
        wrapcmd[1].append(('w', 'nowincheck', False, _('ignored (present for compatibility'
        ' with Mercurial 1.8 and earlier)')))
    else:
        wrapcmd[1].append(('o', 'override', False, _('add files regardless of'
        ' possible case-collision problems')))
        wrapcmd[1].append(('w', 'nowincheck', False, _('do not check'
        ' filenames for Windows incompatibilities')))
    wrapcmd[1].append(('U', 'unguard', False, _('completely skip checks'
    ' related to case-collision problems')))

cmdtable = {
    'casecheck': (casecheck, [], 'check the repository for filename issues')}
