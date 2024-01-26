## The Auction Journey of an HNS Token
1. Someone wants a domain name, like `treehouse.cardano`
2. If the desired domain name does not exist, anyone can initialize an auction for that HNS token. When the auction is initialized, the HNS token is minted and locked at the Auction UTxO at the Auction Validator.
   - (Optional) At the same time that HNS Token is minted and Auction is initialized, the person who initiated the auction can optionally set the `purchaseAmount`, which is essentially a minimum bid amount. The minimum `purchaseAmount` is a parameter of the auction, but the initializer can set it higher than the minimum. Once a `purchaseAmount` is set, every bid must be greater than this amount.
   - The initializer locks the `purchaseAmount` at the auction at this step.
3. An Auction Might Happen - if other people choose to bid on the HNS Token. When someone else places a bid:
   - For each bidder (on each HNS token), a MHABAT token is minted
   - The bid (effectively) must be greater than the `purchaseAmount`: this is not checked by the validator...so our Front End might prevent lower bids
   - When a new bidder joins an Auction, they must submit the Seat Cost + Bid Cost
   - When a new bidder places a Bid, they submit their bid and a secret (Salt) -- look at ways to generate this secret salt.
4. Bidders can update their bid amount. The only cost is a Cardano Tx fee. As a bidder, I must update my bid from the same wallet that I used to join the Auction in Step 3.
5. Bidding window closes. Now it's Bid Disclosure time - where Bidders reveal their bids.
   - Each Bidder has the chance to reveal their bid, iff their bid is greater than the current highest revealed bid.
   - Bid Disclosure window lasts for specified amount of time (1 week? 2 weeks?)
6. Bid Disclosure Window closes. Claim winder opens. (This window stays open indefinitely)
   - Everyone who did not place the highest bid reclaims their seat cost.
   - When seat cost is reclaimed, MHABAT token is burned.
   - In order to reveal a bid, the revealer must deposit their bid amount. When this happens, the previous highest revealed bid is sent back to the wallet from which that bid was placed/revealed.
7. Winner claims the HNS Token
   - The winner is the bidder who revealed the highest bid.
   - When the HNS Token is claimed, the `DRAT` token is minted to the DNS Reference Validator, with "un-initialized" `DNSReferenceDatum`. In this datum, the `origin` matches the token name (which is the same for the HNS Token and DRAT Token). But the `dnsRecords` is an empty list, and `additionalData` is `Nothing`.
   - The `DNSReferenceDatum` must be inline datum. (validator checks for this)
   - The HNS Token is sent to the wallet of the winner. (validator checks that HNS token can only be sent to winner)
   - The winner's revealed bid (see Step 6) is sent to the Main Treasury.

## At this Point: The HNS Token Has an Owner!
So what can the owner do?
- Owner of an HNS Token can configure the Datum in the `DRAT` Token UTxO.