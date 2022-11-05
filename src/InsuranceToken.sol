pragma solidity >=0.7.0 <0.9.0;
// SPDX-License-Identifier: UNLICENSED

contract InsuranceToken{
    
    struct InsuredContract {
        uint quantity;
        uint expires;
    }
    address public minter;
    uint rateInvestor = 1;
    uint rateInsured = 10;
    mapping (address => uint) public balancesInvestor;
    mapping (address => InsuredContract) public balancesInsured;

    constructor() {
        minter = msg.sender;
    }

    // Sends an amount of newly created coins to an address
    // Can only be called by the contract creator
    function mintInvestor(address receiver, uint amount) public {
        //require(msg.sender == minter);
        balancesInvestor[receiver] += amount;
    }
    
    // timeFrame: number of seconds until the insurance contract expires
    function mintInsured(address receiver, uint amount, uint timeFrame) public {
        //require(msg.sender == minter);
        balancesInsured[receiver] = InsuredContract(amount, block.timestamp+timeFrame);
    }

    error InsufficientBalance(uint requested, uint available);

    // An investor sends 'amount' of tokens and gets back the 'amount'*rate
    function ClaimInvestor(address receiver, uint amount) public {
        //require(msg.sender == minter);

        if (amount*rateInvestor > address(this).balance) {
            revert InsufficientBalance({
                requested: amount*rateInvestor,
                available: address(this).balance
            });
        } else {
            if (amount >= balancesInvestor[receiver]) {
                payable(receiver).transfer(amount*rateInvestor);
                balancesInvestor[receiver] -= amount;
            } else {
                 revert InsufficientBalance({
                    requested: amount,
                    available: balancesInvestor[receiver]
                });
            }
        }
        
    }

     // An investor sends 'amount' of tokens and gets back the 'amount'*rate
    function ClaimInsured(address receiver) public {
        //require(msg.sender == minter);
        uint bInsured = balancesInsured[receiver].quantity;
        if (address(this).balance >= bInsured*rateInsured &&
                block.timestamp < balancesInsured[receiver].expires) {
            payable(receiver).transfer(rateInsured*bInsured);
            balancesInsured[receiver].quantity = 0;
        }
    }

    function getBalanceInvestor(address account) public view returns(uint) {
        return uint(balancesInvestor[account]);
    }

    // Sends an amount of existing tokens
    // from any caller to an address
    function send(address receiver, uint amount) public {
        if (amount > balancesInvestor[msg.sender])
            revert InsufficientBalance({
                requested: amount,
                available: balancesInvestor[msg.sender]
            });

        balancesInvestor[msg.sender] -= amount;
        balancesInvestor[receiver] += amount;
    }
}
