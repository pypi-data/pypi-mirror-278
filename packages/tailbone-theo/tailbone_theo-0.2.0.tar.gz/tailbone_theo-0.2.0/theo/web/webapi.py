# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
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
Theo web API app
"""

from tailbone import webapi as base


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    rattail_config = base.make_rattail_config(settings)
    pyramid_config = base.make_pyramid_config(settings)

    # bring in some Theo / Tailbone
    pyramid_config.include('theo.web.subscribers')
    pyramid_config.include('theo.web.api')

    return pyramid_config.make_wsgi_app()
