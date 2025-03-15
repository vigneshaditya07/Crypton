from typing import List
from Crypto.Hash import SHA256


class TransactionInput:
    def __init__(self,tx_pointer : str ='',output_index : int =0,unlock_script : str ='') -> None:
        self.tx_pointer = tx_pointer
        self.output_index = output_index
        self.unlock_script = unlock_script

    def set_unlock_script(self,unlock_script:str):
        self.unlock_script = unlock_script

    def toJSON(self):
        """{
            tx_pointer : ....
            output_index : ....
            unlock_script : ....
        }"""
        tinpjson = {"tx_pointer":self.tx_pointer,"output_index":self.output_index,"unlock_script":self.unlock_script}
        return tinpjson
    @classmethod
    def fromJSON(cls,json):
        Txi = cls(json["tx_pointer"],json["output_index"],json["unlock_script"])
        return Txi

    def to_str(self):
        ti_str = self.tx_pointer + str(self.output_index)
        return ti_str

    def pprint(self):
        print("    "+self.tx_pointer+'_'+str(self.output_index))


class TransactionOutput:
    def __init__(self,amount : int=0,lock_script : str='') -> None:
        self.amount = amount
        self.lock_script = lock_script

    def to_str(self):
        to_str = str(self.amount) + self.lock_script
        return to_str

    def pprint(self):
        print("    "+self.lock_script.split()[2]," ",self.amount)

    def toJSON(self):
        """{
            amount : ...
            lock_script : ...
        }"""
        totjson={"amount":self.amount,"lock_script":self.lock_script}
        return totjson

    @classmethod
    def fromJSON(cls,json):
        Txo=cls(json["amount"],json["lock_script"])
        return Txo


class Transaction:
    def __init__(self,inputs : List[TransactionInput],outputs : List[TransactionOutput]) -> None:
        self.txid = ''
        self.inputs = inputs
        self.input_count = len(inputs)
        self.outputs = outputs
        self.output_count = len(outputs)
        self.update_txid()

    def to_str(self) -> str:
        """Converts the transaction details to str for hashing """
        tx_str=''
        tx_str += str(self.input_count)
        for input in self.inputs:
            tx_str += input.to_str()
        tx_str += str(self.output_count)
        for output in self.outputs:
            tx_str += output.to_str()

        return tx_str

    def pprint(self):

        print("                 ~~~~~~~~")
        print("txid : ",self.txid)
        print("  Input :-")
        for inp in self.inputs:
            inp.pprint()
        print("  Outputs :-")
        for out in self.outputs:
            out.pprint()
        print("                 ~~~~~~~~")


    def update_txid(self):
        """Calculates the hash and sets it as txid"""
        hash = SHA256.new(data=self.to_str().encode())
        self.txid = hash.hexdigest()

    def return_hash(self):
        hash = SHA256.new(data=self.to_str().encode())
        return hash.hexdigest()

    def toJSON(self):
        """{
            txid : ....
            inputs : [....]
            outputs : [....]
        }"""
        txjson= {"txid":self.txid,"inputs":[inp.toJSON() for inp in self.inputs],"outputs":[out.toJSON() for out in self.outputs]}
        return txjson

    @classmethod
    def fromJSON(cls,json):
        inputs = [TransactionInput.fromJSON(Txi) for Txi in json["inputs"]]
        outputs = [TransactionOutput.fromJSON(Txo) for Txo in json["outputs"]]
        transaction = cls(inputs,outputs)
        return transaction





