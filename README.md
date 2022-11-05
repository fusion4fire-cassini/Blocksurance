# Blocksurance
__Example usage:__ Tom might want to insure the plot of land where his country house is located. As it is in the south of italy near a forest he fears that a fire might burn it down. So Tom will contract a policy with Fusion4Fire for 90 days since 1st of June to the end of August. Then he pays a determined amount depending on the risk and he recieves some tokens that he can use to get his money back in the case of a fire. If no fire has started in the 90 days that he has contracted, the token will expire and if he wished to reinsure his land, he would start the process again.

## Smart contract functionality
The smart contract holds a pool of capital that comes from three different activities:
- __Insurance of plots of land:__ The policyholder will deposit a fixed amount in the pool to insure a plot of land. In case of fire the agreed amount of money would be taken out of the pool to cover the incident
- __Investment from individuals or institutions:__ Interested parties can invest money into the pool assuming it will grow in value from the others activities. In exchange for this return, they help increase the total coverage avalaible for policyholders in case of incident.
- __Usage of the pools money(forestry, lending,...):__ The pools money can be used for financing activities that reduce the risk of wildfires, mainly in insured areas. Other possible uses of the money are lending the money to interested parties, one possibility is to some decentralized lending blockchain platforms.
 
### Policyholders
The smart contract allows for the creation of a token that tracks an insurance policy contracted by the policyholder associated to a plot of land for a chosen period of time. This allows him to exchange the token for a predetermined amount of money in case a fire occurs in his property(parametric insurance).

For minting a determined amount of tokens you need to call:
```
function mintInsured(address receiver, uint amount, uint timeFrame) public
```
Where:
- _receiver_ specifies the address where the policyholder wants to save the token.
- _amount_ specifies the number of tokens to be minted.
- _timeFrame_ specifies the length of the contract in number of seconds since the moment of minting.

For claiming the money from a set of tokens you need to call:
```
function ClaimInsured(address receiver) public
```
Where:
- _receiver_ specifies the address where the policyholder wants to save the token

## Investors
