from gigspot_site.utils import conv

def parse_tag(elem, tag):
    tag_elems = elem.findall(tag)
    if not len(tag_elems):
        return None
    res = []
    for tag_elem in tag_elems:
        children = tag_elem.getchildren()
        if children:
            child_tags = list(set([c.tag for c in children]))
            child_dict = {}
            for child_tag in child_tags:
                child_dict[child_tag] = parse_tag(tag_elem, child_tag)
            res.append(child_dict)
        else:
            res.append(tag_elem.text)
    if len(res) == 1:
        return res[0]
    return res

def get_field(elem, rec, tag, is_list=False):
    field = parse_tag(elem, tag)
    if field is not None:
        if is_list:
            rec[tag] = conv.to_list(field)
        else:
            rec[tag] = field

def get_record(elem, tags):
    rec = {}
    for t in tags:
        get_field(elem, rec, t)
    return rec

# def get_mandatory(elem, tags, is_list=False):
#     info = {}
#     for t in tags:
#         info[t] = parse_tag(elem, t)
#         if info[t] is None:
#             raise KeyError()
#     return info

# def get_optional(elem, tags, is_list=False):
#     info = {}
#     for t in tags:
#         v = parse_tag(elem, t)
#         if v is None:
#             continue
#         info[t] = v
#     return info
