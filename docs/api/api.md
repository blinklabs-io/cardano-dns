# Drafting API Docs

## Todo:
- [ ] Write docs for `hns-canvas`
- [ ] Use `hs-harmony` to build a helpful framework for App front-end
- [ ] Include all project parameters in documentation


## `/api/v1/tx`

### `/api/v1/tx/mint+hns`

Request Example:
```

```

Request Body
```json
{
    "address": "", // from connected wallet
    "changeAddress": "", // from connected wallet
    "UserUTxOs": [], // from connected wallet
    "CollateralUTxO": {}, // from connected wallet
    "HNSTokenName": "", // via user input
    "MinAmount": 0 // Get from Min amount / purchaseAmount
}
```

### `/api/v1/tx/bid+hns`

### `/api/v1/tx/update+bid`

### `/api/v1/tx/bid+disclosure`

### `/api/v1/tx/hns+redeeming`

### `/api/v1/tx/bid+reclaiming`

### DNS reference update