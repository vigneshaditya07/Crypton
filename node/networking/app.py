from node.blockchain.transaction import Transaction
from typing import List
from flask import Flask , request

'''
    API:-
        get_chainlength
        new_block    json data
        add_transaction
        get_utxos
        get_nodes
        add_node     param data
        get_block/<bk_height>
        get_blocks   param data
        get_lastblock
        heartbeat

'''

def flask_app(_blockchain,_newblockevent,_tx_verifier,_open_txs,_mine_event,nodelist:List=[]):
    blockchain = _blockchain
    nodes = nodelist
    newblockevent = _newblockevent
    mine_event = _mine_event
    tx_verifier = _tx_verifier
    open_txs = _open_txs
    app = Flask(__name__)

    @app.route('/get_lastblock')
    def last_block():
        block = blockchain.get_lastblock()
        blockjson = block.toJSON()
        return blockjson,200

    @app.route('/get_block/<bk_height>')
    def get_block(bk_height):
        bk_height=int(bk_height)
        block = blockchain.get_block(bk_height)
        if block:
            blockjson = block.toJSON()
            return blockjson,200
        else:
            return 'Invalid',400

    @app.route('/get_blocks')
    def get_blocks():
        start= int(request.args.get('start'))
        end = int(request.args.get('end'))
        bklength = blockchain.get_length()
        if (start<bklength and end<bklength):
            pass
        else:
            return 'Invalid',400
        blocks = []
        for i in range(start,end+1):
            blocks.append((i,blockchain.get_block(i)))

        blocksjson = { str(height):block.toJSON() for height,block in blocks}
        return blocksjson,200

    @app.route('/add_node')
    def add_node():
        port=request.args.get('port')
        if port:
            ip = request.remote_addr + ':' + str(port)
        if ip:
            nodes.append(ip)
            return 'Added',200
        else:
            return '',400

    @app.route('/get_nodes')
    def get_nodes():
        nds={ str(i): ip for i,ip in enumerate(nodes) }
        return nds

    @app.route('/new_block',methods=['POST'])
    def new_block():
        blockjson=request.get_json()
        if blockjson:
            added=blockchain.add_blockJSON(blockjson,tx_verifier)
            if added:
                newblockevent.data = blockjson
                newblockevent.set()
                tx_verifier.utxo_pool.update_utxopool(blockjson)
                print('added')
                return 'block added',200
            else:
                print('not added')
                return '',400
        else:
            return '',400

    @app.route('/get_utxos')
    def get_utxos():
        addrs=request.args.get('address')
        utxos=tx_verifier.utxo_pool.get_utxos_by_address(addrs)
        utxosd={ str(i): utxo for i,utxo in enumerate(utxos) }
        return utxosd,200

    @app.route('/get_chainlength')
    def chain_length():
        length = blockchain.get_length()
        return {"length":length}

    @app.route('/add_transaction',methods=['POST'])
    def add_transaction():
        txjson=request.get_json()
        if txjson:
            tx=Transaction.fromJSON(txjson)
            open_txs.append(tx)
            mine_event.set()
            return 'Transaction Added',200
        else:
            return '',400


    @app.route('/')
    def home():
        return ''

    @app.route('/heartbeat')
    def heartbeat():
        s=request.server
        ip=s[0]+':'+str(s[1])
        return ip,200

    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.route('/shutdown')
    def shutdown():
        shutdown_server()
        return '',200


    return app
