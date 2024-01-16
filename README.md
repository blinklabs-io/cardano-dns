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
- Mint two tokens, associated by name (see note): "Reference Token" and "Owner Token"
- At minting, Owner Token is sent to wallet address of buyer
- At minting, Reference Token is sent to Reference Contract Address
- Datum with Reference Token at Ref. Contract Address contains `DNSReferenceDatum`, which is our on-chain record.

### Questions
- Currently using simple naming convention with `222` prefix on Owner token and `100` prefix on Reference token. This naming doesn't feel right. A broader group is moving toward new CIP.

How do we want to handle this case? Owner should hold a token named `theirdomain.cardano` - in which case, what do we name the reference token? `REFtheirdomain.cardano`?

---

## DNSReferenceDatum
> Updated 2023-11-08

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

We can write `DNSReferenceDatum` on-chain as inline datum, formatted as `.json`:
```json
{
   constructor: 1,
   fields: [
      {
         bytes: "646f6c7068696e2e63617264616e6f"
      },
      [
         {
            constructor: 1,
            fields: [
               {
                  bytes: "646f6c7068696e2e63617264616e6f"
               },
               {
                  bytes: "6e73"
               },
               {
                  bytes: "6e73312e646f6c7068696e2e63617264616e6f"
               }
            ]
         },
         {
            constructor: 1,
            fields: [
               {
                  bytes: "6e73312e646f6c7068696e2e63617264616e6f"
               },
               {
                  bytes: "61"
               },
               {
                  bytes: "3137322e32382e302e33"
               }
            ]
         }
      ]
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


## Example
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
