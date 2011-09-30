#!/usr/bin/env python
# OpenShift Quickstarter Test Suite
#
# Copyright (C) 2011 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
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

class TestCakePHP(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'cakephp'
    title = 'CakePHP: the rapid development php framework'

class TestSeamBooking(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'seambooking'
    title = 'Created with Seam'
    db = False

class TestFrogCMS(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'frogcms'
    title = 'Powered by <a href="http://www.madebyfrog.com/" alt="Frog">'

class TestWolfCMS(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'wolfcms'
    title = '<a href="http://www.wolfcms.org/" title="Wolf CMS">Wolf CMS</a>'

class TestReviewBoard(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'reviewboard'
    title = 'Log In | Review Board'
    index = '/account/login/?next_page=/dashboard/'

class TestSQLBuddy(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'sqlbuddy'
    title = 'SQL Buddy'
    index = '/sqlbuddy/login.php'

class TestFlask(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'flask'
    title = 'Hello World!'

class TestDancer(OpenShiftQuickstartTest, unittest.TestCase):
    app = 'dancer'
    title = 'Welcome to OpenShift'


if __name__ == '__main__':
    if not login:
        login = raw_input('Login: ').strip()
    if not domain:
        domain = raw_input('Domain: ').strip()
    if not password:
        password = getpass.getpass('Password: ')

    unittest.main(verbosity=2)
