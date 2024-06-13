# Copyright 2014 xjmz, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provide base class for FOS service clients.
"""
from __future__ import absolute_import
import copy

import flymeyun_fos
from flymeyun_fos import fos_client_configuration
from flymeyun_fos.exception import FosClientError
from flymeyun_fos.auth import fos_signer
from flymeyun_fos.http import handler
from flymeyun_fos.http import fos_http_client


class FosBaseClient(object):
    """
    TODO: add docstring
    """
    def __init__(self, config, region_supported=True):
        """
        :param config: the client configuration. The constructor makes a copy of this parameter so
                        that it is safe to change the configuration after then.
        :type config: FosClientConfiguration

        :param region_supported: true if this client supports region.
        :type region_supported: bool
        """
        self.service_id = self._compute_service_id()
        self.region_supported = region_supported
        # just for debug
        self.config = copy.deepcopy(fos_client_configuration.DEFAULT_CONFIG)
        if config is not None:
            self.config.merge_non_none_values(config)
        if self.config.endpoint is None:
            self.config.endpoint = self._compute_endpoint()

    def _compute_service_id(self):
        return self.__module__.split('.')[2]

    def _compute_endpoint(self):
        if self.config.endpoint:
            return self.config.endpoint
        if self.region_supported:
            return b'%s://%s.%s.%s' % (
                self.config.protocol,
                self.service_id,
                self.config.region,
                flymeyun_fos.DEFAULT_SERVICE_DOMAIN)
        else:
            return b'%s://%s.%s' % (
                self.config.protocol,
                self.service_id,
                flymeyun_fos.DEFAULT_SERVICE_DOMAIN)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        return fos_http_client.send_request(
            self.config, fos_signer.sign, [handler.parse_error, handler.parse_json],
            http_method, path, body, headers, params)

    def _get_config(self, apiDict, apiName):
        return copy.deepcopy(apiDict[apiName])

    def _add_header(self, apiConfig, key, value):
        self._set_if_nonnull(apiConfig["headers"], key, value)

    def _add_query(self, apiConfig, key, value):
        # key-only query parameter's value is "" and can satisfy non-null
        self._set_if_nonnull(apiConfig["queries"], key, value)

    def _add_path_param(self, apiConfig, key, value):
        if value is None:
            raise FosClientError(b"Path param can't be none.")
        apiConfig["path"] = apiConfig["path"].replace("[" + key + "]", value)

    def _set_if_nonnull(self, params, param_name=None, value=None):
        if value is not None:
            params[param_name] = value
