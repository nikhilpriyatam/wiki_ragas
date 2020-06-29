"""Generates wiki article for any domain from domain KB, template, rendering
code

@author: Nikhil Pattisapu, iREL, IIIT-H"""


import json
import argparse
from jinja2 import Environment, FileSystemLoader


ENV = Environment(loader=FileSystemLoader('templates')) # Global variable


def render_template(template_name, entry_dict, res_path):
    """Demo filters"""
    template = ENV.get_template(template_name)
    res_str = template.render(**entry_dict)
    with open(res_path, 'w') as res:
        res.write(res_str)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--kb_path')
    # PARSER.add_argument('--kb_id')
    PARSER.add_argument('--template_name')
    PARSER.add_argument('--result_path')

    ARGS = PARSER.parse_args()
    DOMAIN_KB = json.load(open(ARGS.kb_path, 'r'))
    for item in DOMAIN_KB:
        render_template(ARGS.template_name, item,
                        ARGS.result_path + item['name'] + '.wiki')
        # if item['name'] == ARGS.kb_id:
        #     render_template(ARGS.template_name, item, ARGS.result_path)
        #     break
