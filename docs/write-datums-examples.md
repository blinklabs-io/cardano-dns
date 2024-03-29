# Example Usage `write_datums`:

## Updated Examples - 2024-02-01

### `village.cardano` - All Correct
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "village" "village.cardano,3600,A,172.28.0.2;village.cardano,28800,ns,ns1.village.cardano;" ""
```
### `city.cardano` - Good Datum, Wrong PolicyID
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "city" "city.cardano,3600,A,172.28.0.2;city.cardano,28800,ns,ns1.city.cardano;" ""
```

### `town.cardano` - Good Datum, No Asset
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "town" "town.cardano,3600,A,172.28.0.2;town.cardano,28800,ns,ns1.town.cardano;" ""
```

### `enclave.cardano` - All Correct, but first DNS Record is a bad IP address
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "enclave" "enclave.cardano,3600,A,401.401.401.401;enclave.cardano,28800,ns,ns1.enclave.cardano;enclave.cardano,3600,A,172.28.0.2;enclave.cardano,,ns,ns2.enclave.cardano;" ""
```

## Wrong Examples - `rtype` and `rdata` in wrong order:

### `treehouse.cardano`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "treehouse" "treehouse.cardano,3600,A,192.168.1.1;treehouse.cardano,,ns,ns1.treehouse.cardano;treehouse.cardano,28800,CNAME,treehouse.cardano" ""
```

### `dolphin.cardano`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "dolphin" "dolphin.cardano,3600,A,111.222.333.444;dolphin.cardano,,ns,ns1.dolphin.cardano;dolphin.cardano,28800,ns2,ns2.dolphin.cardano" ""
```

### `whale.cardano`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "whale" "whale.cardano,3600,A,192.168.1.1;whale.cardano,,ns,ns1.whale.cardano;whale.cardano,28800,CNAME,whale.cardano" ""
```

### `ghost.cardano`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "ghost" "ghost.cardano,3600,A,192.168.1.1;ghost.cardano,,ns,ns1.ghost.cardano;ghost.cardano,3600,ns,ns2.ghost.cardano" ""
```

### `orca.ergo`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "orca" "orca.ergo,3600,A,192.168.1.1;orca.ergo,,ns,ns1.orca.ergo;orca.ergo,28800,CNAME,orca.ergo" ""
```

### `example.com`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "example_4" "example.com,3600,A,192.168.1.1;example.com,,AAAA,2001:0db8:85a3:0000:0000:8a2e:0370:7334;www.example.com,28800,CNAME,example.com;example.com,42069,MX,mail.example.com;example.com,3600456, TXT, 'v=spf1 mx -all';example.com,,NS,ns1.example.com" ""
```

### `.cardano`
```bash
cabal run write_datums . "DNSReference" "DNSReferenceDatum" "1" "." ".cardano,,A,172.28.0.2;.cardano,,ns,n1.cardano." ""
```