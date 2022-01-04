// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;
    mapping(address => uint256) public addressToAmountFund;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public pricefeed;

    constructor(address _pricefeed) public {
        pricefeed = AggregatorV3Interface(_pricefeed);
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minUSD = 50 * 10**18;
        // if(msg.value < minUSD){
        //     revert?
        // }

        require(
            getConversionRate(msg.value) >= minUSD,
            "You need to spend ETH worth atleast 50 USD"
        );
        addressToAmountFund[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return pricefeed.version();
    }

    function getPrice() public view returns (uint256) {
        // (uint80 roundId,
        // int256 answer,
        // uint256 startedAt,
        // uint256 updatedAt,
        // uint80 answeredInRound
        // ) =pricefeed.latestRoundData();
        (, int256 answer, , , ) = pricefeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethprice = getPrice();
        uint256 ethInUSD = (ethprice * ethAmount) / 1000000000000000000;
        return ethInUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier OnlyOwner() {
        require(msg.sender == owner, "Only owners can withdraw");
        _;
    }

    function withDraw() public payable OnlyOwner {
        msg.sender.transfer(address(this).balance);
        for (uint256 fIndex = 0; fIndex < funders.length; fIndex++) {
            address funder = funders[fIndex];
            addressToAmountFund[funder] = 0;
        }
        funders = new address[](0);
    }
}
