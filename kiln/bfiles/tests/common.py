import sys
import os
import stat
import subprocess
import re

import hgtest
import kilntest

# assumes we're run by hg's run-tests.py
STOREDIR = os.path.join(os.getcwd(), 'store')

DEFAULTRC = {
    'extensions': [('kbfiles', kilntest.KBFILESPATH),
                   ('rebase', '')],
    'kilnbfiles': [('systemcache', os.path.join(os.getcwd(), 'bfilesstore')),],
    }

def getversion():
    hgname = 'hg'
    if os.name == 'nt':
        for path in os.environ['PATH'].split(';'):
            if os.path.exists(os.path.join(path, 'hg')):
                hgname = r'python %s\hg' % path
                break
    cmd = [hgname, 'version']
    child = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    stdout, stderr = child.communicate()
    versions = re.findall(r'\d+\.\d+(?:\.\d+)?', stdout)
    parts = [re.match(r'\d+', v).group(0) for v in versions[0].split('.')]

    version = [0, 0, 0]
    for i, part in enumerate(map(int, parts)):
        version[i] = part
    return tuple(version)

version = getversion()

class BfilesTester(hgtest.Tester):
    def updaterc(self, extraconfig=None):
        '''Append configuration settings to $HGRCPATH to configure bfiles
        for the current run, plus any additional settings in extraconfig.
        extraconfig, if supplied, must be a mapping from section name to
        list of (key, value) pairs -- the same structure as DEFAULTRC.'''
        config = DEFAULTRC.copy()
        if extraconfig:
            for (section, values) in extraconfig.iteritems():
                if section in config:
                    config[section] = list(config[section]) + values
                else:
                    config[section] = values

        output = []
        for section in sorted(config):
            entries = config[section]
            output.append('[%s]' % section)
            for entry in entries:
                assert len(entry) == 2, \
                    'a config entry must be an iterable with two items'
                output.append('%s = %s' % tuple(entry))
        self.writerc('\n'.join(output) + '\n')

    def walk(self, dir, prune=None, dirs=False):
        sep = os.path.sep
        dir = dir.replace('/', sep)
        result = []
        prefix = len(dir + sep)
        for (dirpath, dirnames, filenames) in os.walk(dir):
            dirpath = dirpath[prefix:]      # trim common leading dir name
            if dirs and dirpath != '':
                result.append(dirpath)
            if prune:
                dirnames[:] = [name for name in dirnames if name not in prune]
            dirnames.sort()
            filenames.sort()
            result.extend([os.path.join(dirpath, name) for name in filenames])

        return [fn.replace(sep, '/') for fn in result]

    def assertadmin(self, expect):
        actual = self.walk('.hg/bfiles', prune=['pending', 'committed'])
        self.assertequals(expect, actual, 'admin files')

    def assertpending(self, expect):
        actual = self.walk('.hg/bfiles/pending', dirs=True)
        self.assertequals(expect, actual, 'pending files/dirs')

    def assertcommitted(self, expect):
        actual = self.walk('.hg/bfiles/committed', dirs=True)
        self.assertequals(expect, actual, 'committed files/dirs')

    def assertstandins(self, expect):
        actual = self.walk('.hgbfiles')
        self.assertequals(expect, actual, 'standin files')

    def assertstore(self, expect):
        actual = self.walk(STOREDIR, dirs=True)
        self.assertequals(expect, actual, 'store contents')

    def assertdirstate(self, expect):
        actual = self.walk('.')
        def excluded(path):
            return path.startswith('./.hg/') or  path.startswith('./.hgbfiles')
        actual = [x for x in actual if not excluded(x)]
        self.assertequals(expect, actual, 'working files')

    def assertfile(self, file):
        self.asserttrue(os.path.isfile(file),
                        'file %s does not exist' % file)

    def assertfilegone(self, file):
        self.assertfalse(os.path.isfile(file) or os.path.exists(file),
                         'file %s exists (should be gone)' % file)

    def assertdirgone(self, dir):
        self.assertfalse(os.path.isdir(dir) or os.path.exists(dir),
                        'dir %s exists (should be gone)' % dir)

    def isexec(self, filename):
        return (os.stat(filename).st_mode & stat.S_IXUSR) != 0

    def assertexec(self, filename):
        if os.name != 'posix':
            return
        self.asserttrue(self.isexec(filename),
                        '%s is not executable' % filename)

    def assertnotexec(self, filename):
        self.assertfalse(self.isexec(filename),
                         '%s is executable' % filename)

    def asserthashes(self):
        '''assert that all big file hashes are consistent:
        - contents of .hgbfiles/x
        - contents of .hg/bfiles/latest/x
        - hash of x
        '''
        sep = os.path.sep
        latestdir = os.path.join('.hg', 'bfiles', 'latest')
        for bfile in self.walk('.hgbfiles'):
            fhash = sha1(bfile)

            shash = self.readfile(os.path.join('.hgbfiles', bfile))[0:40]
            lhash = self.readfile(os.path.join(latestdir, bfile))[0:40]

            assert shash, "nothing read from file %s" % standin
            assert lhash, "nothing read from file %s" % lfile

            self.asserttrue(
                shash == lhash == fhash,
                "%s: inconsistent hashes:\n"
                "  standin: %s\n"
                "  latest:  %s\n"
                "  file:    %s"
                % (bfile, shash, lhash, fhash))

    def createstore(self, name):
        store_tar = self.tjoin(name + '.tar')
        untar(store_tar)

    def sshstore(self):
        user = os.environ.get('LOGNAME', os.environ.get('USER'))
        return "ssh://%s@localhost/%s" % (user, STOREDIR)

# This deliberately does not use mercurial.util.sha1() -- don't want to
# depend on code that we might be testing.
try:
    import hashlib                      # Python >= 2.5
    _sha1 = hashlib.sha1
except ImportError:
    import sha                          # Python 2.4
    _sha1 = sha.new

def sha1(filename):
    '''Compute and return the SHA-1 hash of the specified file.'''
    # XXX assumes the file is small enough to read into memory
    digester = _sha1()
    f = open(filename)
    try:
        digester.update(f.read())
        return digester.hexdigest()
    finally:
        f.close()

def untar(filename, path='.'):
    '''Untar the specified tar file in path (current directory by
    default).'''
    import tarfile
    tf = tarfile.TarFile(filename)
    for info in tf:
        tf.extract(info, path)
    tf.close()

def checkdirs(patha, pathb):
    filesa = []
    for (dir, dirnames, filenames) in os.walk(patha):
        for f in filenames:
            filename = os.path.join(dir,f)[len(patha)+1:]
            if not filename.startswith('.hg') and not filename.startswith('.kbf'):
                filesa.append(filename)
    filesb = []
    for (dir, dirnames, filenames) in os.walk(pathb):
        for f in filenames:
            filename = os.path.join(dir,f)[len(pathb)+1:]
            if not filename.startswith('.hg') and not filename.startswith('.kbf'):
                filesb.append(filename)

    filesa.sort()
    filesb.sort()
    for (fa, fb) in zip(filesa, filesb):
        if fa != fb:
            return False
            sys.exit()
        fda = open(os.path.join(patha, fa), 'rb').read()
        fdb = open(os.path.join(pathb, fb), 'rb').read()
        if fda != fdb:
            return False
        if os.stat(os.path.join(patha, fa)).st_mode != os.stat(os.path.join(pathb, fb)).st_mode:
            return False
    return True

def checkrepos(hgt, repo1, repo2, revs):
    for i in revs:
        hgt.hg(['up', '-R', repo1, '-r', str(i), '-C'], stdout=hgt.ANYTHING, log=False)
        hgt.hg(['up', '-R', repo2, '-r', str(i), '-C'], stdout=hgt.ANYTHING, log=False)
        hgt.asserttrue(checkdirs(repo1, repo2), 'repos dont match at %d' % i)
    hgt.hg(['up', '-R', repo1, '-C'], stdout=hgt.ANYTHING, log=False)
    hgt.hg(['up', '-R', repo2, '-C'], stdout=hgt.ANYTHING, log=False)
