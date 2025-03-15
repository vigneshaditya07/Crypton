from Crypto.Hash import SHA256
from node.blockchain.transaction import Transaction
from typing import List
import pickle

class Block:
    """
    Attributes :-

    transactions : list of all transactions in the block
    hash         : hash value of the block
    prev_hash    : hash value of the previous block
    nonce        : nonce value of the block
    block_height : height of the block in the chain

    Methods :-

    add_transaction(transaction : Transaction) -> None               : adds the given transaction to the block(does not validate)
    find_transactions_by_address(address : str) -> List[Transaction] : returns all the transactions that involve the given address
    set_nonce(nonce : int) -> None                                   : sets the nonce value of the block
    set_prev_hash(prev_hash : str) -> None                           : sets the prev_hash value(hash of the previous block)
    update_hash() -> None                                            : updates hash of the block
    change_height(height : int) -> None                              : sets the height value of the block(block_height)
    toJSON() -> JSON                                                 : returns the block in json format
    
    """
    def __init__(self,transactions : List[Transaction]=[],prev_hash : str = '') -> None:
        self.transactions=transactions
        self.hash=''
        self.prev_hash=prev_hash
        self.nonce=0
        self.block_height=0
        self.update_hash()

    def add_transaction(self,transaction : Transaction) -> None:
        """adds the transaction to the list of transactions"""
        self.transactions.append(transaction)
        self.update_hash()

    def add_transactions(self,transactions):
        self.transactions.extend(transactions)
        self.update_hash()

    def find_transaction_by_txid(self,txid : str) -> Transaction:
        """returns the transaction with the given id"""
        for transaction in self.transactions:
            if (transaction.txid == txid):
                return transaction
        return None

    def set_nonce(self,nonce : int) -> None:
        """sets the nonce value"""
        self.nonce=nonce
        self.update_hash()

    def set_prev_hash(self,prev_hash : str) -> None:
        """sets the prev_hash value(hash of the previous block)"""
        self.prev_hash=prev_hash
        self.update_hash()
    
    def update_hash(self) -> None:
        """calculate hash of the block"""
        hash = SHA256.new(data=self.prev_hash.encode())
        for transaction in self.transactions:
            hash.update(pickle.dumps(transaction))
        hash.update(str(self.nonce).encode())
        self.hash=hash.hexdigest()

    def return_hash(self):
        """returns hash of the block"""
        hash = SHA256.new(data=self.prev_hash.encode())
        for transaction in self.transactions:
            hash.update(pickle.dumps(transaction))
        hash.update(str(self.nonce).encode())
        return hash.hexdigest()

    def set_height(self,height : int) -> None:
        """sets the height of the block"""
        self.block_height=height

    def toJSON(self):
        """{
            block_height : ....
            prev_hash : ....
            nonce : ....
            hash : ....
            transactions : ....
        }"""
        blockjson = {"block_height":self.block_height,"prev_hash":self.prev_hash,
        "nonce" : self.nonce,"hash":self.hash,"transactions" : [t.toJSON() for t in self.transactions] }
        return blockjson

    @classmethod
    def fromJSON(cls,json):
        block= cls([Transaction.fromJSON(transaction) for transaction in json["transactions"]],json["prev_hash"])
        block.set_nonce(json["nonce"])
        block.set_height(json["block_height"])
        block.update_hash()
        return block

    def  pprint(self):
        print("Block : ",self.block_height)
        print("Hash : ",self.hash)
        print("Previous Hash : ",self.prev_hash)
        print("Nonce : ",self.nonce)
        print("------------------")
        for tx in self.transactions:
            tx.pprint()
        print('------------------')

def verify_block(block,tx_verifier,hash:str='',prev_hash:str='') -> bool: 
    if (block.prev_hash!= prev_hash):
        return False
    if(block.hash!=hash):
        return False
    coinbase = block.transactions[0]
    if(coinbase.output_count!=1):
        return False
    if(coinbase.outputs[0].amount!=50):
        return False
    for transaction in block.transactions[1:]:
        if(transaction.return_hash()!= transaction.txid):
            return False
        if(tx_verifier.verify_transaction(transaction) != True):
            return False

    return True


def mineblock(block,d=4):
    t=0
    while True:
        block.set_nonce(t)
        if(block.hash.startswith('0'*d)):
            break
        t+=1
    return