from pydantic import compiled
from solcx import compile_standard
import json
from web3 import Web3 

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    
# Compiling the solidity code and writing it to a file
compiled_sol = compile_standard(
    {
        "language" : "Solidity",
        "sources" : {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings" : {
            "outputSelection" : {
                "*" : {
                    "*" : ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Extracting the bytecode & abi from compiled_code.json
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connecting to Ganache-cli RPC server using web3
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Connecting to Infura server using web3
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/c5c68137b3494a31bd84635d2826ea60"))
chain_id = 4 # Rinkeby testnet chain ID, from https://chainlist.org/
# choosing a random address & its private key from the given addresses in Ganache
my_address = "0x20A6E1Aca89C4F788dE0922B29d43B1374aD0e91" # Metamask account ID
private_key = "0x1b42dc42988d333c2d664d9d8558baff6fd60a6581d17ad28c2e06fbc80ff361"
print("Connected to Infura network...")
# Creating a contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the nonce (number of transactions by the account)
nonce = w3.eth.getTransactionCount(my_address)

# Three steps to make a transaction
# 1. Create a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId":chain_id, 
        "gasPrice": w3.eth.gas_price,
        "from":my_address, 
        "nonce":nonce
    }
)

# 2. Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# 3. Send the transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Total gas used: ", (tx_receipt.gasUsed * tx_receipt.effectiveGasPrice) / 10 ** 18, " Ether")

# Now we will work with the deployed contract. We need: contract address & contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("Stored value: ", simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(999999).buildTransaction(
    {
        "chainId":chain_id, 
        "gasPrice": w3.eth.gas_price,
        "from":my_address, 
        "nonce":nonce+1
    }
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
print("Changing the value to 999999")
print("Updating contract...")
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Total gas used: ", (tx_receipt.gasUsed * tx_receipt.effectiveGasPrice) / 10 ** 18, " Ether")
print("Contract updated!")
print("Stored value: ",simple_storage.functions.retrieve().call(), " (Updated)")