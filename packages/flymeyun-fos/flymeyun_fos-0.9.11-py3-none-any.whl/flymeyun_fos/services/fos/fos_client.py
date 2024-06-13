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
This module provides a client class for FOS.
"""
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import io
import copy
import http.client
import os
import json
import logging
import shutil
import threading
import multiprocessing
from builtins import str
from builtins import bytes
from future.utils import iteritems

import flymeyun_fos
from flymeyun_fos import utils
from flymeyun_fos.auth import fos_signer
from flymeyun_fos.fos_base_client import FosBaseClient
from flymeyun_fos.exception import FosClientError
from flymeyun_fos.exception import FosServerError
from flymeyun_fos.exception import FosHttpClientError
from flymeyun_fos.http import fos_http_client
from flymeyun_fos.http import handler
from flymeyun_fos.http import http_content_types
from flymeyun_fos.http import http_headers
from flymeyun_fos.http import http_methods
from flymeyun_fos.services import fos
from flymeyun_fos.services.fos import fos_handler
from flymeyun_fos.utils import required
from flymeyun_fos import compat

_logger = logging.getLogger(__name__)

FETCH_MODE_SYNC = b"sync"
FETCH_MODE_ASYNC = b"async"
ENCRYPTION_ALGORITHM = "AES256"
HTTP_PROTOCOL_HEAD = b'http'


class UploadTaskHandle(object):
    """
    handle to control multi upload file with multi-thread
    """
    def __init__(self):
        self.cancel_flag = False
        self.cancel_lock = threading.Lock()

    def cancel(self):
        """
        cancel putting super object from file with multi-thread
        """
        self.cancel_lock.acquire()
        self.cancel_flag = True
        self.cancel_lock.release()

    def is_cancel(self):
        """
        get cancel flag
        """
        self.cancel_lock.acquire()
        result = self.cancel_flag
        self.cancel_lock.release()
        return result


class FosClient(FosBaseClient):
    """
    sdk client
    """
    def __init__(self, config=None):
        FosBaseClient.__init__(self, config)

    def list_buckets(self, config=None):
        """
        List buckets of user

        :param config: None
        :type config: FosClientConfiguration
        :returns: all buckets owned by the user.
        :rtype: flymeyun_fos.fos_response.FOSResponse
        """
        return self._send_request(http_methods.GET, config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_location(self, bucket_name, config=None):
        """
        Get the region which the bucket located in.

        :param bucket_name: the name of bucket
        :type bucket_name: string or unicode
        :param config: None
        :type config: FosClientConfiguration

        :return: region of the bucket
        :rtype: str
        """
        params = {b'location': b''}
        response = self._send_request(http_methods.GET, bucket_name, params=params, config=config)
        return response.location_constraint

    @required(bucket_name=(bytes, str))
    def create_bucket(self, bucket_name, config=None):
        """
        Create bucket with specific name

        :param bucket_name: the name of bucket
        :type bucket_name: string or unicode
        :param config: None
        :type config: FosClientConfiguration
        :returns:
        :rtype: flymeyun_fos.fos_response.FosResponse
        """
        return self._send_request(http_methods.PUT, bucket_name, config=config)

    @required(bucket_name=(bytes, str))
    def does_bucket_exist(self, bucket_name, config=None):
        """
        Check whether there is a bucket with specific name

        :param bucket_name: None
        :type bucket_name: str
        :return:True or False
        :rtype: bool
        """
        try:
            self._send_request(http_methods.HEAD, bucket_name, config=config)
            return True
        except FosHttpClientError as e:
            if isinstance(e.last_error, FosServerError):
                if e.last_error.status_code == http.client.FORBIDDEN:
                    return True
                if e.last_error.status_code == http.client.NOT_FOUND:
                    return False
            raise e

    @required(bucket_name=(bytes, str))
    def get_bucket_acl(self, bucket_name, config=None):
        """
        Get Access Control Level of bucket

        :type bucket: string
        :param bucket: None
        :return:
            **json text of acl**
        """
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  params={b'acl': b''},
                                  config=config)

    @staticmethod
    def _dump_acl_object(acl):
        result = {}
        for k, v in iteritems(acl.__dict__):
            if not k.startswith('_'):
                result[k] = v
        return result

    @required(bucket_name=(bytes, str), acl=(list, dict))
    def set_bucket_acl(self, bucket_name, acl, config=None):
        """
        Set Access Control Level of bucket

        :type bucket: string
        :param bucket: None

        :type grant_list: list of grant
        :param grant_list: None
        :return:
            **HttpResponse Class**
        """
        self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps({'accessControlList': acl},
                                           default=FosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str), canned_acl=bytes)
    def set_bucket_canned_acl(self, bucket_name, canned_acl, config=None):
        """

        :param bucket_name:
        :param canned_acl:
        :param config:
        :return:
        """
        self._send_request(http_methods.PUT,
                           bucket_name,
                           headers={http_headers.FOS_ACL: canned_acl},
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def delete_bucket(self, bucket_name, config=None):
        """
        Delete a Bucket(Must Delete all the Object in Bucket before)

        :type bucket: string
        :param bucket: None
        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE, bucket_name, config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def generate_pre_signed_url(self,
                                bucket_name,
                                key,
                                timestamp=0,
                                expiration_in_seconds=1800,
                                headers=None,
                                params=None,
                                headers_to_sign=None,
                                protocol=None,
                                config=None,
                                httpmethod=http_methods.GET):
        """
        Get an authorization url with expire time.
        specified  protocol in endpoint > protocal > default protocol in config.

        :type timestamp: int
        :param timestamp: None

        :type expiration_in_seconds: int
        :param expiration_in_seconds: None

        :type options: dict
        :param options: None

        :param is_official_domain: default use not official domain,example: bucket.fos.flymeyun.com

        :return:
            **URL string**
        """
        key = compat.convert_to_bytes(key)
        config = self._merge_config(config, bucket_name)
        headers = headers or {}
        params = params or {}

        # specified  protocol in endpoint > protocal > default protocol in config
        if protocol is not None:
            config.protocol = protocol
        endpoint_protocol, endpoint_host, endpoint_port = utils.parse_host_port(config.endpoint,
                                                                                config.protocol)

        full_host = endpoint_host
        if endpoint_port != endpoint_protocol.default_port:
            full_host += b':' + compat.convert_to_bytes(endpoint_port)
        headers[http_headers.HOST] = full_host

        path = self._get_path(config, bucket_name, key)
        if httpmethod != http_methods.GET and httpmethod != http_methods.HEAD:
            headers_to_sign = {b'host'}

        params[http_headers.AUTHORIZATION.lower()] = fos_signer.sign(config.credentials,
                                                                     httpmethod,
                                                                     path,
                                                                     headers,
                                                                     params,
                                                                     timestamp,
                                                                     expiration_in_seconds,
                                                                     headers_to_sign)
        
        return b"%s://%s%s?%s" % (compat.convert_to_bytes(endpoint_protocol.name),
                                  full_host,
                                  path,
                                  utils.get_canonical_querystring(params, False))

    @required(bucket_name=(bytes, str), rules=(list, dict))
    def put_bucket_lifecycle(self, 
                             bucket_name,
                             rules,
                             config=None):
        """
        Put Bucket Lifecycle
       
        :type bucket: string
        :param bucket: None

        :type rules: list
        :param rules: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.PUT, 
                                  bucket_name,
                                  params={b'lifecycle': b''},
                                  body=json.dumps({'rule': rules}),
                                  config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_lifecycle(self, bucket_name, config=None):
        """
        Get Bucket Lifecycle

        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  params={b'lifecycle': b''},
                                  config=config) 

    @required(bucket_name=(bytes, str))
    def delete_bucket_lifecycle(self, bucket_name, config=None):
        """
        Delete Bucket Lifecycle
        
        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  params={b'lifecycle': b''},
                                  config=config)

    @required(bucket_name=(bytes, str), cors_configuration=list)
    def put_bucket_cors(self,
                        bucket_name,
                        cors_configuration,
                        config=None):
        """
        Put Bucket Cors
        :type bucket: string
        :param bucket: None

        :type cors_configuration: list
        :param cors_configuration: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.PUT,
                                  bucket_name,
                                  params={b'cors': b''},
                                  body=json.dumps({'corsConfiguration': cors_configuration}),
                                  config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_cors(self, bucket_name, config=None):
        """
        Get Bucket Cors

        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  params={b'cors': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))
    def delete_bucket_cors(self, bucket_name, config=None):
        """
        Delete Bucket Cors

        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  params={b'cors': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))        
    def list_objects(self,
                     bucket_name,
                     max_keys=1000,
                     prefix=None,
                     marker=None,
                     delimiter=None,
                     config=None):
        """
        Get Object Information of bucket

        :type bucket: string
        :param bucket: None

        :type delimiter: string
        :param delimiter: None

        :type marker: string
        :param marker: None

        :type max_keys: int
        :param max_keys: value <= 1000

        :type prefix: string
        :param prefix: None

        :return:
            **_ListObjectsResponse Class**
        """
        params = {}
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        if prefix is not None:
            params[b'prefix'] = prefix
        if marker is not None:
            params[b'marker'] = marker
        if delimiter is not None:
            params[b'delimiter'] = delimiter

        return self._send_request(http_methods.GET, bucket_name, params=params, config=config)

    @required(bucket_name=(bytes, str))
    def list_all_objects(self, bucket_name, prefix=None, delimiter=None, config=None):
        """

        :param bucket_name:
        :param prefix:
        :param delimiter:
        :param config:
        :return:
        """
        marker = None
        while True:
            response = self.list_objects(
                bucket_name, marker=marker, prefix=prefix, delimiter=delimiter, config=config)
            for item in response.contents:
                yield item
            if response.is_truncated:
                marker = response.next_marker
            else:
                break

    @staticmethod
    def _get_range_header_dict(range):
        if range is None:
            return None
        if not isinstance(range, (list, tuple)):
            raise TypeError('range should be a list or a tuple')
        if len(range) != 2:
            raise ValueError('range should have length of 2')
        return {http_headers.RANGE: b'bytes=%d-%d' % tuple(range)}

    @staticmethod
    def _parse_fos_object(http_response, response):
        """Sets response.body to http_response and response.user_metadata to a dict consists of all http
        headers starts with 'x-fos-meta-'.

        :param http_response: the http_response object returned by HTTPConnection.getresponse()
        :type http_response: httplib.HTTPResponse

        :param response: general response object which will be returned to the caller
        :type response: flymeyun_fos.FosResponse

        :return: always true
        :rtype bool
        """
        user_metadata = {}
        headers_list = http_response.getheaders()
        if compat.PY3:
            temp_heads = []
            for k, v in headers_list:
                k = k.lower()
                temp_heads.append((k, v))
            headers_list = temp_heads

        prefix = compat.convert_to_string(http_headers.FOS_USER_METADATA_PREFIX)
        for k, v in headers_list:
            if k.startswith(prefix):
                k = k[len(prefix):]
                user_metadata[compat.convert_to_unicode(k)] = compat.convert_to_unicode(v)
        response.metadata.user_metadata = user_metadata
        response.data = http_response
        return True

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object(self, bucket_name, key, range=None, traffic_limit=None, config=None):
        """

        :param bucket_name:
        :param key:
        :param range:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        if not key or key.startswith(b"/"):
            raise FosClientError("Key can not be empty or start with '/' .")
        range_header = FosClient._get_range_header_dict(range)
        if traffic_limit is not None:
            if range_header is None:
                range_header = {}
            range_header[http_headers.FOS_TRAFFIC_LIMIT] = traffic_limit
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  key,
                                  headers=range_header,
                                  config=config,
                                  body_parser=FosClient._parse_fos_object)

    @staticmethod
    def _save_body_to_file(http_response, response, file_name, buf_size=16 * 1024, progress_callback=None):
        f = open(file_name, 'wb')
        try:
            # Added progress bar monitoring
            if progress_callback:
                file_size = int(response.metadata.content_length)
                stream = utils.make_progress_adapter(http_response, progress_callback, file_size)
            else:
                stream = http_response

            shutil.copyfileobj(stream, f, buf_size)
            http_response.close()
        finally:
            f.close()
        return True

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object_as_string(self, bucket_name, key, range=None, config=None):
        """

        :param bucket_name:
        :param key:
        :param range:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        response = self.get_object(bucket_name, key, range=range, config=config)
        s = response.data.read()
        response.data.close()
        return s

    @required(bucket_name=(bytes, str), key=(bytes, str), file_name=(bytes, str))
    def get_object_to_file(self,
                           bucket_name,
                           key,
                           file_name,
                           range=None,
                           config=None,
                           progress_callback=None,
                           traffic_limit=None):
        """
        Get Content of Object and Put Content to File

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type file_name: string
        :param file_name: None

        :type range: tuple
        :param range: (0,9) represent get object contents of 0-9 in bytes. 10 bytes date in total.
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        if not key or key.startswith(b"/"):
            raise FosClientError("Key can not be empty or start with '/' .")
        file_name = compat.convert_to_bytes(file_name)
        range_header = FosClient._get_range_header_dict(range)
        if traffic_limit is not None:
            if range_header is None:
                range_header = {}
            range_header[http_headers.FOS_TRAFFIC_LIMIT] = traffic_limit
        
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  key,
                                  headers=range_header,
                                  config=config,
                                  body_parser=lambda http_response, response: FosClient._save_body_to_file(http_response,
                                                                                                           response,
                                                                                                           file_name,
                                                                                                           self._get_config_parameter(config, 'recv_buf_size'),
                                                                                                           progress_callback=progress_callback))

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object_meta_data(self, bucket_name, key, config=None):
        """
        Get head of object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None
        :return:
            **_GetObjectMetaDataResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.HEAD, bucket_name, key, config=config)

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              data=object,
              content_length=compat.integer_types,
              content_md5=(bytes, str))
    def append_object(self,
                      bucket_name,
                      key, data,
                      content_md5,
                      content_length,
                      offset=None,
                      content_type=None,
                      user_metadata=None,
                      content_sha256=None,
                      storage_class=None,
                      user_headers=None,
                      progress_callback=None,
                      traffic_limit=None,
                      object_tagging=None,
                      config=None):
        """
        Put an appendable object to FOS or add content to an appendable object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type content_length: long
        :type offset: long
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        content_md5 = compat.convert_to_bytes(content_md5)
        headers = self._prepare_object_headers(content_length=content_length,
                                               content_md5=content_md5,
                                               content_type=content_type,
                                               content_sha256=content_sha256,
                                               user_metadata=user_metadata,
                                               storage_class=storage_class,
                                               user_headers=user_headers,
                                               traffic_limit=traffic_limit,
                                               object_tagging=object_tagging)

        if content_length > fos.MAX_APPEND_OBJECT_LENGTH:
            raise ValueError('Object length should be less than %d. Use multi-part upload instead.' % fos.MAX_APPEND_OBJECT_LENGTH)

        params = {b'append': b''}
        if offset is not None:
            params[b'offset'] = offset
        
        if progress_callback:
            data = utils.make_progress_adapter(data, progress_callback)

        return self._send_request(http_methods.POST,
                                  bucket_name,
                                  key,
                                  body=data,
                                  headers=headers,
                                  params=params,
                                  config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str), data=(bytes, str))
    def append_object_from_string(self,
                                  bucket_name,
                                  key,
                                  data,
                                  content_md5=None,
                                  offset=None,
                                  content_type=None,
                                  user_metadata=None,
                                  content_sha256=None,
                                  storage_class=None,
                                  user_headers=None,
                                  progress_callback=None,
                                  traffic_limit=None,
                                  config=None):
        """
        Create an appendable object and put content of string to the object
        or add content of string to an appendable object
        """
        key = compat.convert_to_bytes(key)
        if isinstance(data, str):
            data = data.encode(flymeyun_fos.DEFAULT_ENCODING)

        fp = None
        try:
            fp = io.BytesIO(data)
            if content_md5 is None:
                content_md5 = utils.get_md5_from_fp(fp,
                                                    buf_size=self._get_config_parameter(config, 'recv_buf_size'))

            return self.append_object(bucket_name=bucket_name,
                                      key=key,
                                      data=fp,
                                      content_md5=content_md5,
                                      content_length=len(data),
                                      offset=offset,
                                      content_type=content_type,
                                      user_metadata=user_metadata,
                                      content_sha256=content_sha256,
                                      storage_class=storage_class,
                                      user_headers=user_headers,
                                      progress_callback=progress_callback,
                                      traffic_limit=traffic_limit,
                                      config=config)
        finally:
            if fp is not None:
                fp.close()

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              data=object,
              content_length=compat.integer_types,
              content_md5=(bytes, str))
    def put_object(self,
                   bucket_name,
                   key,
                   data,
                   content_length,
                   content_md5,
                   content_type=None,
                   content_sha256=None,
                   user_metadata=None,
                   storage_class=None,
                   user_headers=None,
                   encryption=None,
                   customer_key=None,
                   customer_key_md5=None,
                   progress_callback=None,
                   traffic_limit=None,
                   object_tagging=None,
                   config=None):
        """
        Put object and put content of file to the object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type fp: FILE
        :param fp: None

        :type file_size: long
        :type offset: long
        :type content_length: long
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        content_md5 = compat.convert_to_bytes(content_md5)
        headers = self._prepare_object_headers(content_length=content_length,
                                               content_md5=content_md5,
                                               content_type=content_type,
                                               content_sha256=content_sha256,
                                               user_metadata=user_metadata,
                                               storage_class=storage_class,
                                               user_headers=user_headers,
                                               traffic_limit=traffic_limit,
                                               object_tagging=object_tagging,)

        self._get_config_parameter(config, 'recv_buf_size')

        if content_length > fos.MAX_PUT_OBJECT_LENGTH:
            raise ValueError('Object length should be less than %d. Use multi-part upload instead.' % fos.MAX_PUT_OBJECT_LENGTH)
        
        if progress_callback:
            data = utils.make_progress_adapter(data, progress_callback)

        return self._send_request(http_methods.PUT,
                                  bucket_name,
                                  key,
                                  body=data,
                                  headers=headers,
                                  config=config)

    @required(bucket=(bytes, str), key=(bytes, str), data=(bytes, str))
    def put_object_from_string(self,
                               bucket,
                               key,
                               data,
                               content_md5=None,
                               content_type=None,
                               content_sha256=None,
                               user_metadata=None,
                               storage_class=None,
                               user_headers=None,
                               encryption=None,
                               customer_key=None,
                               customer_key_md5=None,
                               progress_callback=None,
                               traffic_limit=None,
                               object_tagging=None,
                               config=None):
        """
        Create object and put content of string to the object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type input_content: string
        :param input_content: None

        :type options: dict
        :param options: None
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        if isinstance(data, str):
            data = data.encode(flymeyun_fos.DEFAULT_ENCODING)

        fp = None
        try:
            fp = io.BytesIO(data)
            if content_md5 is None:
                content_md5 = utils.get_md5_from_fp(fp,
                                                    buf_size=self._get_config_parameter(config, 'recv_buf_size'))
            return self.put_object(bucket,
                                   key,
                                   fp,
                                   content_length=len(data),
                                   content_md5=content_md5,
                                   content_type=content_type,
                                   content_sha256=content_sha256,
                                   user_metadata=user_metadata,
                                   storage_class=storage_class,
                                   user_headers=user_headers,
                                   encryption=encryption,
                                   customer_key=customer_key,
                                   customer_key_md5=customer_key_md5,
                                   progress_callback=progress_callback,
                                   traffic_limit=traffic_limit,
                                   object_tagging=object_tagging,
                                   config=config)
        finally:
            if fp is not None:
                fp.close()

    @required(bucket=(bytes, str), key=(bytes, str), file_name=(bytes, str))
    def put_object_from_file(self,
                             bucket,
                             key,
                             file_name,
                             content_length=None,
                             content_md5=None,
                             content_type=None,
                             content_sha256=None,
                             user_metadata=None,
                             storage_class=None,
                             user_headers=None,
                             encryption=None,
                             customer_key=None,
                             customer_key_md5=None,
                             progress_callback=None,
                             traffic_limit=None,
                             object_tagging=None,
                             config=None):
        """
        Put object and put content of file to the object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type file_name: string
        :param file_name: None

        :type options: dict
        :param options: None
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        fp = open(file_name, 'rb')
        try:
            if content_length is None:
                fp.seek(0, os.SEEK_END)
                content_length = fp.tell()
                fp.seek(0)
            if content_md5 is None:
                recv_buf_size = self._get_config_parameter(config, 'recv_buf_size')
                content_md5 = utils.get_md5_from_fp(fp, length=content_length, buf_size=recv_buf_size)
            if content_type is None:
                content_type = utils.guess_content_type_by_file_name(file_name)
            return self.put_object(bucket,
                                   key,
                                   fp,
                                   content_length=content_length,
                                   content_md5=content_md5,
                                   content_type=content_type,
                                   content_sha256=content_sha256,
                                   user_metadata=user_metadata,
                                   storage_class=storage_class,
                                   user_headers=user_headers,
                                   encryption=encryption,
                                   customer_key=customer_key,
                                   customer_key_md5=customer_key_md5,
                                   progress_callback=progress_callback,
                                   traffic_limit=traffic_limit,
                                   object_tagging=object_tagging,
                                   config=config)
        finally:
            fp.close()

    @required(source_bucket_name=(bytes, str),
              source_key=(bytes, str),
              target_bucket_name=(bytes, str),
              target_key=(bytes, str))
    def copy_object(self,
                    source_bucket_name,
                    source_key,
                    target_bucket_name,
                    target_key,
                    etag=None,
                    content_type=None,
                    user_metadata=None,
                    storage_class=None,
                    user_headers=None,
                    copy_object_user_headers=None,
                    traffic_limit=None,
                    object_tagging=None,
                    config=None):
        """
        Copy one object to another object

        :type source_bucket: string
        :param source_bucket: None

        :type source_key: string
        :param source_key: None

        :type target_bucket: string
        :param target_bucket: None

        :type target_key: string
        :param target_key: None
        :return:
            **HttpResponse Class**
        """
        source_key = compat.convert_to_bytes(source_key)
        target_key = compat.convert_to_bytes(target_key)
        headers = self._prepare_object_headers(content_type=content_type,
                                               user_metadata=user_metadata,
                                               storage_class=storage_class,
                                               user_headers=user_headers,
                                               traffic_limit=traffic_limit,
                                               object_tagging=object_tagging)
        headers[http_headers.FOS_COPY_SOURCE] = utils.normalize_string(b'/%s/%s' % (compat.convert_to_bytes(source_bucket_name),
                                                                                    source_key),
                                                                       False)
        if etag is not None:
            headers[http_headers.FOS_COPY_SOURCE_IF_MATCH] = etag
        if user_metadata is not None or content_type is not None:
            headers[http_headers.FOS_COPY_METADATA_DIRECTIVE] = b'replace'
        else:
            headers[http_headers.FOS_COPY_METADATA_DIRECTIVE] = b'copy'

        if copy_object_user_headers is not None:
            try:
                headers = FosClient._get_user_header(headers, copy_object_user_headers, True)
            except Exception as e:
                raise e

        return self._send_request(http_methods.PUT,
                                  target_bucket_name,
                                  target_key,
                                  headers=headers,
                                  config=config,
                                  body_parser=fos_handler.parse_copy_object_response)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def delete_object(self, bucket_name, key, config=None):
        """
        Delete Object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.DELETE, bucket_name, key, config=config)

    @required(bucket_name=(bytes, str), key_list=list)
    def delete_multiple_objects(self, bucket_name, key_list, config=None):
        """
        Delete Multiple Objects

        :type bucket: string
        :param bucket: None

        :type key_list: string list
        :param key_list: None
        :return:
            **HttpResponse Class**
        """
        key_list_json = [{'key': compat.convert_to_string(k)} for k in key_list]
        return self._send_request(http_methods.POST,
                                  bucket_name,
                                  body=json.dumps({'objects': key_list_json}),
                                  params={b'delete': b''},
                                  config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def initiate_multipart_upload(self,
                                  bucket_name,
                                  key,
                                  content_type=None,
                                  storage_class=None,
                                  user_headers=None,
                                  config=None):
        """
        Initialize multi_upload_file.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None
        :return:
            **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        headers = {}
        if storage_class is not None:
            headers[http_headers.FOS_STORAGE_CLASS] = storage_class

        if content_type is not None:
            headers[http_headers.CONTENT_TYPE] = utils.convert_to_standard_string(content_type)
        else:
            headers[http_headers.CONTENT_TYPE] = http_content_types.OCTET_STREAM

        if user_headers is not None:
            try:
                headers = FosClient._get_user_header(headers, user_headers, False)
            except Exception as e:
                raise e

        return self._send_request(http_methods.POST,
                                  bucket_name,
                                  key,
                                  headers=headers,
                                  params={b'uploads': b''},
                                  config=config)

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              upload_id=(bytes, str),
              part_number=int,
              part_size=compat.integer_types,
              part_fp=object)
    def upload_part(self,
                    bucket_name,
                    key,
                    upload_id,
                    part_number,
                    part_size,
                    part_fp,
                    part_md5=None,
                    progress_callback=None,
                    traffic_limit=None,
                    config=None):
        """
        Upload a part.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None

        :type part_number: int
        :param part_number: None

        :type part_size: int or long
        :param part_size: None

        :type part_fp: file pointer
        :param part_fp: not None

        :type part_md5: str
        :param part_md5: None

        :type config: dict
        :param config: None

        :return:
               **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        if part_number < fos.MIN_PART_NUMBER or part_number > fos.MAX_PART_NUMBER:
            raise ValueError('Invalid part_number %d. The valid range is from %d to %d.' % (part_number,
                                                                                            fos.MIN_PART_NUMBER,
                                                                                            fos.MAX_PART_NUMBER))

        if part_size > fos.MAX_PUT_OBJECT_LENGTH:
            raise ValueError('Single part length should be less than %d. ' % fos.MAX_PUT_OBJECT_LENGTH)

        headers = {http_headers.CONTENT_LENGTH: part_size,
                   http_headers.CONTENT_TYPE: http_content_types.OCTET_STREAM}
        if part_md5 is not None:
            headers[http_headers.CONTENT_MD5] = part_md5

        if progress_callback:
            part_fp = utils.make_progress_adapter(part_fp, progress_callback, part_size)
        
        if traffic_limit is not None:
            headers[http_headers.FOS_TRAFFIC_LIMIT] = traffic_limit
        return self._send_request(http_methods.PUT,
                                  bucket_name,
                                  key,
                                  body=part_fp,
                                  headers=headers,
                                  params={b'partNumber': part_number, b'uploadId': upload_id},
                                  config=config)

    @required(source_bucket_name=(bytes, str),
              source_key=(bytes, str),
              target_bucket_name=(bytes, str),
              target_key=(bytes, str),
              upload_id=(bytes, str),
              part_number=int,
              part_size=compat.integer_types,
              offset=compat.integer_types)
    def upload_part_copy(self,
                         source_bucket_name,
                         source_key,
                         target_bucket_name,
                         target_key,
                         upload_id,
                         part_number,
                         part_size,
                         offset,
                         etag=None,
                         content_type=None,
                         user_metadata=None,
                         traffic_limit=None,
                         config=None):
        """
        Copy part.

        :type source_bucket_name: string
        :param source_bucket_name: None

        :type source_key: string
        :param source_key: None

        :type target_bucket_name: string
        :param target_bucket_name: None

        :type target_key: string
        :param target_key: None

        :type upload_id: string
        :param upload_id: None

        :return:
            **HttpResponse**
        """
        source_key = compat.convert_to_bytes(source_key)
        target_key = compat.convert_to_bytes(target_key)
        headers = self._prepare_object_headers(content_type=content_type,
                                               user_metadata=user_metadata,
                                               traffic_limit=traffic_limit)
        headers[http_headers.FOS_COPY_SOURCE] = utils.normalize_string(b"/%s/%s" % (compat.convert_to_bytes(source_bucket_name),
                                                                                    source_key),
                                                                       False)
        range = b"""bytes=%d-%d""" % (offset, offset + part_size - 1)
        headers[http_headers.FOS_COPY_SOURCE_RANGE] = range
        if etag is not None:
            headers[http_headers.FOS_COPY_SOURCE_IF_MATCH] = etag

        return self._send_request(http_methods.PUT,
                                  target_bucket_name,
                                  target_key,
                                  headers=headers,
                                  params={b'partNumber': part_number, b'uploadId': upload_id},
                                  config=config)

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              upload_id=(bytes, str),
              part_number=int,
              part_size=compat.integer_types,
              file_name=(bytes, str),
              offset=compat.integer_types)
    def upload_part_from_file(self,
                              bucket_name,
                              key,
                              upload_id,
                              part_number,
                              part_size,
                              file_name,
                              offset,
                              part_md5=None,
                              progress_callback=None,
                              traffic_limit=None,
                              config=None):
        """

        :param bucket_name:
        :param key:
        :param upload_id:
        :param part_number:
        :param part_size:
        :param file_name:
        :param offset:
        :param part_md5:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        f = open(file_name, 'rb')
        try:
            f.seek(offset)
            return self.upload_part(bucket_name,
                                    key,
                                    upload_id,
                                    part_number,
                                    part_size,
                                    f,
                                    part_md5=part_md5,
                                    progress_callback=progress_callback,
                                    traffic_limit=traffic_limit,
                                    config=config)
        finally:
            f.close()

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              upload_id=(bytes, str),
              part_list=list)
    def complete_multipart_upload(self,
                                  bucket_name,
                                  key,
                                  upload_id,
                                  part_list,
                                  user_metadata=None,
                                  config=None):
        """
        After finish all the task, complete multi_upload_file.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None

        :type part_list: list
        :param part_list: None

        :return:
            **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        headers = self._prepare_object_headers(content_type=http_content_types.JSON,
                                               user_metadata=user_metadata)

        return self._send_request(http_methods.POST,
                                  bucket_name,
                                  key,
                                  body=json.dumps({'parts': part_list}),
                                  headers=headers,
                                  params={b'uploadId': upload_id})

    @required(bucket_name=(bytes, str), key=(bytes, str), upload_id=(bytes, str))
    def abort_multipart_upload(self, bucket_name, key, upload_id, config=None):
        """
        Abort upload a part which is being uploading.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None
        :return:
            **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  key,
                                  params={b'uploadId': upload_id})

    @required(bucket_name=(bytes, str), key=(bytes, str), upload_id=(bytes, str))
    def list_parts(self,
                   bucket_name,
                   key,
                   upload_id,
                   max_parts=None,
                   part_number_marker=None,
                   config=None):
        """
        List all the parts that have been upload success.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None

        :type max_parts: int
        :param max_parts: None

        :type part_number_marker: string
        :param part_number_marker: None
        :return:
            **_ListPartsResponse Class**
        """
        key = compat.convert_to_bytes(key)
        params = {b'uploadId': upload_id}
        if max_parts is not None:
            params[b'maxParts'] = max_parts
        if part_number_marker is not None:
            params[b'partNumberMarker'] = part_number_marker

        return self._send_request(http_methods.GET, bucket_name, key, params=params, config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str), upload_id=(bytes, str))
    def list_all_parts(self, bucket_name, key, upload_id, config=None):
        """

        :param bucket_name:
        :param key:
        :param upload_id:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        part_number_marker = None
        while True:
            response = self.list_parts(bucket_name, key, upload_id,
                                       part_number_marker=part_number_marker,
                                       config=config)
            for item in response.parts:
                yield item
            if not response.is_truncated:
                break
            part_number_marker = response.next_part_number_marker

    @required(bucket_name=(bytes, str))
    def list_multipart_uploads(self,
                               bucket_name,
                               max_uploads=None,
                               key_marker=None,
                               prefix=None,
                               delimiter=None,
                               config=None):
        """
        List all Multipart upload task which haven't been ended.(Completed Init_MultiPartUpload
        but not completed Complete_MultiPartUpload or Abort_MultiPartUpload)

        :type bucket: string
        :param bucket: None

        :type delimiter: string
        :param delimiter: None

        :type max_uploads: int
        :param max_uploads: <=1000

        :type key_marker: string
        :param key_marker: None

        :type prefix: string
        :param prefix: None

        :type upload_id_marker: string
        :param upload_id_marker:
        :return:
            **_ListMultipartUploadResponse Class**
        """
        params = {b'uploads': b''}
        if delimiter is not None:
            params[b'delimiter'] = delimiter
        if max_uploads is not None:
            params[b'maxUploads'] = max_uploads
        if key_marker is not None:
            params[b'keyMarker'] = key_marker
        if prefix is not None:
            params[b'prefix'] = prefix

        return self._send_request(http_methods.GET, bucket_name, params=params, config=config)

    @required(bucket_name=(bytes, str))
    def list_all_multipart_uploads(self, bucket_name, prefix=None, delimiter=None, config=None):
        """

        :param bucket_name:
        :param prefix:
        :param delimiter:
        :param config:
        :return:
        """
        key_marker = None
        while True:
            response = self.list_multipart_uploads(bucket_name,
                                                   key_marker=key_marker,
                                                   prefix=prefix,
                                                   delimiter=delimiter,
                                                   config=config)
            for item in response.uploads:
                yield item
            if not response.is_truncated:
                break
            if response.next_key_marker is not None:
                key_marker = response.next_key_marker
            elif response.uploads:
                key_marker = response.uploads[-1].key
            else:
                break

    def _upload_task(self,
                     bucket_name,
                     object_key,
                     upload_id,
                     part_number,
                     part_size,
                     file_name,
                     offset,
                     part_list,
                     uploadTaskHandle,
                     progress_callback=None,
                     traffic_limit=None):
        if uploadTaskHandle.is_cancel():
            _logger.debug("upload task canceled with partNumber={}!".format(part_number))
            return
        try:
            response = self.upload_part_from_file(bucket_name,
                                                  object_key,
                                                  upload_id,
                                                  part_number,
                                                  part_size,
                                                  file_name,
                                                  offset,
                                                  progress_callback=progress_callback,
                                                  traffic_limit=traffic_limit)
            part_list.append({"partNumber": part_number, "eTag": response.metadata.etag})
            _logger.debug("upload task success with partNumber={}!".format(part_number))
        except Exception as e:
            _logger.debug("upload task failed with partNumber={}!".format(part_number))
            raise e

    @required(bucket_name=(bytes, str), key=(bytes, str), file_name=(bytes, str))
    def put_super_obejct_from_file(self,
                                   bucket_name,
                                   key,
                                   file_name,
                                   chunk_size=5,
                                   thread_num=None,
                                   uploadTaskHandle=None,
                                   content_type=None,
                                   storage_class=None,
                                   user_headers=None,
                                   progress_callback=None,
                                   traffic_limit=None,
                                   config=None):
        """
        Multipart Upload file to FOS

        param chunk_size: part size , default part size is 5MB
        """
        # check params
        if chunk_size > 5 * 1024 or chunk_size <= 0:
            raise FosClientError("chunk size is valid, it should be more than 0 and not nore than 5120!")
        left_size = os.path.getsize(file_name)
        # if file size more than 48.8TB, reject
        if left_size > 50000 * 1024 * 1024 * 1024:
            raise FosClientError("File size must not be more than 48.8TB!")
        if thread_num is None or thread_num <= 1:
            thread_num = multiprocessing.cpu_count()
        part_size = chunk_size * 1024 * 1024
        total_part = left_size // part_size
        if left_size % part_size != 0:
            total_part += 1
        if uploadTaskHandle is None:
            uploadTaskHandle = UploadTaskHandle()
        # initial
        upload_id = self.initiate_multipart_upload(bucket_name,
                                                   key,
                                                   content_type=content_type,
                                                   storage_class=storage_class,
                                                   user_headers=user_headers).upload_id

        executor = ThreadPoolExecutor(thread_num)
        all_tasks = []
        offset = 0
        part_number = 1
        part_list = []

        while left_size > 0:
            if left_size < part_size:
                part_size = left_size
            temp_task= executor.submit(self._upload_task,
                                       bucket_name,
                                       key,
                                       upload_id,
                                       part_number,
                                       part_size,
                                       file_name,
                                       offset,
                                       part_list,
                                       uploadTaskHandle,
                                       progress_callback,
                                       traffic_limit)
            all_tasks.append(temp_task)
            left_size -= part_size
            offset += part_size
            part_number += 1
        # wait all upload task to exit
        wait(all_tasks, return_when=ALL_COMPLETED)
        if uploadTaskHandle.is_cancel():
            _logger.debug("putting super object is canceled!")
            self.abort_multipart_upload(bucket_name, key, upload_id=upload_id)
            return False
        elif len(part_list) != total_part:
            _logger.debug("putting super object failed!")
            self.abort_multipart_upload(bucket_name, key, upload_id=upload_id)
            return False
        # sort
        part_list.sort(key=lambda x: x["partNumber"])
        # complete_multipart_upload
        self.complete_multipart_upload(bucket_name, key, upload_id, part_list)
        return True

    @required(bucket_name=(bytes, str), key=(bytes, str), acl=(list, dict))
    def set_object_acl(self, bucket_name, key, acl, config=None):
        """
        Set Access Control Level of object

        :type bucket: string
        :param bucket: None

        :type acl: list of grant
        :param acl: None
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        self._send_request(http_methods.PUT,
                           bucket_name,
                           key,
                           body=json.dumps({'accessControlList': acl},
                                           default=FosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def set_object_canned_acl(self,
                              bucket_name,
                              key,
                              canned_acl=None,
                              grant_read=None,
                              grant_full_control=None,
                              config=None):
        """

        :type bucket_name: string
        :param bucket_name: None

        :type key: string
        :param key: None

        :type canned_acl: string
        :param canned_acl: for header 'x-fos-acl', it's value only is
        canned_acl.PRIVATE or canned_acl.PRIVATE_READ

        :type grant_read: string
        :param grant_read: Object id of getting READ right permission.
        for exapmle,grant_read = 'id="6c47...4c94",id="8c42...4c94"'

        :type grant_full_control: string
        :param grant_full_control: Object id of getting READ right permission.
        for exapmle,grant_full_control = 'id="6c47...4c94",id="8c42...4c94"'

        :param config:
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        headers = None
        num_args = 0
        if canned_acl is not None:
            headers = {http_headers.FOS_ACL: compat.convert_to_bytes(canned_acl)}
            num_args += 1
        if grant_read is not None:
            headers = {http_headers.FOS_GRANT_READ: compat.convert_to_bytes(grant_read)}
            num_args += 1
        if grant_full_control is not None:
            headers = {http_headers.FOS_GRANT_FULL_CONTROL: compat.convert_to_bytes(grant_full_control)}
            num_args += 1

        if num_args == 0:
            raise ValueError("donn't give any object canned acl arguments!")
        elif num_args >= 2:
            raise ValueError("cann't get more than one object canned acl arguments!")

        self._send_request(http_methods.PUT,
                           bucket_name,
                           key,
                           headers=headers,
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object_acl(self, bucket_name, key, config=None):
        """
        Get Access Control Level of object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  key,
                                  params={b'acl': b''},
                                  config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def delete_object_acl(self, bucket_name, key, config=None):
        """
        Get Access Control Level of  object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  key,
                                  params={b'acl': b''},
                                  config=config)

    def get_user_quota(self, config=None):
        """
        get user quota

        :param config:
        :return:
        """
        return self._send_request(http_methods.GET,
                                  params={b'userQuota': b''},
                                  config=config)
    
    @required(max_bucket_count=(int), max_capacity_mega_bytes=(int))
    def put_user_quota(self, max_bucket_count, max_capacity_mega_bytes, config=None):
        """
        put user quota

        :type max_bucket_count: int
        :param max_bucket_count: max bucket count

        :type max_capacity_mega_bytes: long
        :param max_capacity_mega_bytes: max capacity mega bytes

        :param config:
        :return:
        """
        return self._send_request(http_methods.PUT,
                                  body=json.dumps({'maxBucketCount': max_bucket_count,
                                                   'maxCapacityMegaBytes': max_capacity_mega_bytes}),
                                  params={b'userQuota': b''},
                                  config=config)

    def delete_user_quota(self, config=None):
        """
        delete user quota

        :param config:
        :return:
        """
        return self._send_request(http_methods.DELETE,
                                  params={b'userQuota': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))
    def get_notification(self, bucket_name, config=None):
        """
        get notification

        :type bucket_name: string
        :param bucket_name: bucket name

        :param config:
        :return:
        """
        return self._send_request(http_methods.GET,
                                  bucket_name=bucket_name,
                                  params={b'notification': b''},
                                  config=config)

    @required(bucket_name=(bytes, str), notifications=(list, ))
    def put_notification(self, bucket_name, notifications, config=None):
        """
        put user quota

        :type bucket_name: string
        :param bucket_name: bucket

        :type notifications: list of dict
        :param notifications: notifacation param

        :param config:
        :return:
        """
        return self._send_request(http_methods.PUT,
                                  bucket_name=bucket_name,
                                  body=json.dumps({'notifications': notifications}),
                                  params={b'notification': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))
    def delete_notification(self, bucket_name, config=None):
        """
        delete notification

        :type bucket_name: string
        :param bucket_name: bucket name

        :param config:
        :return:
        """
        return self._send_request(http_methods.DELETE,
                                  bucket_name=bucket_name,
                                  params={b'notification': b''},
                                  config=config,)

    def put_object_tagging(self, bucket_name, key, obj_tag_args, config=None):
        """
        put object tagging

        :type bucket_name: string
        :param bucket_name: bucket name

        :type key: string
        :param key: object name

        :type obj_tag_args: dict
        :param obj_tag_args: object tagging args

        :return:
        """
        return self._send_request(http_methods.PUT,
                                  bucket_name=bucket_name,
                                  key=key,
                                  body=json.dumps(obj_tag_args, default=FosClient._dump_acl_object),
                                  params={b'tagging': b''},
                                  config=config)

    def put_object_tagging_canned(self, bucket_name, key, tag_header, config=None):
        """
        put object tagging

        :type bucket_name: string
        :param bucket_name: bucket name

        :type key: string
        :param key: object name

        :type obj_tag_args: dict
        :param obj_tag_args: object tagging args

        :return:
        """
        headers = {http_headers.FOS_TAGGING: compat.convert_to_bytes(tag_header)}
        return self._send_request(http_methods.PUT,
                                  bucket_name=bucket_name,
                                  key=key,
                                  headers=headers,
                                  params={b'tagging': b''},
                                  config=config)

    def get_object_tagging(self, bucket_name, key, config=None):
        """
        put object tagging

        :type bucket_name: string
        :param bucket_name: bucket name

        :type key: string
        :param key: object name

        :return:
        """
        return self._send_request(http_methods.GET,
                                  bucket_name=bucket_name,
                                  key=key,
                                  params={b'tagging': b''},
                                  config=config)

    @staticmethod
    def _prepare_object_headers(content_length=None,
                                content_md5=None,
                                content_type=None,
                                content_sha256=None,
                                etag=None,
                                user_metadata=None,
                                storage_class=None,
                                user_headers=None,
                                encryption=None,
                                customer_key=None,
                                customer_key_md5=None,
                                traffic_limit=None,
                                object_tagging=None):
        headers = {}

        if content_length is not None:
            if content_length and content_length < 0:
                raise ValueError('content_length should not be negative.')
            headers[http_headers.CONTENT_LENGTH] = compat.convert_to_bytes(content_length)

        if content_md5 is not None:
            headers[http_headers.CONTENT_MD5] = utils.convert_to_standard_string(content_md5)

        if content_type is not None:
            headers[http_headers.CONTENT_TYPE] = utils.convert_to_standard_string(content_type)
        else:
            headers[http_headers.CONTENT_TYPE] = http_content_types.OCTET_STREAM

        if content_sha256 is not None:
            headers[http_headers.FOS_CONTENT_SHA256] = content_sha256

        if etag is not None:
            headers[http_headers.ETAG] = b'"%s"' % utils.convert_to_standard_string(etag)

        if user_metadata is not None:
            meta_size = 0
            if not isinstance(user_metadata, dict):
                raise TypeError('user_metadata should be of type dict.')
            for k, v in iteritems(user_metadata):
                k = utils.convert_to_standard_string(k)
                v = utils.convert_to_standard_string(v)
                normalized_key = http_headers.FOS_USER_METADATA_PREFIX + k
                headers[normalized_key] = v
                meta_size += len(normalized_key)
                meta_size += len(v)
            if meta_size > fos.MAX_USER_METADATA_SIZE:
                raise ValueError(
                    'Metadata size should not be greater than %d.' % fos.MAX_USER_METADATA_SIZE)

        if storage_class is not None:
            headers[http_headers.FOS_STORAGE_CLASS] = storage_class

        if encryption is not None:
            headers[http_headers.FOS_SERVER_SIDE_ENCRYPTION] = utils.convert_to_standard_string(encryption)

        if customer_key is not None:
            headers[http_headers.FOS_SERVER_SIDE_ENCRYPTION_CUSTOMER_KEY] = utils.convert_to_standard_string(customer_key)

        if customer_key_md5 is not None:
            headers[http_headers.FOS_SERVER_SIDE_ENCRYPTION_CUSTOMER_KEY_MD5] = utils.convert_to_standard_string(customer_key_md5)

        if user_headers is not None:
            try:
                headers = FosClient._get_user_header(headers, user_headers, False)
            except Exception as e:
                raise e
        
        if traffic_limit is not None:
            headers[http_headers.FOS_TRAFFIC_LIMIT] = traffic_limit

        if object_tagging is not None:
            headers[http_headers.FOS_TAGGING] = compat.convert_to_bytes(object_tagging)
        return headers

    @staticmethod
    def _get_user_header(headers, user_headers, is_copy=False):
        if not isinstance(user_headers, dict):
            raise TypeError('user_headers should be of type dict.')

        if not is_copy:
            user_headers_set = {http_headers.CACHE_CONTROL,
                                http_headers.CONTENT_ENCODING,
                                http_headers.CONTENT_DISPOSITION,
                                http_headers.EXPIRES,
                                http_headers.FOS_PROCESS}
        else:
            user_headers_set = {http_headers.FOS_COPY_SOURCE_IF_NONE_MATCH,
                                http_headers.FOS_COPY_SOURCE_IF_UNMODIFIED_SINCE,
                                http_headers.FOS_COPY_SOURCE_IF_MODIFIED_SINCE}

        for k, v in iteritems(user_headers):
            k = utils.convert_to_standard_string(k)
            v = utils.convert_to_standard_string(v)
            if k in user_headers_set:
                headers[k] = v
        return headers

    def _get_config_parameter(self, config, attr):
        result = None
        if config is not None:
            result = getattr(config, attr)
        if result is not None:
            return result
        return getattr(self.config, attr)

    @staticmethod
    def _get_path(config, bucket_name=None, key=None, _=False):
        _, host_name, _ = utils.parse_host_port(config.endpoint, config.protocol)
        if config.cname_enabled or utils.is_cname_like_host(host_name) or utils.is_custom_host(host_name, bucket_name):
            return utils.append_uri(flymeyun_fos.URL_PREFIX, key)

        return utils.append_uri(flymeyun_fos.URL_PREFIX, bucket_name, key)

    def _merge_config(self, config, bucket_name):
        new_config = copy.copy(self.config)
        if config is not None:
            new_config.merge_non_none_values(config)
        
        endpoint = self._change_user_endpoint(new_config, bucket_name)
        new_config.endpoint = endpoint
        return new_config

    @classmethod
    def _change_user_endpoint(cls, config, bucket_name):
        _, user_host_name, _ = utils.parse_host_port(config.endpoint, config.protocol)
        user_endpoint_split = compat.convert_to_bytes(user_host_name).split(b'.')
        user_endpoint = config.endpoint
        is_fos_path_style_host = utils.is_fos_suffixed_host(user_host_name) and len(user_endpoint_split) == 3
        # 1. check ipv4 or path style
        if utils.check_ipv4(user_host_name):
            return config.endpoint
        
        if config.path_style_enable:
            return config.endpoint
        
        # 2. check cname domain
        if config.cname_enabled or utils.is_cname_like_host(user_host_name):
            # cname domain
            if is_fos_path_style_host:
                raise ValueError('endpoint is not cname domain, please set cname_enabled=False')
            else:
                return config.endpoint
        
        # default use virtual-hosted endpoint
        if bucket_name is not None:
            if is_fos_path_style_host:
                # split http head
                if user_endpoint.startswith(HTTP_PROTOCOL_HEAD):
                    http_head_split = user_endpoint.split(b'//') 
                    if len(http_head_split) < 2:
                        return config.endpoint
                    bucket_endpoint = http_head_split[0] + b'//' + compat.convert_to_bytes(bucket_name) + b'.' + http_head_split[1]
                    return compat.convert_to_bytes(bucket_endpoint)
                else:
                    return compat.convert_to_bytes(bucket_name)+b'.' + compat.convert_to_bytes(user_endpoint)
        
        # check virtual-hosted endpoint's bucket_name is not query bucket_name
        if len(user_endpoint_split) == 4 and bucket_name is not None:
            if user_endpoint_split[0] != compat.convert_to_bytes(bucket_name):
                raise ValueError('your endpoint\'s bucket_name is not equal your query bucket_name!')

        return config.endpoint

    @staticmethod
    def _need_retry_backup_endpoint(error):
        # always retry on IOError
        if isinstance(error, IOError):
            return True

        # Only retry on a subset of service exceptions
        if isinstance(error, FosServerError):
            if error.status_code == http.client.INTERNAL_SERVER_ERROR:
                return True
            if error.status_code == http.client.SERVICE_UNAVAILABLE:
                return True
            if error.code == FosServerError.REQUEST_EXPIRED:
                return True
        return False

    def _send_request(self,
                      http_method,
                      bucket_name=None,
                      key=None,
                      body=None,
                      headers=None,
                      params=None,
                      config=None,
                      body_parser=None):
        config = self._merge_config(config, bucket_name)

        path = FosClient._get_path(config, bucket_name, key)
        if body_parser is None:
            body_parser = handler.parse_json

        try:
            return fos_http_client.send_request(
                config, fos_signer.sign, [handler.parse_error, body_parser],
                http_method, path, body, headers, params)
        except FosHttpClientError as e:
            # retry backup endpoint
            if config.backup_endpoint is None:
                raise e
            if FosClient._need_retry_backup_endpoint(e.last_error):
                _logger.debug(b'Retry for backup endpoint.')
                path = FosClient._get_path(config, bucket_name, key, True)
                return fos_http_client.send_request(
                    config, fos_signer.sign, [handler.parse_error, body_parser],
                    http_method, path, body, headers, params, True)
            else:
                raise e
