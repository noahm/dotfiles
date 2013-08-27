import compileall
import os
import zipfile

def compile_extensions():
    curdir = os.path.dirname(os.path.abspath(__file__))
    compileall.compile_dir(curdir, force=True)

def walk(dir_root):
    for dirpath, dirnames, filenames in os.walk(dir_root):
        dirnames_set = set(dirnames)
        if 'tests' in dirnames_set:
            dirnames.remove('tests')

        for filename in filenames:
            ignore, ext = os.path.splitext(filename)
            if filename == 'setup.py':
                continue
            if ext not in ('.py', '.pyc'):
                continue
            yield os.path.join(dirpath, filename)

def build_release():
    absdir = os.path.abspath(os.path.dirname(__file__))
    target = os.path.join(absdir, 'kiln_extensions.zip')

    print 'Creating ZIP archive...'
    f = None
    try:
        f = zipfile.ZipFile(target, 'w')
        for filename in walk(absdir):
            zip_filename = os.path.join(
                'kiln_extensions',
                os.path.relpath(filename, absdir))
            print '  %s' % zip_filename
            f.write(filename, zip_filename)
    finally:
        if f: f.close()
    print 'Success!'

if __name__ == '__main__':
    compile_extensions()
    build_release()
