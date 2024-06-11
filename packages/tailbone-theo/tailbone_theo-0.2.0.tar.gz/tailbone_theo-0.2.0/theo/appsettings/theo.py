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
Theo app settings
"""

# bring in some common settings from rattail
from rattail.settings import (
    Setting,

    # (General)
    rattail_single_store,

    # # DataSync
    # rattail_datasync_url,
)


##############################
# (General)
##############################

class theo_link_to_mobile(Setting):
    """
    If set, displays a link to Theo Mobile app, within main (desktop) app page
    footer.
    """
    group = "(General)"
    namespace = 'theo'
    name = 'link_to_mobile'
    data_type = bool
