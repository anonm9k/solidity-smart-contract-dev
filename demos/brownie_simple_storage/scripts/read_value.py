from brownie import accounts # This is list of 10 Ganache accounts spawned by brownie
from brownie import config # This connects to our brownie-config.yaml file
from brownie import SimpleStorage # Importing our contract, this is a list of contract objects

def read_contract():
    simple_storage = SimpleStorage[-1] # -1 to get the most recent deployment
    print(simple_storage.retrieve())

def main():
    read_contract()