# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_itbill import ITBill
from uw_itbill.models import Provision as ProvisionModel


class Provision(ITBill):

    _path_prefix = 'provision/'

    def get_provision_by_key_remote(self, key_remote):
        url = self.url("key_remote/{key_remote}")
        return self._fetch_provision(url)

    def get_provision_by_sys_id(self, sys_id):
        url = self.url("sys_id/{sys_id}")
        return self._fetch_provision(url)

    def _fetch_provision(self, url):
        json_data = self.get_resource(url)

        if isinstance(json_data, list):
            provisions = []
            for prov in json_data:
                provisions.append(
                    ProvisionModel(data=prov.get('provision')))

            return provisions

        return ProvisionModel(data=json_data.get('provision'))

    def put_provision_by_remote_key(self, key_remote, provision):
        url = self.url("key_remote/{key_remote}")

        json_data = self.put_resource(url, data)

        return ProvisionModel(data=json_data)
