# Copyright 2014 xjmz, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module defines string constants for HTTP headers
"""

# Standard HTTP Headers

AUTHORIZATION = b"Authorization"

CACHE_CONTROL = b"Cache-Control"

CONTENT_DISPOSITION = b"Content-Disposition"

CONTENT_ENCODING = b"Content-Encoding"

CONTENT_LENGTH = b"Content-Length"

CONTENT_MD5 = b"Content-MD5"

CONTENT_TYPE = b"Content-Type"

ETAG = b"ETag"

EXPIRES = b"Expires"

HOST = b"Host"

RANGE = b"Range"

USER_AGENT = b"User-Agent"

# FOS Common HTTP Headers

FOS_PREFIX = b"x-fos-"

FOS_ACL = b"x-fos-acl"

FOS_CONTENT_SHA256 = b"x-fos-content-sha256"

FOS_COPY_METADATA_DIRECTIVE = b"x-fos-metadata-directive"

FOS_COPY_SOURCE = b"x-fos-copy-source"

FOS_COPY_SOURCE_IF_MATCH = b"x-fos-copy-source-if-match"

FOS_COPY_SOURCE_IF_MODIFIED_SINCE = b"x-fos-copy-source-if-modified-since"

FOS_COPY_SOURCE_IF_NONE_MATCH = b"x-fos-copy-source-if-none-match"

FOS_COPY_SOURCE_IF_UNMODIFIED_SINCE = b"x-fos-copy-source-if-unmodified-since"

FOS_COPY_SOURCE_RANGE = b"x-fos-copy-source-range"

FOS_DATE = b"x-fos-date"

FOS_USER_METADATA_PREFIX = b"x-fos-meta-"

# FOS HTTP Headers

FOS_STORAGE_CLASS = b"x-fos-storage-class"

FOS_GRANT_READ = b'x-fos-grant-read'

FOS_GRANT_FULL_CONTROL = b'x-fos-grant-full-control'

FOS_SERVER_SIDE_ENCRYPTION = b"x-fos-server-side-encryption"

FOS_SERVER_SIDE_ENCRYPTION_CUSTOMER_KEY = b"x-fos-server-side-encryption-customer-key"

FOS_SERVER_SIDE_ENCRYPTION_CUSTOMER_KEY_MD5 = b"x-fos-server-side-encryption-customer-key-md5"

FOS_TRAFFIC_LIMIT = b"x-fos-traffic-limit"

# STS HTTP Headers

FOS_TAGGING = b"x-fos-tagging"

FOS_PROCESS = b"x-fos-process"
