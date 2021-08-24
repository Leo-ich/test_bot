#!/usr/bin/env bash

# generate a self-signed certificate and private key

openssl req -x509 -days 3650 -out webhook_cert.crt -keyout webhook_pkey.key \
-newkey rsa:2048 -nodes -sha256 \
-subj '/CN=tzortestbot.herokuapp.com' -extensions EXT -config <( \
printf "[dn]\nCN=tzortestbot.herokuapp.com\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:tzortestbot.herokuapp.com\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")

# In "Common Name (eg, your name or your server's hostname)"
# you should specify the IP address of the server or
# the domain name of the server.
