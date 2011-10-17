
def etree_to_dict(etree):
    """Too stupid, probably needs to be recursive"""
    return {kv.tag: kv.text for kv in etree}
