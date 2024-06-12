# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015-2024 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from trellowarrior import NAME, VERSION

import sys

def version(args):
    sys.stdout.write('{} {}\n'.format(NAME, VERSION))
