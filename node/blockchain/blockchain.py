from node.blockchain.block import Block, verify_block
from typing import List

class BlockChain:
    """
    Attributes :-

    blocks       : list of blocks
    block_length : length of the blockchain

    Methods :-

    get_length() -> int                                        : returns the length of the block chain
    add_blockJSON() -> bool                                    : adds the given blockJSON(internally calls _add_block)
    _add_block(block :Block) -> None                           : adds the given block to the block chain 
    remove_block_from(length : int) -> None                    : removes all the blocks after the given length
    update_length() -> None                                    : updates the length of the blockchain
    validate_block(remove_invalid : bool = False) -> bool      : returns true if the blockchain is valid. If remove_valid is set
                                                               ~ as True removes all the invalid blocks
    print_block_chain() -> None                                : prints the blockchain
    
    """
    def __init__(self,bkcollection) -> None: 
        self.bkcollection = bkcollection
        self.block_length = self.bkcollection.count_documents({})

    def get_length(self) -> int:
        """returns the length of the blockchain"""
        return self.block_length

    def get_lastblock(self):
        last_block=self.get_block(self.block_length-1)
        return last_block

    def add_blockJSON(self,blockjson,tx_verifier):
        last_block=self.get_lastblock()
        prev_hash=last_block.hash
        print(prev_hash)
        hash=blockjson["hash"]
        block= Block.fromJSON(blockjson)
        valid = verify_block(block,tx_verifier,hash,prev_hash)
        if valid:
            try:
                self._add_block(block)
                return True
            except:
                print('Not valid')
                return False
        else:
            return False

    def _add_block(self,block :Block) -> None:
        """adds the block to the chain"""
        block.set_height(self.block_length)
        print(block.toJSON())
        self.bkcollection.insert_one(block.toJSON())
        self.update_length()

    def remove_block_from(self,length : int) -> None:
        """removes all the blocks after the given length"""
        if(length>self.block_length):
            return
        query = {"block_height" : {"$gt":length-1}}
        self.bkcollection.delete_many(query)
        self.update_length()


    def update_length(self) -> None:
        """updates the length of the blockchain"""
        self.block_length = self.bkcollection.count_documents({})

    def get_block(self,block_height:int):
        blockjson = self.bkcollection.find_one({"block_height":block_height})
        if blockjson:
            block = Block.fromJSON(blockjson)
            return block
        else:
            return None

    def blocks_cursor(self):
        return self.bkcollection.find()

    def validate_block_chain(self,tx_verifier,remove_invalid : bool = False) -> bool:
        """validates the blockchain and removes invalid blocks"""
        block_cursor = self.bkcollection.find()
        prev_hash = "000085b508a925316f11583cfee32b65e0e56ec1049765d8f9563b124a49b89b"
        block_cursor.next()
        for blockjson in block_cursor:
            block=Block.fromJSON(blockjson)
            blockvalid=verify_block(block,tx_verifier,blockjson["hash"],prev_hash)
            if(blockvalid==False):
                return False
            prev_hash=block.hash 