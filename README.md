# cardano-dns
Shared space for information about decentralized DNS on Cardano

This repo describes the decentralized DNS system designed by several teams.

- The Silk Toad
- Gimbalabs
- Blink Labs

The goal is a standard for creating decentralized DNS services on Cardano,
backed by data on the blockchain.

---

## How it works
- Mint two tokens, associated by name (see note): "DNS Reference Token" and "HNS Token"
- When an Auction is initialized, the HNS Token is locked in an Auction
- When the Auction is completed and the HNS Token is claimed, the DNS Reference Token is sent to Reference Contract Address
- Datum with Reference Token at Ref. Contract Address contains `DNSReferenceDatum`, which is our on-chain record.
- For more details see `/docs/app-architecture.md`

## Three Unique Token Policy IDs - Same Token Name
1. Domain Ownership HNS Token - eventually ends up in owner's wallet -- but it goes on a journey to get there (see below)
2. DNS Reference Authentication Token (DRAT) - locked at DNS Reference Validator with DNS Reference Datum
3. Bidding Token (MHABAT) "Minting HNS Auction Bidding Authentication Token" - the token name matches the HNS token being bid upon.

## On-Chain Examples - To be Posted 2024-01-29:
1. Correct PolicyID + Correct Token Name + Correct Datum
2. Correct Datum, but no Asset
3. Correct Datum, but wrong Asset Policy Id

## We think this case is no possible:
- Good Datum, correct PolicyID, but mismatched Token Name -- validators prevent this case -- Adrian is checking for loopholes

## Example Usage `write_datums`:

```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "example_4" "example.com,3600,A,192.168.1.1;example.com,,AAAA,2001:0db8:85a3:0000:0000:8a2e:0370:7334;www.example.com,28800,CNAME,example.com;example.com,42069,MX,mail.example.com;example.com,3600456, TXT, 'v=spf1 mx -all';example.com,,NS,ns1.example.com" ""
```

```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "treehouse" "treehouse.cardano,3600,A,192.168.1.1;treehouse.cardano,,ns,ns1.treehouse.cardano;treehouse.cardano,28800,CNAME,treehouse.cardano" ""
```

## Todo: Make a List of All System Parameters

---

## DNSReferenceDatum
> Updated 2024-01-26

```haskell
data DNSRecord = DNSRecord
    {   lhs   :: BuiltinByteString
    ,   ttl   :: Maybe Integer
    ,   rtype :: BuiltinByteString
    ,   rdata :: BuiltinByteString
    }


data DNSReferenceDatum = DNSReferenceDatum
    {   origin         :: TokenName
    ,   dnsRecords     :: [DNSRecord]
    ,   additionalData :: Maybe BuiltinData
    }
```

### Example `DNSReferenceDatum`
Updated 2024-01-26. Will be posted on-chain 2024-01-29:

We can write `DNSReferenceDatum` on-chain as inline datum, formatted as `.json`:
```json
{
    "constructor": 1,
    "fields": [
        {
            "bytes": "74726565686f757365"
        },
        {
            "list": [
                {
                    "constructor": 1,
                    "fields": [
                        {
                            "bytes": "74726565686f7573652e63617264616e6f"
                        },
                        {
                            "constructor": 0,
                            "fields": [
                                {
                                    "int": 3600
                                }
                            ]
                        },
                        {
                            "bytes": "3139322e3136382e312e31"
                        },
                        {
                            "bytes": "41"
                        }
                    ]
                },
                {
                    "constructor": 1,
                    "fields": [
                        {
                            "bytes": "74726565686f7573652e63617264616e6f"
                        },
                        {
                            "constructor": 1,
                            "fields": []
                        },
                        {
                            "bytes": "6e73312e74726565686f7573652e63617264616e6f"
                        },
                        {
                            "bytes": "6e73"
                        }
                    ]
                },
                {
                    "constructor": 1,
                    "fields": [
                        {
                            "bytes": "74726565686f7573652e63617264616e6f"
                        },
                        {
                            "constructor": 0,
                            "fields": [
                                {
                                    "int": 28800
                                }
                            ]
                        },
                        {
                            "bytes": "74726565686f7573652e63617264616e6f"
                        },
                        {
                            "bytes": "434e414d45"
                        }
                    ]
                }
            ]
        },
        {
            "constructor": 1,
            "fields": []
        }
    ]
}
```

### Example Root Domain Record
```json
{
   constructor: 1,
   fields: [
      {
         bytes: "2e"
      },
      [
         {
            constructor: 1,
            fields: [
               {
                  bytes: "2e"
               },
               {
                  bytes: "6e73"
               },
               {
                  bytes: "6e73312e63617264616e6f"
               }
            ]
         },
         {
            constructor: 1,
            fields: [
               {
                  bytes: "6e73312e63617264616e6f"
               },
               {
                  bytes: "61"
               },
               {
                  bytes: "3137322e32382e302e32"
               }
            ]
         }
      ]
   ]
}
```


## Example - Updates coming 2024-01-29
Updated 2024-01-14 with new DNS Reference Validator Address `addr_test1vzetgvj80ut4pfg02z7jncgpg4lzj4nt6rtcpmtywfce58gjvkr54`

Query this example of a DNS Reference Validator Address: [addr_test1vzetgvj80ut4pfg02z7jncgpg4lzj4nt6rtcpmtywfce58gjvkr54](https://preprod.cardanoscan.io/address/addr_test1vzetgvj80ut4pfg02z7jncgpg4lzj4nt6rtcpmtywfce58gjvkr54)

For example with `https://preprod.gomaestro-api.org/addresses/utxos`:
```bash
curl -X POST \
  -H "api-key: ${MAESTRO_API_KEY_PREPROD}" \
  https://preprod.gomaestro-api.org/v1/addresses/utxos \
  -H "Content-Type: application/json" \
  -d '["addr_test1vzetgvj80ut4pfg02z7jncgpg4lzj4nt6rtcpmtywfce58gjvkr54"]'
```

See [Example response](example.json)

### Creating a .cardano zone file

Using the above example, we can now build a zone file. Using the
[dns.py](dns.py) Python script, we can output a zone file suitable for serving
a `.cardano` domain with the data from our example. This is a simple proof of
concept of transaction parsing using a remote API.

* Using [gomaestro] API:
```bash
export MAESTRO_API_KEY=${MAESTRO_API_KEY}
python3 dns.py > cardano.zone
```
* Using [kupo] API:
```bash
pip install cbor2 uplc
python3 dns-kupo.py > cardano.zone
```

The current zone [file](cardano.zone) includes our datum from above.

* Using [cdnsd]:
The `cdnsd` daemon is a purpose-built indexer and DNS server.

https://github.com/blinklabs-io/cdnsd

---

# Plutus Contracts
Repo: https://gitlab.com/gimbalabs/handshake-plutus

## Principles
- Build for re-use
- Build for recursive deployment

## Outline
- Reference Validation Logic: How to Update DNS Datum
- Minting Logic
- Token Naming
- Auction Contracts
- Governance Contracts

## Usage:
- In [Plutus Apps](https://github.com/input-output-hk/plutus-apps), `git checkout c4f4dc5fedd5b1804781abb7db0fb5a553e24ecb`

---

## Roadmap

### Reference Validation Logic: How to Update DNS Datum
- [ ] Implement Update Logic

### Minting Logic
If these conditions are met, mint a token pair:
- DNSReferenceDatum.origin must match TokenName
- DNSReferenceDatum.origin must meet DNS validation rules
- TokenName must be new/unique
- Must mint token pair with matching names
- One token must be minted to Reference Validator
- Reference Datum must be valid

### Token Naming
- Start by applying CIP-68. If we realize the need for a new standard, then create it.
- Automate contract-based name validation

### Auction Contracts
- See https://en.wikipedia.org/wiki/Vickrey_auction
- Handshake uses a modified Vickrey auction, emulate this
- Next Step: Define Auction Rules -> Implement in SC
- Test a [Hydra implementation](https://hydra.family/head-protocol/use-cases/nft-auction/)

### Governance Contracts
- Apply SCG governance
- What experiments do we want to run?

### Nested Implementation
- create an instance of N+1 domain - require locking of N in order to build instance
- One address where all SLD Records are held
- Another validator that handles TLD logic
    - Includes some set of governance parameters
- fractal n+1 level domain registration / minting
- Mint an SLD on a Given TLD
- revocation list for a given TLD
- If I hold a TLD, I can:
    - delegate it (permanently?) to a contract where I can mint SLDs

- If I hold a SLD, I can:
    - a. create or edit a DNS record at that SLD, OR
    - b. create 3rdLDs on my SLD

[gomaestro]: https://www.gomaestro.org/
[kupo]: https://github.com/CardanoSolutions/kupo/
