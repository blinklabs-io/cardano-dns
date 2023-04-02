# cardano-handshake
Shared space for information about Handshake on Cardano

---

## How it works
- Mint two tokens, associated by name (see note): "Reference Token" and "Owner Token"
- At minting, Owner Token is sent to wallet address of buyer
- At minting, Reference Token is sent to Reference Contract Address
- Datum with Reference Token at Ref. Contract Address contains `DNSReferenceDatum`, which is our on-chain record.

### Questions
- Naming doesn't feel good. Moving toward new CIP. How do we want to handle in this case? Owner should hold a token named `theirdomain.cardano` - in which case, what do we name the reference token? `REFtheirdomain.cardano`? 

---

## DNSReferenceDatum
- Do we need both `name` and `origin`?
- Is it sufficient for `ns` to be a simple list?
```haskell
data DNSReferenceDatum = DNSReferenceDatum
  { 
    name    :: BuiltinByteString,
    origin  :: BuiltinByteString,
    soa     :: SOARecord,
    ns      :: [BuiltinByteString]
  }

-- where:
data SOARecord = SOARecord 
  {
    soaMname       :: BuiltinByteString,
    soaRname       :: BuiltinByteString,
    soaSerial      :: Integer,
    soaRefresh     :: Integer,
    soaRetry       :: Integer,
    soaExpire      :: Integer,
    soaTtl         :: Integer
  }
```

We can write `DNSReferenceDatum` on-chain as inline datum, formatted as `.json`:
```json
{
  "constructor": 0,
  "fields": [
    { "bytes": "6d696c6b7368616b65" },
    { "bytes": "6d696c6b7368616b652e63617264616e6f" },
    {
      "constructor": 0,
      "fields": [
        { "bytes": "6e73312e6d696c6b7368616b652e63617264616e6f" },
        { "bytes": "686f73742e6578616d706c652e646f6d61696e" },
        { "int": 1680427566 },
        { "int": 3600 },
        { "int": 600 },
        { "int": 604800 },
        { "int": 86400 }
      ]
    },
    { 
      "list": [
        { 
          "constructor": 0, 
          "fields": [
            { "bytes": "6e73312e6d696c6b7368616b652e63617264616e6f" }, 
            { "bytes": "6e73322e6d696c6b7368616b652e63617264616e6f" }
          ] 
        }
      ]
    }
  ]
}
```

## Example
Query this example of a DNS Reference Validator Address: [addr_test1wqgf0d7rdlamdy46hd5u5wq47ql9chvv8w3k70nyqcfgd2qwpvxpx](https://preprod.cardanoscan.io/address/701097b7c36ffbb692babb69ca3815f03e5c5d8c3ba36f3e64061286a8)

For example with `https://preprod.gomaestro-api.org/addresses/utxos`:
```bash
curl -X POST \
  -H "api-key: DrhTBZ40MGef8XYWbwIi6ej4CAw7tgwP" \
  https://preprod.gomaestro-api.org/addresses/utxos \
  -H "Content-Type: application/json" \
  -d '["addr_test1wqgf0d7rdlamdy46hd5u5wq47ql9chvv8w3k70nyqcfgd2qwpvxpx"]'  
```

See [Example response](example.json)

---

## Current Actions
1. Decide on validation logic and validator parameters
2. Decide on minting logic
3. Decide on token naming, defining a new standard (with Mesh) if necessary
4. Then implement

### 1. Updating DNS Datum at Reference Validator
- Is the datum above sufficient?
- Are SOA and DNS record immutable?
- If not, who can change the SOA and DNS records?
- MVP allows owner of domain to change SOA and DNS.
- Who holds an admin token? Should admin token exist? With what powers?

### 2. Decide on minting logic Minting Conditions
- How is the domain name itself handled? -> At minting, `DNSReferenceDatum.origin` must match `TokenName`.
- If Reference Datum matches token name, mint a token pair. 
- Must mint token pair with matching names
- One token must be minted to Reference Validator
- Reference Datum must be valid
- Domain token name must be unique -> best way to handle is with an App Token. Then use Maestro to determine if App signs Tx.

### 3. Token Naming
- CIP68-sufficient, or new standard for associated tokens?

### 4. Answer questions above -> Development Roadmap

---

## Case Study + General Design
### Case Study: Minting a `.cardano` domain token

### General design
- Is recursive design part of MVP?

---

## Roadmap
- [x] Create a set of dummy `DNSReferenceDatum` records at a validator address
    - [x] Implement essential validator
    - [x] For initial example, use simple minting policy as placeholder
    - [x] Write basic scripts for minting token pairs
    - [x] Use to create datum
- [x] Add basic documentation for consuming `DNSReferenceDatum` at reference contract address
- [ ] With team, answer questions below (sync / async?)
- [ ] Fully implement reference validator
- [ ] Fully implement minting validator