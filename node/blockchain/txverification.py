from node.blockchain.block import Block
from node.blockchain.txverificationengine import tx_verification_engine
from typing import List
from node.blockchain.transaction import Transaction, TransactionOutput

class Utxo_pool:
    def __init__(self,utxo_collection) -> None:
        self.utxo_pool= utxo_collection

    def get_utxo_by_id(self,utxo_id:str) -> Transaction:
        utxo=self.utxo_pool.find_one({"utxo_id":utxo_id})
        return utxo

    def utxo_id(self,txid:str,outindex:int) -> str:
        utxo_id=txid + '_' + str(outindex)
        return utxo_id

    def construct_utxopool(self,blockchain):
        self.utxo_pool.remove({})
        for blockjson in blockchain.blocks_cursor():
            block=Block.fromJSON(blockjson)
            self.update_utxopool(block)
                    

    def update_utxopool(self,block):
        if(isinstance(block,dict)):
            block = Block.fromJSON(block)
        for transaction in block.transactions:
            for i,txoutput in enumerate(transaction.outputs):
                utxo_id=self.utxo_id(transaction.txid,i)
                utxo_script = txoutput.lock_script
                utxo_amt = txoutput.amount
                utxo ={"utxo_id":utxo_id,"lock_script":utxo_script,"amount":utxo_amt}
                utxo["addresses"]=addresses_from_lockscript(utxo_script)
                self.utxo_pool.insert_one(utxo)

            for i,txinput in enumerate(transaction.inputs):
                inputid=txinput.tx_pointer + '_' + str(txinput.output_index)
                self.utxo_pool.delete_one({"utxo_id":inputid})


    def get_utxos_by_address(self,address):
        utxos=[]
        for utxo in self.utxo_pool.find({},{'_id':False}):
            if address in utxo["addresses"]:
                utxos.append(utxo)

        return utxos

    def pprint(self):
        print('----------------------------------------------------------------')
        for data in self.utxo_pool.find():
            print(data["addresses"]," : ",data["amount"])
        print('----------------------------------------------------------------')

    
class Tx_verifier:
    def __init__(self,utxo_pool) -> None:
        self.utxo_pool = utxo_pool

    def verify_transaction(self,transaction : Transaction):
        total_input_amount,total_output_amount= 0,0
        for input in transaction.inputs:
            utxo_id=input.tx_pointer + '_' + str(input.output_index)
            utxo = self.utxo_pool.get_utxo_by_id(utxo_id)
            if utxo==None:
                return False
            utxo = TransactionOutput.fromJSON(utxo)
            verification_engine=tx_verification_engine(input.unlock_script,utxo.lock_script,transaction.to_str())
            valid=verification_engine.verify_transaction()
            if valid:
                total_input_amount+=utxo.amount
            else:
                return False

        for output in transaction.outputs:
            if(not isinstance(output.amount,int)):
                return False
            total_output_amount+=output.amount

        if(total_output_amount <= total_input_amount):
            return True
        else:
            return False

def addresses_from_lockscript(lockscript):
    addresses=[]
    addresses.append(lockscript.split()[2][1:-1])
    return addresses
