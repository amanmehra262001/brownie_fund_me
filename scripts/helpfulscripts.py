from brownie import network, accounts, config, MockV3Aggregator

# from web3 import Web3

DECIMAL = 8
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]


def getaccounts():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks.......")
    if len(MockV3Aggregator) <= 0:
        print("Deploying new mock.................")
        MockV3Aggregator.deploy(DECIMAL, STARTING_PRICE, {"from": getaccounts()})
    print("Mocks deployed")
