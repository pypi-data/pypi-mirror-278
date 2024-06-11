"""
   Copyright 2020-2024 MiPasa

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
import cgi
from io import BytesIO
import json
import urllib.parse
import requests


DEFAULT_GATEWAY_URL = 'https://gateway-proxy-bee-3-0.gateway.ethswarm.org'


class SwarmError(Exception):
    def __init__(self, msg, swarm_hash=None):
        super().__init__(msg)
        self.swarm_hash = swarm_hash


class SwarmAPIError(SwarmError):
    def __init__(self, msg, swarm_hash=None, status_code=None):
        super().__init__(msg, swarm_hash=swarm_hash)
        self.status_code = status_code


class SwarmTypeError(SwarmError):
    def __init__(self, msg, swarm_hash=None, expected_type=None, actual_type=None):
        super().__init__(msg, swarm_hash=swarm_hash)
        self.expected_type = expected_type
        self.actual_type = actual_type


class SwarmConnection:
    def __init__(self, gateway_url=DEFAULT_GATEWAY_URL):
        self.gateway_url = gateway_url

    def __repr__(self):
        return "<SwarmConnection>"

    @staticmethod
    def _detect_type(r):
        if "Content-Type" in r.headers:
            t = r.headers["Content-Type"]
            if t == "text/csv":
                return "csv"
            elif t == "application/json":
                return "json"
            elif t == "application/vnd.apache.parquet" or t == "application/parquet":
                return "parquet"

        if "Content-Disposition" in r.headers:
            _, params = cgi.parse_header(r.headers["Content-Disposition"])
            if "filename" in params:
                _, ext = os.path.splitext(params["filename"])
                ext = ext.lower()
                if ext == ".csv":
                    return "csv"
                elif ext == ".json":
                    return "json"
                elif ext == ".parquet":
                    return "parquet"

        return "bytes"

    def _read_file_internal(self, swarm_hash):
        r = requests.get(
            '%s/bzz/%s' % (self.gateway_url, urllib.parse.quote(swarm_hash))
        )

        if r.status_code != 200:
            raise SwarmAPIError(
                'Hash %s not found or could not be retrieved from Swarm (code %d)'
                % (repr(swarm_hash), r.status_code),
                swarm_hash=swarm_hash,
                status_code=r.status_code,
            )

        data_type = self._detect_type(r)
        return r.content, data_type

    @staticmethod
    def _load_optional_pandas():
        try:
            import pandas as pd
            return pd
        except ImportError:
            raise ImportError('Pandas is not installed, but required for read_csv and read_parquet functions.')

    @staticmethod
    def _check_optional_parquet():
        try:
            import pyarrow
        except ImportError:
            try:
                import fastparquet
            except ImportError:
                raise ImportError('Neither PyArrow or FastParquet are installed, but required for read_parquet function.')

    def _reinterpret_file(self, content, data_type):
        if data_type == "csv":
            pd = self._load_optional_pandas()
            f = BytesIO(content)
            return pd.read_csv(f)
        elif data_type == "parquet":
            pd = self._load_optional_pandas()
            self._check_optional_parquet()
            f = BytesIO(content)
            return pd.read_parquet(f)
        elif data_type == "json":
            f = BytesIO(content)
            return json.load(f)
        else:
            return content

    def read_file(self, swarm_hash, as_type="bytes", verify_type=False):
        allowed_types = [None, 'bytes', 'csv', 'parquet', 'json']
        if as_type not in allowed_types:
            raise ValueError('Unsupported type %s (expected one of %s)' % (repr(as_type), ', '.join(map(repr, allowed_types))))

        content, data_type = self._read_file_internal(swarm_hash)

        if as_type == "bytes":
            return content

        if verify_type and as_type is not None and data_type != as_type:
            raise SwarmTypeError(
                'Hash %s is not of type %s' % (repr(swarm_hash), repr(as_type)),
                swarm_hash=swarm_hash,
                expected_type=as_type,
                actual_type=data_type
            )

        return self._reinterpret_file(content, as_type)

    def read_csv(self, swarm_hash):
        return self.read_file(swarm_hash, as_type="csv")

    def read_parquet(self, swarm_hash):
        return self.read_file(swarm_hash, as_type="parquet")

    def read_json(self, swarm_hash):
        return self.read_file(swarm_hash, as_type="json")
