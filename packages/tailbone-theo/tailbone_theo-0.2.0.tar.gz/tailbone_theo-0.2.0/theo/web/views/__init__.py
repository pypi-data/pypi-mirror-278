# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Views
"""

from tailbone.views import typical

from theo.config import integrate_catapult, integrate_corepos, integrate_locsms


def includeme(config):
    rattail_config = config.registry.settings.get('rattail_config')

    config.include('tailbone.views.essentials')
    config.include('tailbone.views.messages')
    config.include('tailbone.views.trainwreck.defaults')

    mods = {}

    if integrate_catapult(rattail_config):
        config.include('tailbone_onager.views')
        config.include('tailbone_onager.views.catapult')

    elif integrate_corepos(rattail_config):
        config.include('tailbone_corepos.views')
        config.include('tailbone_corepos.views.corepos')
        mods['tailbone.views.purchases'] = 'tailbone_corepos.views.purchases'

    elif integrate_locsms(rattail_config):
        config.include('tailbone_locsms.views')
        config.include('tailbone_locsms.views.locsms')

    typical.defaults(config, **mods)
