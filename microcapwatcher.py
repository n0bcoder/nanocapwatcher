import asyncio
import json
import requests
from web3 import Web3
from websockets import connect
import time
import sys
import re

ws_url = 'ws://127.0.0.1:8546'
rpc_url = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(rpc_url))

#exclude
exclude = r'0x244AE091Cc6f9A95F42d64B14Aa71d0cC692e312|0xaa8CF065ab44A6E4Eb2B3aBa786530E7F0c7AaE6|0x89A94eef968066A59dfd8444C512aAbe763Be669'

def runme():
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
                        fr = tx['from']
                        reg = r'^0x60a06040'
                        contract = re.findall(reg, data)
                        if contract:
                            ex = re.findall(exclude, fr)
                            if ex:
                                pass
                            if not ex:
                                balance = w3.eth.getBalance(fr)
                                if balance < 950000000000000000:
                                    print('Microcap found :'+'\n'+'https://bscscan.com/tx/'+txHash)
                except Exception as e:
                    pass

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(get_event())
    except Exception as e:
        pass

runme()
