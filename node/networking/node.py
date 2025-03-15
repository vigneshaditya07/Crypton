from walletapp.wallet import Wallet
from node.blockchain.block import Block, mineblock
import threading
import time
from node.blockchain.txverification import Tx_verifier

from node.networking.app import flask_app
import requests
from concurrent.futures import ThreadPoolExecutor

class NodeRequests:

    def __init__(self,timeout=5,port=5000) -> None:
        self.timeout = timeout
        self.port = port

    def get_nodes(self,ip):
        url = 'http://' + ip + '/get_nodes'
        try:
            r=requests.get(url,timeout=self.timeout)
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

    def heartbeat(self,ip):
        url = 'http://' + ip + '/heartbeat'
        try:
            r=requests.get(url,timeout=0.1)
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

    def transmit_block(self,ip,blockjson):
        url = 'http://' + ip + '/new_block'
        try:
            r=requests.post(url,timeout=self.timeout,json=blockjson)
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

    def add_me(self,ip):
        url = 'http://' + ip + '/add_node'
        try:
            r=requests.get(url,timeout=self.timeout,params={'port':self.port})
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

    def get_chainlength(self,ip):
        url = 'http://' + ip + '/get_chainlength'
        try:
            r=requests.get(url,timeout=self.timeout)
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

    def get_block(self,ip,height):
        url = 'http://' + ip + '/get_block/' + str(height)
        try:
            r=requests.get(url,timeout=self.timeout)
        except:
            print("Request to ",ip,' failed')
            r=None
        return r


    def get_lastblock(self,ip):
        url = 'http://' + ip + '/get_lastblock'
        try:
            r=requests.get(url,timeout=self.timeout)
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

    def get_blocks(self,ip,start,end):
        url = 'http://' + ip + '/get_blocks'
        try:
            r=requests.get(url,timeout=self.timeout,params={'start':start,'end':end})
        except:
            print("Request to ",ip,' failed')
            r=None
        return r

class NodeEvent:
    def __init__(self,data=None) -> None:
        self.event = threading.Event()
        self.data = data
        self.set = self.event.set
        self.wait = self.event.wait
        self.is_set = self.event.is_set
        self.clear = self.event.clear

class Node:
    def __init__(self,blockchain,utxo_pool,**kwargs) -> None:
        self.request = NodeRequests(port=kwargs.get('port',5000))
        self.nodeslist = kwargs.get('nodeslist',[])
        self.newblock_event = NodeEvent()
        self.mine_event = NodeEvent()
        self.open_txs = kwargs.get('open_txs',[])
        self.blockchain = blockchain
        self.mineblock = mineblock
        self.coinbaseaddr = kwargs.get('coinbaseaddr','PmYxd2pPnetR1bGZEUMMWS5P8kykj7yLS')
        self.tx_verifier = Tx_verifier(utxo_pool)
        self.miningreward = 50 * 10000 #50 coins i.e 500000 units
        self.flask_app = flask_app(self.blockchain,self.newblock_event,self.tx_verifier,self.open_txs,self.mine_event,self.nodeslist)

    def transmit_block(self,blockjson):
        alive=[]
        fs=[]
        print('Started Transmitting')
        with ThreadPoolExecutor(max_workers=8) as hthreads:
            for node in self.nodeslist:
                f=hthreads.submit(self.request.heartbeat,node)
                fs.append(f)

        for f in fs:
            r = f.result()
            if(r):
                alive.append(r.text)
        print('Found alive nodes')
        with ThreadPoolExecutor(max_workers=8) as threads:
            for node in alive:
                threads.submit(self.request.transmit_block,node,blockjson)

        print('Transmitted')

    def update_peers(self):
        fs=[]
        with ThreadPoolExecutor(max_workers=16) as threads:
            for node in self.nodeslist:
                f=threads.submit(self.request.get_nodes,node)
                fs.append(f)

        for f in fs:
            r=f.result()
            if(r):
                for i in r.json():
                    self.nodeslist.append(r[i])

    def listen(self):
        self.flask_app.run()

    def mine(self):
        lastblock = self.blockchain.get_lastblock()
        coinbase = Wallet.create_coinbase(self.coinbaseaddr,block_height=lastblock.block_height+1,reward=self.miningreward)
        block = Block([coinbase],lastblock.hash)
        block.add_transactions(self.open_txs)
        print('Started mining...')
        self.mineblock(block)
        blockjson = block.toJSON()
        print(blockjson)
        r1=requests.get('http://127.0.0.1:5000/heartbeat')
        r= requests.post('http://127.0.0.1:5000/new_block',json=blockjson) #needs changing ig


    def run(self):
        th = threading.Thread(target=self.listen,daemon=True)
        th.start()
        while True:
            if(self.newblock_event.is_set()):
                print("Found new block")
                blockjson=self.newblock_event.data
                tt=threading.Thread(target=self.transmit_block,args=[blockjson])
                tt.start()
                self.newblock_event.clear()
                self.newblock_event.data=None

            if(self.mine_event.is_set()):
                mt=threading.Thread(target=self.mine)
                mt.start()
                mt.join()
                self.mine_event.clear()      
