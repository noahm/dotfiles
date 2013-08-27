import json
import sys
import os
import time
import getpass
import urllib2
from urllib import urlencode

from custom import *

# Ensure that the home directory is set appropriately so that the kilnauth
# cookies will be found.  This is important because Mercurial 1.9 and later
# changes the home directory in the test script.
os.environ['HOME'] = os.path.expanduser('~' + getpass.getuser());

# Paths for the individual extensions
KBFILESPATH = KILNEXTPATH + '/bfiles/kbfiles'
KILNAUTHPATH = KILNEXTPATH + '/kilnauth.py'
GESTALTPATH = KILNEXTPATH + '/gestalt.py'
KILNPATHPATH = KILNEXTPATH + '/kilnpath.py'
BIGPUSHPATH = KILNEXTPATH + '/big-push.py'
KILNPATH = KILNEXTPATH + '/kiln.py'
CASEGUARDPATH = KILNEXTPATH + '/caseguard.py'

def api(url):
    return KILNURL + '/api/1.0/' + url

def slurp(url, params={}, post=False, raw=False):
    params = urlencode(params, doseq=True)
    handle = urllib2.urlopen(url, params) if post else urllib2.urlopen(url + '?' + params)
    content = handle.read()
    obj = content if raw else json.loads(content)
    handle.close()
    return obj

def gettoken():
     return slurp(api('Auth/Login'), dict(sUser=USER, sPassword=PASSWORD))

def createtest(hgt, token):
    projects = slurp(api('Project'), dict(token=token))

    found = False
    for project in projects:
        if project['sName'] == 'Test':
            ixProject = project['ixProject']
            for group in project['repoGroups']:
                if group['sName'] == 'Test':
                    ixRepoGroup = group['ixRepoGroup']
                    found = True

    if not found:
        return None

    repo = slurp(api('Repo/Create'), dict(sName='Test', sDescription='test', ixRepoGroup=ixRepoGroup, sDefaultPermission='write', token=token))
    ixRepo = repo['ixRepo']

    hgt.asserttrue(isinstance(ixRepo, int), 'Create failed %s' % (str(ixRepo)))

    time.sleep(1)
    while True:
        # work around a known bug in Kiln that returns non-JSON data for this
        # API route so that we don't have "ignorable tests" in bfiles
        try:
            if slurp(api('Repo/%d' % ixRepo), dict(token=token))['sStatus'] == 'good':
                break
        except ValueError:
            pass
        time.sleep(0.1)

    return (KILNURL + '/Repo/Test/Test/Test', ixRepo)

def createtestbranch(hgt, token, ixParent):
    projects = slurp(api('Project'), dict(token=token))

    found = False
    for project in projects:
        if project['sName'] == 'Test':
            ixProject = project['ixProject']
            for group in project['repoGroups']:
                if group['sName'] == 'Test':
                    ixRepoGroup = group['ixRepoGroup']
                    found = True

    if not found:
        return None

    time.sleep(1)
    while slurp(api('Repo/%d' % ixParent), dict(token=token))['sStatus'] != 'good':
        time.sleep(0.1)

    repo = slurp(api('Repo/Create'), dict(sName='TestBranch', sDescription='test branch', ixRepoGroup=ixRepoGroup, ixParent=ixParent, fCentral=False, sDefaultPermission='write', token=token))
    ixRepo = repo['ixRepo']

    hgt.asserttrue(isinstance(ixRepo, int), 'Create failed %s' % (str(ixRepo)))

    time.sleep(1)
    while slurp(api('Repo/%d' % ixRepo), dict(token=token))['sStatus'] != 'good':
        time.sleep(0.1)

    return (KILNURL + '/Repo/Test/Test/TestBranch', ixRepo)

def deletetest(hgt, token):
    projects = slurp(api('Project'), dict(token=token))

    found = False
    foundbranch = False
    for project in projects:
        if project['sName'] == 'Test':
            ixProject = project['ixProject']
            for group in project['repoGroups']:
                if group['sName'] == 'Test':
                    ixRepoGroup = group['ixRepoGroup']
                    for repo in group['repos']:
                        if repo['sName'] == 'Test':
                            ixRepo = repo['ixRepo']
                            found = True
                        if repo['sName'] == 'TestBranch':
                            ixBranch = repo['ixRepo']
                            foundbranch = True

    if foundbranch:
        slurp(api('Repo/%d/Delete' % ixBranch), dict(token=token), post=True)
        try:
            while True:
                slurp(api('Repo/%d' % ixBranch), dict(token=token))
                time.sleep(0.1)
        except urllib2.HTTPError:
            pass
        except ValueError:
            pass
    if found:
        slurp(api('Repo/%d/Delete' % ixRepo), dict(token=token), post=True)
        try:
            while True:
                slurp(api('Repo/%d' % ixRepo), dict(token=token))
                time.sleep(0.1)
        except urllib2.HTTPError:
            pass
        except ValueError:
            pass
