# cardano-handshake
Shared space for information about Handshake on Cardano

## Roadmap
- [ ] Create a set of dummy `DNSReferenceDatum` records at a validator address
    - [ ] Write basic validator
    - [ ] Write basic scripts
- [ ] Add basic documentation for consuming `DNSReferenceDatum` at reference contract address
- [ ] With team, answer questions below
- [ ] Implement minting validator

## DNSReferenceDatum
```haskell
data DNSReferenceDatum = DNSReferenceDatum
  { 
    origin  :: BuiltinByteString,
    soa     :: SOARecord,
    ns      :: [BuiltinByteString]
  }
```

---

## Current Actions
1. Decide on validation logic and validator parameters
2. Decide on minting logic
3. Decide on token naming, defining a new standard (with Mesh) if necessary
4. Then implement

### 1. Updating DNS Datum at Reference Validator
- Who can change the SOA and DNS records, and how?
- If holder of owner token, then can update datum
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