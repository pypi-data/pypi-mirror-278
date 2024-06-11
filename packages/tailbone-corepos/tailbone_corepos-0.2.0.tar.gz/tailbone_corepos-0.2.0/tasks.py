# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tasks for tailbone-corepos
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
    Release a new version of 'tailbone-corepos'.
    """
    if os.path.exists('tailbone_corepos.egg-info'):
        shutil.rmtree('tailbone_corepos.egg-info')
    c.run('python -m build --sdist')
    filename = f'tailbone_corepos-{__version__}.tar.gz'
    c.run('twine upload dist/{}'.format(filename))
