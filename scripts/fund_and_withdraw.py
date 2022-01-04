from brownie import FundMe
from scripts.helpfulscripts import getaccounts


def fund():
    fund_me = FundMe[-1]
    account = getaccounts()
    entrance_fee = fund_me.getEntranceFee()
    print(f"entry fee is {entrance_fee}")
    print("Funding............")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = getaccounts()
    fund_me.withDraw({"from": account})


def main():
    fund()
    withdraw()
