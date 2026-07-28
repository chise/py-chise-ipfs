import re
import libipld
import ipld

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
