import httpx
import libipld
import sys

IPFS_API_URL = "http://localhost:5001/api/v0"
IPFS_GW_URL = "https://ipfs.nijl.ac.jp/ipfs"

def ipfs_gw_dag_get (cid):
    with httpx.Client() as client:
        response = client.get(f"{IPFS_GW_URL}/{cid}")
        if response.status_code == 200:
            return libipld.decode_dag_cbor(response.content)

def block_api_dag_get (cid):
    try:
        with httpx.Client() as client:
            response = client.post(f"{IPFS_API_URL}/block/get", params={"arg": cid})
            if response.status_code == 200:
                return libipld.decode_dag_cbor(response.content)
    except httpx.TimeoutException:
        print ('[IPLD Warning] Connection timeout.', file=sys.stderr)
        print(f"[IPLD Warning] Use IPFS GW {IPFS_GW_URL} as the fallback.",
              file=sys.stderr)
        return (ipfs_gw_dag_get(cid))
    except httpx.HTTPStatusError as exc:
        print(f"[IPLD Warning] HTTP error; status code: {exc.response.status_code}.",
              file=sys.stderr)
        print(f"[IPLD Warning] Use IPFS GW {IPFS_GW_URL} as the fallback.",
              file=sys.stderr)
        return (ipfs_gw_dag_get(cid))
    except httpx.RequestError as exc:
        print(f"[IPLD Warning] Kubo IPFS API is not available: {exc}.",
              file=sys.stderr)
        print(f"[IPLD Warning] Use IPFS GW {IPFS_GW_URL} as the fallback.",
              file=sys.stderr)
        return (ipfs_gw_dag_get(cid))

try:
    with httpx.Client() as client:
        response = client.post(f"{IPFS_API_URL}/bootstrap")
        if response.status_code == 200:
            dag_get = block_api_dag_get
except httpx.TimeoutException:
    print ('[IPLD Warning] Connection timeout.', file=sys.stderr)
    print(f"[IPLD Warning] Use IPFS GW {IPFS_GW_URL} as the fallback.",
          file=sys.stderr)
    dag_get = ipfs_gw_dag_get
except httpx.HTTPStatusError as exc:
    print(f"[IPLD Warning] HTTP error; status code: {exc.response.status_code}.",
          file=sys.stderr)
    print(f"[IPLD Warning] Use IPFS GW {IPFS_GW_URL} as the fallback.",
          file=sys.stderr)
    dag_get = ipfs_gw_dag_get
except httpx.RequestError as exc:
    print(f"[IPLD Warning] Kubo IPFS API is not available: {exc}.",
          file=sys.stderr)
    print(f"[IPLD Warning] Use IPFS GW {IPFS_GW_URL} as the fallback.",
          file=sys.stderr)
    dag_get = ipfs_gw_dag_get
