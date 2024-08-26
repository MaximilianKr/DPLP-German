from lxml import etree
import os, sys, json, copy
import argparse

def remove_title(rst):
    matches = rst.xpath('/rst/body/segment[@id=1]')
    if len(matches) == 0:
        return False
    
    title = matches[0]
    # check if the title is not used anywhere in the document
    if rst.xpath(f'/rst/body/segment[@parent=1]') or rst.xpath(f'/rst/body/group[@parent=1]'):
        return False
    
    title.getparent().remove(title)
    return True
    
# def map_relations(rst, relmap, filename):
#     for node in rst.xpath('/rst/body/*'):
#         relname = node.get('relname')
#         if relname is None:
#             continue
#         if relname not in rel_map:
#             raise Exception(f"Error:unknonw relation {relname} found in {filename}")
#         node.set('relname', rel_map[relname])
    
#     relations = rst.xpath('/rst/header/relations')[0]
#     rel_lookup = set()
#     for rel in list(relations.xpath('rel')):
#         name = rel.get('name')
#         type = rel.get('type')

#         if name not in relmap:
#             relations.remove(rel)
#             continue
#         name = relmap[name]

#         key = name+type
#         if key in rel_lookup:
#             relations.remove(rel)
#         else:
#             rel.set('name', name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Removes the orphan title EDU (if there is any) and copies the original file to the backup directory',
    )
    parser.add_argument('path')           # positional argument
    # parser.add_argument("-b", "--backup_path", type=str, default='rs3_backup', help="Path where we will backup the changed rs3 files.")

    args = parser.parse_args()
    path = args.path
    # backup_path = path + args.backup_path
    
    with open('parsing_eval_metrics/rel_mapping.json') as f:
        rel_map = json.load(f)
        # avoid error for the relations aready mapped
        for val in list(rel_map.values()):
            rel_map[val] = val

    #if not os.path.exists(backup_path):
    #    os.mkdir(backup_path)

    all_files = os.listdir(path)
    for filename in sorted(all_files):
        if not filename.endswith('.rs3'):
            continue

        filename = f'{path}/{filename}'
        parser = etree.XMLParser(remove_blank_text=True)
        rst = etree.parse(filename, parser)

        #if (remove_title(rst)):
        #    os.system(f'cp {path}/{filename} {backup_path}/{filename}')
        # map_relations(rst, rel_map, filename)

        rst.write(filename, xml_declaration=False, pretty_print=True, encoding='utf8')

    print("RS3 preprocessing finished")
