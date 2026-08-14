import re
import libipld
import ipld

def decode_char (ccs, cpos):
    with open('data/gCCS_cpos_oid.tsv', 'r') as f:
        for line in f:
            match = re.search(f'^{re.escape(ccs)}\t{cpos}\t([^\t\n\r]+?)$', line)
            if match:
                oid = match.group(1)
                match = re.search('^[0-9]+$', oid)
                if match:
                    return chr(int(oid))
                else:
                    return {'genre': 'character',
                            'id': oid,
                            'ref': {'/': oid}}

def oid_to_node_id (character):
    if isinstance(character, dict):
        ref = character.get('ref', None)
        if isinstance(ref, bytes):
            oid = libipld.encode_cid(ref)
        else:
            oid = ref.get('/', None)
    elif len(character) == 1:
        oid = str(ord(character))
    else:
        oid = character

    with open('data/oid_node-cid.tsv', 'r') as f:
        for line in f:
            match = re.search(f'^{oid}\t([^\t\n\r]+?)$', line)
            if match:
                return match.group(1)

def get_sections (object_id):
    node_cid = oid_to_node_id (object_id)
    return ipld.dag_get(f'{node_cid}')

def get_section (object_id, section):
    node_cid = oid_to_node_id (object_id)
    return ipld.dag_get(f'{node_cid}/{section}')
