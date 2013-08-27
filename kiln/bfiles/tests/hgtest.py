"""
Experimental testing framework for Mercurial and its extensions.
The goal is to allow tests to be Python scripts rather than shell
scripts.  They should be:
  * more portable
  * possibly faster
  * much easier to understand and modify
  * somewhat easier to write

"""

import sys
import os
import re
import atexit
import subprocess
import traceback

ANYTHING = re.compile(r'')

class Failure(Exception):
    pass

class Tester(object):
    """
    Default test framework.  Is fairly verbose: writes each announcement
    and each hg command to stdout.
    """

    ANYTHING = ANYTHING

    def __init__(self):
        self.stdout = sys.stdout
        self.failures = []
        atexit.register(self._atexit)
        self.firstannounce = True

    def _atexit(self):
        if self.failures:
            sys.stderr.write('%d failures\n' % len(self.failures))
            sys.exit(1)

    def announce(self, msg):
        if self.firstannounce:
            msg = '% ' + msg + '\n'
            self.firstannounce = False
        else:
            msg = '\n% ' + msg + '\n'
        self.stdout.write(msg)
        self.stdout.flush()

    def hg(self, args, stdout='', stderr='', status=0, log=True):
        """
        Run an hg command and check that it output the specified text to
        stdout and stderr and returned the specified status.  stdout and
        stderr may be strings for exact comparison or re pattern objects
        for a regex comparison.  The constant ANYTHING conveniently
        matches any output, for when you don't care.
        """

        # XXX should use exact path to hg
        # XXX set PYTHONPATH?

        hgname = 'hg'
        if os.name == 'nt':
            for path in os.environ['PATH'].split(';'):
                if os.path.exists(os.path.join(path, 'hg')):
                    hgname = r'python %s\hg' % path
                    break
        cmd = hgname.split(' ') + args
        if log:
            self._logcmd(['hg'] + args)
        child = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)

        actual_stdout, actual_stderr = child.communicate()
        actual_status = child.returncode
        if os.name == 'nt' and actual_status < 0:
            # hack to match my Unix-centric expected status
            # (Mercurial actually exits with status -1, and the signedness
            # is preserved in Windows but wrapped around to 255 on Unix)
            actual_status += 256

        self.assertoutput(stdout, actual_stdout, 'stdout', cmd)
        self.assertoutput(stderr, actual_stderr, 'stderr', cmd)
        if isinstance(status, list):
            self.asserttrue(actual_status in status, "Status doesn't match")
        else:
            self.assertequals(status, actual_status)
        #self._failearly()

    def tjoin(self, *path):
        '''Return the path to filename in $TESTDIR.'''
        return os.path.join(os.environ['TESTDIR'], *path)

    def writefile(self, filename, content, mode='w'):
        '''Write content to filename.  By default, clobber the file and
        write in text mode; override mode to append and/or write in
        binary mode.'''
        dirname = os.path.dirname(filename)
        if dirname != '' and not os.path.exists(dirname):
            os.makedirs(dirname)

        f = open(filename, mode)
        try:
            f.write(content)
        finally:
            f.close()

    def writerc(self, content):
        '''Append content to the file specified by HGRCPATH.'''
        self.writefile(os.environ['HGRCPATH'], content, mode='a')

    def readfile(self, filename, mode='r'):
        f = open(filename, mode)
        try:
            return f.read()
        finally:
            f.close()

    def assertfalse(self, test, msg):
        if test:
            self._fail(msg)

    def asserttrue(self, test, msg):
        if not test:
            self._fail(msg)

    def assertequals(self, expect, actual, prefix=''):
        if expect != actual:
            if prefix:
                prefix += ': '
            if isinstance(expect, list):
                msg = self._listfailure(expect, actual, prefix)
            else:
                msg = prefix + self._shortfailure(expect, actual)
            self._fail(msg)

    def assertoutput(self, expect, actual, label, cmd):
        '''Assert that the actual output (stdout or stderr) of cmd matches
        the expected output.'''
        filtered = self._filteroutput(actual)
        if self._stringmatch(expect, filtered):
            # silence is golden, so say nothing on success
            return

        msg = self._bannerbracket(
            '%s %s:' % ('expected', label),
            str(expect),
            '%s %s:' % ('actual (filtered)', label),
            str(filtered))
        self._fail(msg)

    # -- Internal methods ----------------------------------------------

    def _shortfailure(self, expect, actual):
        return 'expected %r, but got %r' % (expect, actual)

    def _listfailure(self, expect, actual, prefix):
        return self._bannerbracket(
            '%s%s:' % (prefix, 'expected'),
            '\n'.join(['  %r' % v for v in expect]) + '\n',
            '%s%s:' % (prefix, 'actual'),
            '\n'.join(['  %r' % v for v in actual]) + '\n')

    def _bannerbracket(self, label1, content1, label2, content2):
        banner1 = ('-- %s ' % label1).ljust(60, '-')
        banner2 = ('-- %s ' % label2).ljust(60, '-')
        return ('\n' +
                banner1 + '\n' +
                content1 +
                banner2 + '\n' +
                content2 +
                '-'*60)


    def _fail(self, msg):
        self.stdout.write('FAIL: %s\n' % msg)

        # print a stack trace up to the point where we entered this module
        sys.stdout.write('failure context:\n')
        stack = traceback.extract_stack()
        modfile = sys.modules[__name__].__file__
        modfile = re.sub(r'\.py[co]$', '.py', modfile)
        while stack[-1][0] == modfile:
            del stack[-1]
        for line in traceback.format_list(stack):
            sys.stdout.write(line)

        self.failures.append(msg)

    def _failearly(self):
        if self.failures:
            raise Failure()

    try:
        re_type = re._pattern_type      # Python 2.5 and up
    except AttributeError:
        re_type = type(re.compile(''))  # Python 2.4

    def _stringmatch(self, expect, actual):
        if isinstance(expect, self.re_type):
            return bool(expect.search(actual))
        else:
            return expect == actual

    unsafechars = re.compile(r'[^a-zA-Z0-9\-\_\+\.\/\=\:]')

    def _logcmd(self, cmd):
        vcmd = []
        sep = os.path.sep
        unix = (sep == '/')
        for arg in cmd:
            if not unix and sep in arg:
                arg = arg.replace(sep, '/')
            if self.unsafechars.search(arg):
                arg = '\'' + arg.replace('\'', '\\\'') + '\''
            for var in ('TESTDIR', 'HGTMP'):
                val = os.environ[var].replace(sep, '/')
                arg = arg.replace(val, '$' + var)
            vcmd.append(arg)
        self.stdout.write(' '.join(vcmd) + '\n')
        self.stdout.flush()

    def _filteroutput(self, output):
        '''Filter Mercurial output to match test expectations.
        - convert local path separator to Unix
        - replace occurences of TESTDIR and HGTMP with pseudo-variable
          expansion
        '''
        sep = os.path.sep
        unix = (sep == '/')
        if not unix and sep in output:
            output = output.replace(sep, '/')
        for var in ('TESTDIR', 'HGTMP'):
            val = os.environ[var].replace(sep, '/')
            output = output.replace(val, '$' + var)
        return output
