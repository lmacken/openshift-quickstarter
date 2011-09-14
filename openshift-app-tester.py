#!/usr/bin/env python
# OpenShift Quickstarter Test Suite
# Author: Luke Macken <lmacken@redhat.com>

import os
import shutil
import getpass
import unittest
import pexpect

login = None
password = None
domain = None
timeout = 600

class OpenShiftQuickstartTest(object):
    app = None
    title = None
    db = True
    index = '/'

    def setUp(self):
        self._create_app()
        self.html = self.get(self.index)

    def tearDown(self):
        self._destroy_app()

    def _create_app(self):
        cmd = ['./openshift-quickstarter', login, domain, self.app, self.app]
        child = pexpect.spawn(' '.join(cmd), timeout=timeout)
        child.expect('Password:')
        child.sendline(password)
        if self.db:
            child.expect('Password:')
            child.sendline(password)
        child.expect(pexpect.EOF)

    def _destroy_app(self):
        if os.path.isdir(self.app):
            shutil.rmtree(self.app)
        child = pexpect.spawn('rhc-ctl-app -l %s -c destroy -a %s' % (
                login, self.app), timeout=timeout)
        child.expect('Password:')
        child.sendline(password)
        child.expect('Do you want to destroy this application \(y\/n\):')
        child.sendline('y')
        child.expect(pexpect.EOF)

    def get(self, path):
        return pexpect.run('curl http://%s-%s.rhcloud.com%s' % (
            self.app, domain, path))

    def test_index(self):
        assert self.title in self.html, self.html


class TestPyramid(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'pyramid'
    title = '<a href="1">test name</a>'

class TestTurboGears2(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'turbogears2'
    title = 'Welcome to TurboGears'

class TestDrupal(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'drupal'
    title = 'Welcome to OpenShift Drupal'

class TestRails(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'rails'
    title = 'Home#index'

class TestDjango(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'django'
    title = 'Yeah Django!'

class TestWordpress(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'wordpress'
    title = 'Welcome to the famous five minute WordPress installation process!'
    index = '/wp-admin/install.php'

class TestMediaWiki(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'mediawiki'
    title = 'MediaWiki has been successfully installed'
    index = '/index.php/Main_Page'

class TestPyBlosxom(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'pyblosxom'
    title = 'A PyBlosxom blog running in the Red Hat Cloud!'
    db = False


if __name__ == '__main__':
    if not login:
        login = raw_input('Login: ').strip()
    if not domain:
        domain = raw_input('Domain: ').strip()
    if not password:
        password = getpass.getpass('Password: ')

    unittest.main(verbosity=2)
