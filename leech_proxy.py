#!/usr/bin/env python3

import proxy
import re
import ipaddress

from proxy.common.utils import bytes_, text_
from proxy.http.parser import HttpParser
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.methods import httpMethods
from typing import Optional

class TrackerRequestRewritePlugin(HttpProxyBasePlugin):
    """Modify tracker GET request to report different upload data."""

    def before_upstream_connection(
            self, request: HttpParser) -> Optional[HttpParser]:
        return request

    def handle_client_request(
            self, request: HttpParser) -> Optional[HttpParser]:
        if request.method == httpMethods.GET:
            path_str = text_(request.path)
            downloaded = 0
            match = re.search('(?:^|\\?|&)downloaded=(\\d+)(?:&|$)', path_str)
            if match:
                downloaded = int(match.group(1))
            match = re.search('(?:^|\\?|&)uploaded=(\\d+)(?:&|$)', path_str)
            if match:
                uploaded = int(downloaded * 1.2 if downloaded > 0 else int(match.group(1)) * 1.2)
                path_str = path_str[:match.start(1)] + str(uploaded) + path_str[match.end(1):]
                request.path = bytes_(path_str)
        return request

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        return chunk

    def on_upstream_connection_close(self) -> None:
        pass

if __name__ == '__main__':
    proxy.main(
        hostname = ipaddress.IPv4Address('127.0.0.1'),
        plugins = ['__main__.TorrentLeechPlugin'],
        ca_key_file = '/Users/imagi/ca-key.pem',
        ca_cert_file = '/Users/imagi/ca-cert.pem',
        ca_signing_key_file = '/Users/imagi/ca-signing-key.pem',
        ca_file = '/Users/imagi/cacert.pem',
    )   
