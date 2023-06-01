#!/usr/bin/env python3

import json
import os
import requests
import time
import uplc
import cbor2

ADDRESS = os.getenv('ADDRESS', 'addr_test1wqhlsl9dsny9d2hdc9uyx4ktj0ty0s8kxev4y9futq4qt4s5anczn')
NETWORK = os.getenv('NETWORK', 'iohk-preprod')
KUPO_URL = os.getenv('KUPO_URL', 'https://d.kupo-api.' + NETWORK + '.dandelion.link')

def main():
    custom_headers = {"Content-Type": "application/json"}
    utxos = requests.get(f"{KUPO_URL}/matches/{ADDRESS}?unspent", headers=custom_headers, timeout=60)
    txs = json.loads(utxos.content.decode())

    cardano = dict()
    now = int(time.time())

    print("$ORIGIN cardano.")
    print("$TTL 60")
    print("@ IN SOA ns1.cardano. hostmaster.cardano. "+str(now)+" 21600 3600 604800 60")
    print("  IN NS ns1.cardano.")
    print("ns1.cardano. IN A 172.17.0.1")

    for tx in txs:
        datum_bytes = json.loads(requests.get(f"{KUPO_URL}/datums/{tx['datum_hash']}", headers=custom_headers, timeout=60).content)['datum']

        datum_json = uplc.ast.data_from_cbortag(cbor2.loads(bytes.fromhex(datum_bytes))).to_json()
        
        name = bytes.fromhex(datum_json['fields'][0]['bytes']).decode()
        ns_list = datum_json['fields'][1]['list']

        for ns in ns_list:
            print(name + " IN NS " + bytes.fromhex(ns['bytes']).decode() + ".")
            print(bytes.fromhex(ns['bytes']).decode() + ". IN A 172.17.0.1")

if __name__ == '__main__':
    main()

