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
Configuration for Theo
"""

from rattail.config import ConfigExtension


class TheoConfig(ConfigExtension):
    """
    Rattail config extension for Theo
    """
    key = 'theo'

    def configure(self, config):

        # this is the "Theo" app
        config.setdefault('rattail', 'app_title', "Theo")
        config.setdefault('rattail', 'app_package', 'theo')

        # Theo comes with its own menu for web app
        config.setdefault('tailbone.menus', 'handler', 'theo.web.menus:TheoMenuHandler')

        # Trainwreck model is same regardless of POS
        config.setdefault('rattail.trainwreck', 'model', 'rattail.trainwreck.db.model.defaults')

        # do we integrate w/ CORE-POS?
        if integrate_corepos(config):
            config.setdefault('rattail', 'model', 'theo.db.model_corepos')
            config.setdefault('rattail', 'settings', 'theo.appsettings.theo')
            config.setdefault('rattail', 'products.handler', 'rattail_corepos.products:CoreProductsHandler')
            config.setdefault('rattail.batch', 'vendor_catalog.handler.spec', 'rattail_corepos.batch.vendorcatalog:VendorCatalogHandler')
            config.setdefault('rattail.importing', 'versions.handler', 'theo.importing.versions_corepos:FromTheoToTheoVersions')
            config.setdefault('rattail.problems', 'modules', 'rattail.problems.rattail rattail_corepos.problems.corepos')

        # do we integrate w/ Catapult?
        elif integrate_catapult(config):
            config.setdefault('rattail', 'model', 'theo.db.model_catapult')
            config.setdefault('rattail', 'settings', 'theo.appsettings.theo, theo.appsettings.catapult')
            config.setdefault('rattail.importing', 'versions.handler', 'theo.importing.versions_catapult:FromTheoToTheoVersions')

        # do we integrate w/ LOC SMS?
        elif integrate_locsms(config):
            config.setdefault('rattail', 'model', 'theo.db.model_locsms')
            config.setdefault('rattail', 'settings', 'theo.appsettings.theo')
            config.setdefault('rattail.importing', 'versions.handler', 'theo.importing.versions_locsms:FromTheoToTheoVersions')

        else: # no integration
            config.setdefault('rattail', 'settings', 'theo.appsettings.theo')


def integrate_catapult(config):
    return config.getbool('theo', 'integrate_catapult', default=False,
                          usedb=False)


def integrate_corepos(config):
    return config.getbool('theo', 'integrate_corepos', default=False,
                          usedb=False)


def integrate_locsms(config):
    return config.getbool('theo', 'integrate_locsms', default=False,
                          usedb=False)


def mirror_posdb(config):
    return config.getbool('theo', 'mirror_posdb', default=False,
                          usedb=False)
