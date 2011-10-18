
def etree_to_dict(etree):
    data = {}
    for kv in etree:
        if len(list(kv)):
            value = etree_to_dict(kv)
        else:
            value = kv.text
        data[kv.tag] = value
    return data
