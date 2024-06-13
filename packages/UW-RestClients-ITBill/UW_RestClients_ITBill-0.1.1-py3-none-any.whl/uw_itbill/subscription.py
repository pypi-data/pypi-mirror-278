# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Copyright 2021 UW-IT, University of Washingtonp
# SPDX-License-Identifier: Apache-2.0

from uw_itbill import ITBill
from uw_itbill.models import Subscription as SubscriptionModel


class Subscription(ITBill):

    _path_prefix = 'subscription/'

    def get_subscription_by_worktag(self, worktag):
        url = self.url(f"worktag/{worktag}")
        return self._fetch_subscription(url)

    def get_subscription_by_key_remote(self, key_remote):
        url = self.url(f"key_remote/{key_remote}")
        return self._fetch_subscription(url)

    def get_subscription_by_sys_id(self, sys_id):
        url = self.url(f"sys_id/{sys_id}")
        return self._fetch_subscription(url)

    def _fetch_subscription(self, url):
        json_data = self.get_resource(url)

        if isinstance(json_data, list):
            subscriptions = []
            for sub in json_data:
                sub_json = sub.get('subscription')
                subscriptions.append(SubscriptionModel(data=sub_json))

            return subscriptions

        sub_json = json_data.get('subscription')
        return SubscriptionModel(data=sub_json)

    def get_subscriptions_by_worktags(self, worktags):
        url = self.url(f"worktags?worktags={','.join(worktags)}")

        subscriptions = []
        for sub in self.get_resource(url):
            json_data = SubscriptionModel(data=sub)
            subscriptions.append(json_data)

        return subscriptions

    def create_subscription(self, subscription):
        url = self.url().rstrip('/')

        json_data = self.post_resource(url, subscription)

        return SubscriptionModel(data=json_data)

    def update_subscription_by_key_remote(self, key_remote, subscription):
        url = self.url(f"key_remote/{key_remote}")

        json_data = self.put_resource(url, subscription)

        return SubscriptionModel(data=json_data)
