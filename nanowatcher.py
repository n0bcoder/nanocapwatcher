import asyncio
import json
import requests
from web3 import Web3
from websockets import connect
import sys
import abi as key


ws_url = 'ws://127.0.0.1:8546'
rpc_url = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(rpc_url))

def run():
    print("*Nanocap watcher ............")
    async def get_event():
        async with connect(ws_url) as ws:
            await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
            subscription_response = await ws.recv()
            response = json.loads(subscription_response)
            txHash = response['result']

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=15)
                    response = json.loads(message)
                    if response['params']['result'] != txHash:
                        txHash = response['params']['result']
                        # filter and process the event data here
                        tx = w3.eth.get_transaction(txHash)
                        data = tx.input
                        reg = r'^0x60a06040'
                        contract = re.findall(reg, data)
                        if contract:
                            balance = w3.eth.getBalance(tx['from'])
                            if balance < 950000000000000000:
                                print('Nanocrot Found :'+key.CRED+'\n'+'https://bscscan.com/tx/'+txHash+key.RESET)
                except Exception as e:
                    pass

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(get_event())
    except Exception as e:
        pass

run()
