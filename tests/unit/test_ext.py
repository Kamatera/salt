# -*- coding: utf-8 -*-
# Import Python libs
from __future__ import absolute_import, unicode_literals
import os
import sys
import logging
import subprocess
import tempfile


# Import Salt Testing libs
from tests.support.unit import TestCase, skipIf
from tests.support.runtests import RUNTIME_VARS
import tests.support.helpers

# Import Salt libs
import salt.modules.cmdmod
import salt.utils.platform
import salt.utils.files

log = logging.getLogger(__name__)


@skipIf(not salt.utils.path.which('bash'), 'Bash needed for this test')
class VendorTornadoTest(TestCase):
    '''
    Ensure we are not using any non vendor'ed tornado
    '''

    def test_import_override(self):
        tmp = tempfile.mkdtemp()
        test_source = tests.support.helpers.dedent('''
        from __future__ import absolute_import, print_function
        import salt
        import tornado
        print(tornado.__name__)
        ''')
        tornado_source = tests.support.helpers.dedent('''
        foo = 'bar'
        ''')
        with salt.utils.files.fopen(os.path.join(tmp, 'test.py'), 'w') as fp:
            fp.write(test_source)
        with salt.utils.files.fopen(os.path.join(tmp, 'tornado.py'), 'w') as fp:
            fp.write(tornado_source)
        # Preserve the virtual environment
        p = subprocess.Popen(
            [sys.executable, os.path.join(tmp, 'test.py')],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env={'PYTHONPATH': ':'.join(sys.path)}
        )
        p.wait()
        pout = p.stdout.read().strip()
        assert pout == 'salt.ext.tornado'

    def test_vendored_tornado_import(self):
        grep_call = salt.modules.cmdmod.run_stdout(
            cmd='bash -c \'grep -r "import tornado" ./salt/*\'',
            cwd=RUNTIME_VARS.CODE_DIR,
            ignore_retcode=True,
        ).split('\n')
        valid_lines = []
        for line in grep_call:
            if line == '':
                continue
            # Skip salt/ext/tornado/.. since there are a bunch of imports like
            # this in docstrings.
            if 'salt/ext/tornado/' in line:
                continue
            log.error("Test found bad line: %s", line)
            valid_lines.append(line)
        assert valid_lines == [], len(valid_lines)

    def test_vendored_tornado_import_from(self):
        grep_call = salt.modules.cmdmod.run_stdout(
            cmd='bash -c \'grep -r "from tornado" ./salt/*\'',
            cwd=RUNTIME_VARS.CODE_DIR,
            ignore_retcode=True,
        ).split('\n')
        valid_lines = []
        for line in grep_call:
            if line == '':
                continue
            log.error("Test found bad line: %s", line)
            valid_lines.append(line)
        assert valid_lines == [], len(valid_lines)
