# leech_proxy
Greedy Torrent clone for Linux / Mac / whatever capable of running Python

## Setup

1. python3 -m pip proxy.py
2. Generate SSL certficates - https://github.com/abhinavsingh/proxy.py#tls-interception. This should produce ca-cert.pem ca-key.pem and ca-signing-key.pem
3. Download https://curl.se/ca/cacert.pem
4. Run python3 leech_proxy.py

## transmission-daemon setup

1. Edit transmission-daemon.service
2. Add the following line to the [Service] section:
    `Environment="HTTP_PROXY=http://127.0.0.1:8899" "HTTPS_PROXY=http://127.0.0.1:8899" "CURL_CA_BUNDLE=<path to>/ca-cert.pem"`