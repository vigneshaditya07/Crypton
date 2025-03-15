import requests
from transaction import Transaction, TransactionInput, TransactionOutput
from typing import List,Tuple, Union
from Crypto.Hash import SHA256
from Crypto.Hash import RIPEMD160
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import base58
import pickle

# 1 coin = 10000 units

class WalletData:
    def __init__(self,username='',pwdhash='') -> None:
        self.username = username
        self.password = pwdhash
        self.keys=[]
        self.addrskeymap={}
        self.addresses=[]
        self.contacts=[]
        self.balance = 0
        self.spent = 0
        self.received = 0
        self.tx_history=[]
        self.recent_txs=[]
        self.nodeip=''
        

    def __getstate__(self):
        keys = self.keys
        self.keys = [ k.d for k in self.keys ]
        self.addrskeymap = {}
        state = self.__dict__
        self.keys = keys
        self.update_addrskeymap()
        return state

    def __setstate__(self,state):
        self.__dict__ = state
        self.keys = [ ECC.construct(curve='P-256',d=x) for x in self.keys ]
        self.update_addrskeymap()

    def save_data(self):
        with open("walletdata/"+self.username,'w') as f:
            b=pickle.dumps(self)

    def update_addrskeymap(self):
        self.addrskeymap={ Wallet.address_of(k):k for k in self.keys }

    def update_addresses(self):
        self.addresses=[Wallet.address_of(k) for k in self.keys]

    def add_key(self,key):
        self.keys.append(key)
        self.update_addresses()
        self.update_addrskeymap()

    def calculate_balance(self):
        balance=0
        for my_address in self.addresses:
            r= requests.get('http://'+ self.nodeip +'/get_utxos',params={'address':my_address})
            utxosJSON = r.json()
            for i in utxosJSON:
                utxo = utxosJSON[i]
                balance+=utxo['amount']

        self.balance=balance
        return self.balance

    def add_recent_tx(self,tx):
        self.recent_txs.append(tx)

    def add_contact(self,contact):
        self.contacts.append(contact)

class Wallet:
    def __init__(self,walletdata:WalletData) -> None:
        self.walletdata = walletdata

    @staticmethod
    def address_of(key:ECC.EccKey) -> str:
        cmprssed=Wallet.compress_publickey(key)
        address = Wallet.generate_address(cmprssed)
        return address

    @staticmethod
    def generate_address(publickey:str) -> str:
        shahash = SHA256.new(publickey.encode())
        ripehash = RIPEMD160.new(shahash.digest())
        address = base58.b58encode_check(ripehash.digest())
        return address.decode()

    @staticmethod
    def generate_lock_script(script_type :str,data : List) -> str:
        """generates the lock script. data is list of either addresse or keys"""
        if(script_type=='P2PH'):
            if(isinstance(data[0],ECC.EccKey)):
                cmprsspk= Wallet.compress_publickey(data[0])
                addrs= Wallet.generate_address(cmprsspk) 
            elif(isinstance(data[0],str)):
                addrs=data[0]
            addrs =addrs
            lock_script="op_dup op_addr <{address}> op_equalverify op_checksig".format(address=addrs)
            return lock_script
        elif (script_type=='P2PK'):
            pass
        elif (script_type=='MULTISIG'):
            pass

    @staticmethod
    def generate_unlock_script(script_type :str,signature_str:str,publickeys:List[ECC.EccKey]) -> str:
        """generates the unlock script"""
        if(script_type=='P2PH' or script_type=='P2Pk'):
            unlock_script = "{signature} <{compressed_publickey}>"
            signer = DSS.new(publickeys[0],'fips-186-3')
            h = SHA256.new(signature_str.encode())
            signature = signer.sign(h)
            signature = signature.hex()
            cmprssedkey=Wallet.compress_publickey(publickeys[0])
            unlock_script = unlock_script.format(signature=signature,compressed_publickey = cmprssedkey)
            return unlock_script


    @staticmethod
    def generate_ECC_key(private_key :int = None) -> ECC.EccKey:
        if(private_key == None):
            return ECC.generate(curve='P-256')
        try:    
            key = ECC.construct(curve='P-256',d=private_key)
            return key
        except ValueError:
            return None

    @staticmethod
    def load_privatekey():
        pass

    @staticmethod
    def compress_publickey(publickey:ECC.EccKey) -> str:
        x,y=publickey.pointQ.xy
        cmprssdkey = ''
        if(y%2==0):
            cmprssdkey+='0'
        else:
            cmprssdkey+='1'

        cmprssdkey+= (hex(x)[2:])
        return cmprssdkey

    @staticmethod
    def create_P2PH_transaction(inputs,change_address:Union[ECC.EccKey,str],payto_address:Union[ECC.EccKey,str],amount:Tuple[int,int]) -> Transaction:
        # inputs:=[(key,inputstr),(key2,inputstr2),..]               amount:=(sendamount,changeamount)
        #tx input generation
        tx_inputs=[]
        for input in inputs:
            tx_pointer,output_index = input[1].split(sep='_')  # inputstr = txpointer_outputindex
            txinput=TransactionInput(tx_pointer,int(output_index))
            tx_inputs.append(txinput)
        #tx output generation
        lock_script=Wallet.generate_lock_script('P2PH',[payto_address])
        txoutput=TransactionOutput(amount[0],lock_script)

        #change output
        if(amount[1]!=0):
            lock_script2=Wallet.generate_lock_script('P2PH',[change_address])
            change_output=TransactionOutput(amount[1],lock_script2)
            transaction = Transaction(tx_inputs,[txoutput,change_output])
        else:
            transaction = Transaction(tx_inputs,[txoutput])

        #signature
        sig_str = transaction.to_str()

        for i,input in enumerate(inputs):
            unlock_script=Wallet.generate_unlock_script('P2PH',sig_str,[input[0]])
            transaction.inputs[i].set_unlock_script(unlock_script)
        
        return transaction

    @staticmethod
    def create_coinbase(address:Union[ECC.EccKey,str],block_height=0,reward=50*10000) ->Transaction:
        tx_input=TransactionInput('Coinbase'+str(block_height),0,'')
        lock_script=Wallet.generate_lock_script('P2PH',[address])
        tx_output = TransactionOutput(reward,lock_script)
        coinbase_tx=Transaction([tx_input],[tx_output])
        return coinbase_tx


    def key_of(self,address):
        return self.walletdata.addrskeymap[address]


    def pay(self,address:Union[ECC.EccKey,str],payamount):
        if(not isinstance(payamount,int)):
            return False
        available_utxos= []
        balance=0
        for my_address in self.walletdata.addresses:
            r= requests.get('http://'+ self.walletdata.nodeip + '/get_utxos',params={'address':my_address})
            utxosJSON = r.json()
            for i in utxosJSON:
                utxo = utxosJSON[i]
                available_utxos.append(utxo)
                balance+=utxo['amount']
                
        if(balance < payamount):
            return False

        available_utxos.sort(key=lambda item:item['amount'])

        pay=0
        inputs=[]
        amount=(0,0)
        for utxo in available_utxos:
            utxoamount = utxo['amount']
            pay += utxoamount
            key=self.key_of(utxo['addresses'][0])
            input_str=utxo['utxo_id']
            inputs.append((key,input_str))
            if pay>=payamount:
                amount=(payamount,pay-payamount)
                break
        
        tx=Wallet.create_P2PH_transaction(inputs,inputs[-1][0],address,amount)
        txjson = tx.toJSON()
        r=requests.post('http://'+ self.walletdata.nodeip + '/add_transaction',json=txjson)
        return True