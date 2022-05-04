from turtle import update
from brownie import accounts # This is list of 10 Ganache accounts spawned by brownie
from brownie import config # This connects to our brownie-config.yaml file
from brownie import network # Brownie has a list of networks. Check 'brownie networks list'
from brownie import SimpleStorage # Importing our contract, this is a list of contract objects

import os 

def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("anonmak")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])
    
    # We deploy the contract. (type: transact). This will return a contract object
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)

    transaction = simple_storage.store(1234, {"from": account})

    transaction.wait(1)

    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)

# Check if --network is included in brownie run deploy.py
def get_account():
    if(network.show_active()=="development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()