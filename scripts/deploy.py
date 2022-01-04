from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helpfulscripts import getaccounts, deploy_mocks, LOCAL_BLOCKCHAIN_ENV


def deploy_fund_me():
    account = getaccounts()
    # print(network.show_active())
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        # print(price_feed_address)
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
