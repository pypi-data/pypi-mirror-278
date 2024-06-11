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
MailChimp list views
"""

from rattail_mailchimp.db.model import MailChimpList, MailChimpListMember

from tailbone.views import MasterView


class MailChimpListView(MasterView):
    """
    MailChimp List views
    """
    model_class = MailChimpList
    url_prefix = '/mailchimp/lists'
    route_prefix = 'mailchimp.lists'
    creatable = False
    editable = False
    deletable = False
    has_rows = True
    model_row_class = MailChimpListMember

    labels = {
        'id': "ID",
    }

    grid_columns = [
        'id',
        'name',
        'date_created',
    ]

    form_fields = [
        'id',
        'name',
        'date_created',
    ]

    row_labels = {
        'contact_id': "Contact ID",
        'id': "ID",
    }

    row_grid_columns = [
        'email_address',
        'full_name',
        'email_type',
        'status',
        'contact_id',
        'last_changed',
    ]

    row_form_fields = [
        'email_address',
        'full_name',
        'email_type',
        'status',
        'source',
        'unsubscribe_reason',
        'last_changed',
        'contact_id',
        'id',
    ]

    def configure_grid(self, g):
        super(MailChimpListView, self).configure_grid(g)

        g.set_sort_defaults('name')

        g.set_link('id')
        g.set_link('name')

    def get_row_data(self, mclist):
        model = self.model
        return self.Session.query(model.MailChimpListMember)\
                           .filter(model.MailChimpListMember.list == mclist)

    def get_parent(self, member):
        return member.list

    def configure_row_grid(self, g):
        super(MailChimpListView, self).configure_row_grid(g)

        g.set_sort_defaults('email_address')

        g.set_link('email_address')
        g.set_link('full_name')

    def row_grid_extra_class(self, member, i):
        if member.status == 'unsubscribed':
            return 'notice'

    def get_row_instance_title(self, member):
        return member.email_address


def includeme(config):
    MailChimpListView.defaults(config)
