from brownie import FundMe
from brownie import MockV3Aggregator # List of MockV3Aggregators
from brownie import network # Brownie has a list of networks. Check 'brownie networks list'
from brownie import accounts # This is list of 10 Ganache accounts spawned by brownie
from brownie import config # This connects to our brownie-config.yaml file
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-l"]

def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print("Current network: ", network.show_active())
    else:
        print(f"Current network: {network.show_active()}")
        if len(MockV3Aggregator) <= 0:
            print("Deploying Mock...")
            MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from":account})
            print("Mock deployed...")

        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
            price_feed_address,
            {"from": account}, 
            publish_source=config["networks"][network.show_active()].get("verify")
        )
    print(f'FundMe deployed at address: {fund_me.address}')
    return fund_me

def main():
    deploy_fund_me()

# Check if --network is included in brownie run deploy.py
def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    