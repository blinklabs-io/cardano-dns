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
- The outcome of the auction system is to mint two tokens, associated by name: DNS Reference Token (`DRAT`) and `HNS Token`
- When an Auction is initialized, the HNS Token is minted and locked in an Auction
- When the Auction is completed and the HNS Token is claimed, the DNS Reference Token is minted and sent to DNS Reference Contract Address
- Datum with Reference Token at Ref. Contract Address contains `DNSReferenceDatum`, which is our on-chain record.
- For more details see [/docs/app-architecture.md](/docs/app-architecture.md)

## Three Unique Token Policy IDs - Same Token Name
1. Domain Ownership is represented by `HNS Token` - eventually ends up in owner's wallet.
2. DNS Reference Authentication Token (`DRAT`) - locked at DNS Reference Validator with DNS Reference Datum
3. Bidding Token (`MHABAT`) "Minting HNS Auction Bidding Authentication Token" - the token name matches the HNS token being bid upon.

---

# Testing 2024-01-29

## On-Chain Examples
Updated 2024-01-29 with temporary DNS Reference Testing Address [addr_test1vr75xezmpxastymx985l3gamuxrwqdwcfrcnjlygs55aynsqu3edq](https://preprod.cardanoscan.io/address/addr_test1vr75xezmpxastymx985l3gamuxrwqdwcfrcnjlygs55aynsqu3edq)

Query with `https://preprod.gomaestro-api.org/addresses/utxos`:
```bash
curl -X POST \
  -H "api-key: ${MAESTRO_API_KEY_PREPROD}" \
  https://preprod.gomaestro-api.org/v1/addresses/utxos \
  -H "Content-Type: application/json" \
  -d '["addr_test1vr75xezmpxastymx985l3gamuxrwqdwcfrcnjlygs55aynsqu3edq"]'
```

See [Example response](example.json)

## When Testing, Look For:
1. Correct PolicyID + Correct Token Name + Correct Datum: `village.cardano`
2. Correct PolicyID + Correct Token Name + Correct Datum, with first `a` and `ns` records mapping to bad IP address: `enclave.cardano`
3. Ok Datum, but no Asset: `town.cardano`
4. Correct Datum, but wrong Asset Policy Id: `city.cardano`

> Full list: [/docs/write-datums-examples.md](/docs/write-datums-examples.md)

## We think this case is not possible:
- Good Datum, correct PolicyID, but mismatched Token Name -- validators prevent this case -- Adrian is checking for loopholes

### Parameters
- Testing Address: `addr_test1vr75xezmpxastymx985l3gamuxrwqdwcfrcnjlygs55aynsqu3edq`
- Correct `.cardano` PolicyID: `6af60c2a7a06551ef09b3810a41d086b26ca26f926d22e462103194d`
- "Wrong" PolicyID Example: `602406ccbbbc071846eb38d1db876b90d6233747b626e38c8255ca7a` (could be any policy ID other than the correct `.cardano` one)

### Notes
- TLD is not included in the `TokenName`. The TLD is implied by the `CurrencySymbol`
- Check that resolver rejects other TLDs. `orca.ergo` is provided as an example

### Todo: Make a List of All System Parameters

---

## DNSReferenceDatum
> Updated 2024-01-29

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
Updated 2024-01-29.

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
