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
CORE Office - patch customer gaps
"""

import logging

from rattail.app import GenericHandler
from rattail_corepos.corepos.util import get_core_members


log = logging.getLogger(__name__)


class CustomerGapPatcher(GenericHandler):
    """
    POST to the CORE API as needed, to patch gaps for customerID
    """

    def run(self, dry_run=False, progress=None):
        corepos = self.app.get_corepos_handler()
        op = corepos.get_model_office_op()
        corepos_api = corepos.make_webapi()
        members = get_core_members(self.config, corepos_api, progress=progress)
        tally = self.app.make_object(updated=0)

        self.maxlen_phone = self.app.maxlen(op.Customer.phone)
        # nb. just in case the smallest one changes in future..
        other = self.app.maxlen(op.MemberInfo.phone)
        if other < self.maxlen_phone:
            self.maxlen_phone = other

        def inspect(member, i):
            for customer in member['customers']:
                customer_id = int(customer['customerID'])
                if not customer_id:
                    data = dict(member)
                    self.trim_phones(data)
                    cardno = data.pop('cardNo')
                    log.debug("%s call set_member() for card no %s: %s",
                              'should' if dry_run else 'will',
                              cardno, data)
                    if not dry_run:
                        corepos_api.set_member(cardno, **data)
                    tally.updated += 1
                    return

        action = "Finding"
        if not dry_run:
            action += " and fixing"
        self.app.progress_loop(inspect, members, progress,
                               message=f"{action} customerID gaps")

        sys.stdout.write("\n")
        if dry_run:
            sys.stdout.write("would have ")
        sys.stdout.write(f"updated {tally.updated} members\n")

    def trim_phones(self, data):
        # the `meminfo` table allows 30 chars for phone, but
        # `Customers` table only allows 20 chars.  so we must trim to
        # 20 chars or else the CORE API will silently fail to update
        # tables correctly when we POST to it
        for customer in data['customers']:
            for field in ['phone', 'altPhone']:
                value = customer[field]
                if len(value) > self.maxlen_phone:
                    log.warning("phone value for cardno %s is too long (%s chars) "
                                "and will be trimmed to %s chars: %s",
                                data['cardNo'],
                                len(value),
                                self.maxlen_phone,
                                value)
                    customer[field] = value[:self.maxlen_phone]
