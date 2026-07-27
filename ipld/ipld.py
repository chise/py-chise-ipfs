#import requests
import httpx
#import json

#IPFS_API_URL = "http://localhost:5001/api/v0"

# def dag_get (cid):
#     response = requests.post(f"{IPFS_API_URL}/dag/get", params={"arg": cid}, headers = {"Content-Type": "application/json; charset=utf-8"}, encoding='utf-8')
#     #response = requests.post(f"{IPFS_API_URL}/dag/get", params={"arg": cid})
#     #response.encoding = response.apparent_encoding
#     return (response.text)

import libipld

IPFS_GW_URL = "https://ipfs.nijl.ac.jp/ipfs"

def dag_get (cid):
    with httpx.Client() as client:
        response = client.get(f"{IPFS_GW_URL}/{cid}")
        if response.status_code == 200:
            return libipld.decode_dag_cbor(response.content)
