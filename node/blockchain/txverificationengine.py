from collections import deque
from Crypto.Hash import SHA256,RIPEMD160
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import base58

class InvalidTransaction(Exception):
    pass

class StackMachine:
    def __init__(self) -> None:
        self.stack = deque()
        self.instruction_pointer = 0
        self.instructions = []
        self.dispatch_map = {}

    def pop(self):
        return self.stack.pop()
    def push(self,value):
        self.stack.append(value)
    def peek(self):
        return self.stack[-1]
    def next_instruction(self):
        self.instruction_pointer+=1
    def exit(self):
        raise InvalidTransaction("Script forcefully exited")

    def dispatch(self,op_code):
        if op_code in self.dispatch_map:
            self.dispatch_map[op_code]()
        elif op_code[0]=='<' and op_code[-1] == '>':
            self.push(op_code[1:-1].encode())
        else:
            self.push(bytes.fromhex(op_code))

    def run(self):
        while self.instruction_pointer < len(self.instructions):
            op_code = self.instructions[self.instruction_pointer]
            self.dispatch(op_code)
            self.next_instruction()

class tx_verification_engine(StackMachine):
    def __init__(self,unlock_script:str,lock_script:str,signature_str:str='') -> None:
        super().__init__()
        self.dispatch_map = {
            'op_equal' : self.equal,
            'op_verify' : self.verify,
            'op_equalverify' : self.equal_verify,
            'op_dup' : self.dup,
            'op_sha256' : self.sha256,
            'op_ripemd160' : self.ripemd160,
            'op_hash160' : self.hash160,
            'op_base58' : self.base58_checksum,
            'op_addr' : self.addr,
            'op_checksig' : self.checksig,
            'op_checksigverify' : self.checksigverify,
            'op_checkmultisig' : self.checkmultisig
        }
        self.unlock_script = unlock_script.split()
        self.lock_script = lock_script.split()
        self.signature_str = signature_str
    
    def verify_transaction(self):
        instructions=self.unlock_script + self.lock_script
        self.instructions = instructions
        try:
            self.run()
        except Exception as error:
            print(error)
            return False
            #self.exit()
        if(len(self.stack)==1 and self.stack[0]==True):
            return True
        else:
            return False

    def load_public_key(self,x):
        xs=x.decode()
        sign=int(xs[0])
        x=int(xs[1:],16)
        prime=115792089210356248762697446949407573530086143415290314195533631308867097853951
        b=41058363725152142129326129780047268409114441015993725554835256314039467401291
        y=pow(((x**3) - (3*x) + b),28948022302589062190674361737351893382521535853822578548883407827216774463488,prime)
        if(y % 2 != sign):
            y=prime-y
        key=ECC.construct(curve='P-256',point_x=x,point_y=y)
        return key

    def equal(self):
        self.push(self.pop()==self.pop())

    def verify(self):
        if(not self.pop()):
            self.exit()

    def dup(self):
        self.push(self.peek())

    def sha256(self):
        hash=SHA256.new(data=self.pop())
        self.push(hash.digest())
    
    def equal_verify(self):
        self.equal()
        self.verify()

    def ripemd160(self):
        hash=RIPEMD160.new(data=self.pop())
        self.push(hash.digest())
    
    def hash160(self):
        self.sha256()
        self.ripemd160()

    def base58_checksum(self):
        b58=base58.b58encode_check(self.pop())
        self.push(b58)

    def addr(self):
        self.hash160()
        self.base58_checksum()

    def checksig(self):
        key = self.load_public_key(self.pop())
        hash = SHA256.new(self.signature_str.encode())
        sig_verifier = DSS.new(key,'fips-186-3')
        try:
            sig_verifier.verify(hash,self.pop())
            self.push(True)
        except ValueError as error:
            print(error)
            self.push(False)

    def checksigverify(self):
        self.checksig()
        self.verify()

    def checkmultisig(self):
        no_publickeys = int.from_bytes(self.pop(),'big')
        publickeys = []
        for i in range(no_publickeys):
            publickeys.append(self.load_public_key(self.pop()))
        threshold = int.from_bytes(self.pop(),'big')
        valid_signatures = 0
        hash = SHA256.new(self.signature_str.encode())
        for publickey in publickeys:
            sig_verifier = DSS.new(publickey,'fips-186-3')
            try:
                sig_verifier.verify(hash,self.peek())
                self.pop()
                valid_signatures+=1
                if threshold==valid_signatures:
                    self.push(True)
                    break
            except ValueError as error:
                print(error)
        if threshold!=valid_signatures:
            self.push(False)

