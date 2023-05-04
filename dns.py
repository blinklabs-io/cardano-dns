#!/usr/bin/env python3

import json
import os
import requests
import time

ADDRESS = 'addr_test1wqgf0d7rdlamdy46hd5u5wq47ql9chvv8w3k70nyqcfgd2qwpvxpx'
NETWORK = 'preprod'

API_KEY = os.environ['MAESTRO_API_KEY']

def main():
    maestro = 'https://' + NETWORK + '.gomaestro-api.org'
    custom_headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = [ADDRESS]
    utxos = requests.post(f"{maestro}/addresses/utxos", json=data, headers=custom_headers, timeout=60)
    txs = json.loads(utxos.content.decode())
    # print(json.dumps(txs, indent=2))

    cardano = dict()
    now = int(time.time())

    print("$ORIGIN cardano.")
    print("$TTL 60")
    print("@ IN SOA ns.cardano. hostmaster.cardano. ("+str(now)+", 21600, 3600, 604800, 60)")

    for tx in txs:
        name = bytes.fromhex(tx['datum']['json']['fields'][0]['bytes']).decode()
        origin = bytes.fromhex(tx['datum']['json']['fields'][1]['bytes']).decode()
        soa_raw = tx['datum']['json']['fields'][2]['fields']
        ns_list = tx['datum']['json']['fields'][3]['list']

        if origin.split(".")[-1] == 'cardano':
            cardano[name] = dict({"origin": origin})
            for ns in ns_list:
                print(name + " IN NS " + bytes.fromhex(ns['bytes']).decode() + ".")

if __name__ == '__main__':
    main()

