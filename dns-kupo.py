#!/usr/bin/env python3

import json
import os
import requests
import time
import uplc
import cbor2

ADDRESS = 'addr_test1wqgf0d7rdlamdy46hd5u5wq47ql9chvv8w3k70nyqcfgd2qwpvxpx'
NETWORK = 'iohk-preprod'
KUPO_URL = 'https://d.kupo-api.' + NETWORK + '.dandelion.link'

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
        origin = bytes.fromhex(datum_json['fields'][1]['bytes']).decode()
        soa_raw = datum_json['fields'][2]['fields']
        ns_list = datum_json['fields'][3]['list']

        if origin.split(".")[-1] == 'cardano':
            cardano[name] = dict({"origin": origin})
            for ns in ns_list:
                print(name + " IN NS " + bytes.fromhex(ns['bytes']).decode() + ".")
                print(bytes.fromhex(ns['bytes']).decode() + ". IN A 172.17.0.1")

if __name__ == '__main__':
    main()

