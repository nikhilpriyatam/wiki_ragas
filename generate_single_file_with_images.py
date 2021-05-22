"""Generates wiki article for any domain from domain KB, template, rendering
code

@author: Nikhil Pattisapu, iREL, IIIT-H"""


from os import path
import json
import argparse
from jinja2 import Environment, FileSystemLoader


ENV = Environment(loader=FileSystemLoader('templates')) # Global variable


def render_template(template_name, entry_dict):
    """Demo filters"""
    template = ENV.get_template(template_name)
    res_str = template.render(**entry_dict)
    return res_str


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--kb_path')
    PARSER.add_argument('--img_path')
    PARSER.add_argument('--template_name')
    PARSER.add_argument('--result_file')

    ARGS = PARSER.parse_args()
    DOMAIN_KB = json.load(open(ARGS.kb_path, 'r'))
    res_str = ""
    for item in DOMAIN_KB:
        img_paths = []
        raga_img = ARGS.img_path + "/" + item['name'] + '_kb2wiki.png'
        if path.exists(raga_img):
            img_paths.append(item['name'] + '.png')
        else:
            img_paths.append(item['name'] + "_ar_kb2wiki.png")
            img_paths.append(item['name'] + "_av_kb2wiki.png")
        item['img_paths'] = img_paths
        res_str += "{{-start-}}\n"
        res_str += render_template(ARGS.template_name, item)
        res_str += "{{-stop-}}\n"
    with open(ARGS.result_file, 'w') as res:
        res.write(res_str)
