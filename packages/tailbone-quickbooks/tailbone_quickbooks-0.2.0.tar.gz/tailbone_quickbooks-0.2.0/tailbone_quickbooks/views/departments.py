# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
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
Department views, w/ Quickbooks integration
"""

from tailbone.views import ViewSupplement


class DepartmentViewSupplement(ViewSupplement):
    """
    Department view supplement for Quickbooks integration
    """
    route_prefix = 'departments'

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.QuickbooksDepartment)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('quickbooks_expense_account', model.QuickbooksDepartment.quickbooks_expense_account)
        g.set_filter('quickbooks_expense_class', model.QuickbooksDepartment.quickbooks_expense_class)

    def configure_form(self, f):
        f.append('quickbooks_expense_account')
        f.append('quickbooks_expense_class')

    def get_version_child_classes(self):
        model = self.model
        return [model.QuickbooksDepartment]


def includeme(config):
    DepartmentViewSupplement.defaults(config)
