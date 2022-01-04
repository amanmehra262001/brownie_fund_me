from scripts.helpfulscripts import LOCAL_BLOCKCHAIN_ENV, getaccounts
from scripts.deploy import deploy_fund_me
import pytest
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    account = getaccounts()
    fund_me = deploy_fund_me()
    # print("fund me deployed")
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFund(account.address) == entrance_fee
    tx2 = fund_me.withDraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFund(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # fund_me.withDraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withDraw({"from": bad_actor})
