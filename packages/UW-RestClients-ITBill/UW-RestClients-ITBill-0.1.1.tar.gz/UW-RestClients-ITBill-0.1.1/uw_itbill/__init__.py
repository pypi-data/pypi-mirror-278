# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.exceptions import DataFailureException
from uw_itbill.dao import ITBill_DAO
import json


class ITBill(object):
    """
    The ITBill object has methods for getting information
    about accounts, courses, enrollments and users within
    Canvas
    """

    _url_base = '/api/x_unowr_subscriptn/'
    _url_path_prefix = ''

    def url(self, path=""):
        return f"{self._url_base}{self._path_prefix}{path}"

    def get_resource(self, url):
        response = ITBill_DAO().getURL(url, {'Accept': 'application/json'})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def post_resource(self, url, body):
        response = ITBill_DAO().postURL(url, {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }, body)

        if response.status not in [200, 201]:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)
