# cardano-handshake
Shared space for information about Handshake on Cardano

## Roadmap
- [x] Create a set of dummy `DNSReferenceDatum` records at a validator address
    - [x] Implement essential validator
    - [x] For initial example, use simple minting policy as placeholder
    - [x] Write basic scripts for minting token pairs
    - [x] Use to create datum
- [ ] Add basic documentation for consuming `DNSReferenceDatum` at reference contract address
- [ ] With team, answer questions below (sync / async?)
- [ ] Fully implement reference validator
- [ ] Fully implement minting validator

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
    { "list": [{ "constructor": 0, "fields": [{ "bytes": "6e73312e6d696c6b7368616b652e63617264616e6f" }, { "bytes": "6e73322e6d696c6b7368616b652e63617264616e6f" }] }] }
  ]
}
```

## Example
Query this example of a DNS Reference Validator Address: [addr_test1wpsen790sz5rw9f7pt5c6rtm3kf9rpj3n32jtenuj02qqhga2unhd](https://preprod.cardanoscan.io/address/706199f8af80a837153e0ae98d0d7b8d925186519c5525e67c93d4005d)

For example with `https://preprod.gomaestro-api.org/addresses/utxos`:
```bash
curl -X POST \
  -H "api-key: <your_project_api_key>" \
  https://preprod.gomaestro-api.org/addresses/utxos \
  -H "Content-Type: application/json" \
  -d '["addr_test1wpsen790sz5rw9f7pt5c6rtm3kf9rpj3n32jtenuj02qqhga2unhd"]'  
```

See [Example response](example-query-response.json)

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