# -*- coding: utf-8; -*-
################################################################################
#
#  pyCOREPOS -- Python Interface to CORE POS
#  Copyright © 2018-2024 Lance Edgar
#
#  This file is part of pyCOREPOS.
#
#  pyCOREPOS is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  pyCOREPOS is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  pyCOREPOS.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tasks for 'pyCOREPOS' package
"""

import os
import re
import shutil

from invoke import task


here = os.path.abspath(os.path.dirname(__file__))
__version__ = None
pattern = re.compile(r'^version = "(\d+\.\d+\.\d+)"$')
with open(os.path.join(here, 'pyproject.toml'), 'rt') as f:
    for line in f:
        line = line.rstrip('\n')
        match = pattern.match(line)
        if match:
            __version__ = match.group(1)
            break
if not __version__:
    raise RuntimeError("could not parse version!")


@task
def release(c):
    """
    Release a new version of 'pyCOREPOS'.
    """
    if os.path.exists('pyCOREPOS.egg-info'):
        shutil.rmtree('pyCOREPOS.egg-info')
    c.run('python -m build --sdist')
    c.run('twine upload dist/pycorepos-{}.tar.gz'.format(__version__))
