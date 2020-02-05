#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import json
import sys
from functools import partial
import argparse

#handlering the output encode problem
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
elif sys.version_info[0] == 3:
    open = partial(open,encoding='utf-8')

from utilities import make_colors

colors = make_colors()

class SpeciesLib():
    """
    SpeciesLib offer reading, adding and 
    delete functions to the Species Translations
    """
    def __init__(self,trans_path=None):
        if not trans_path:
            BASIC_DIR = os.path.dirname(os.path.abspath(__file__))
            trans_path = os.path.join(BASIC_DIR,'species_translation.json')
        self.trans_path = trans_path
        with open(trans_path,'r') as indata:
            trans_dict = json.load(indata)
        self.config_dict = trans_dict
        
    def add(self,key,value):
        """
        Update {key:value} to  .keylib config
        """
        print('Update {key}: {value} to config...'.format(key=key,value=value))
        self.config_dict.update({key:value})

    def remove(self,key):
        """
        Remove indicated value from ~/.keylib
        """
        if self.config_dict.get(key):
            del self.config_dict[key]
            print('{key} have been removed from config {config_path}!'.format(
                key=key,config_path=self.trans_path))
        else:
            print('{key} you want to remove from ~/.keylib doesn\'t exists!So do nothing'.format(key=key))

    def save(self):
        """
        write a new config with init_keys
        """
        with open(self.trans_path,'w') as odata:
            # print(self.config_dict)
            json.dump(self.config_dict,odata,indent=2,ensure_ascii=False)
        config_json = json.dumps(self.config_dict,indent=2,ensure_ascii=False)
        print('update result dict:\n{green}{bright}{config_json}{back}'.format(
            config_json=config_json,**colors))

    def show(self):
        """
        show the content of .keylib
        """
        config_json = json.dumps(self.config_dict,indent=2,ensure_ascii=False)
        if sys.version_info[0] == 2:
            print("{green}{bright}{config_json}{back}".format(config_json=config_json.encode('utf-8'),**colors))
        else:
            print("{green}{bright}{config_json}{back}".format(config_json=config_json,**colors))

    def __getitem__(self,tag):
        """
        reading config file and generate
        config_dict and get item from it
        """
        key = self.config_dict.get(tag)
        if key:
            return key
        else:
            # self.show()
            return None 
    def __contains__(self,key):
        """
        in operator
        """
        if key in self.config_dict:
            return True
        return False

def translation_operations(args):
    """
    execute the show,add and remove functions
    of SpeciesLib
    """
    spe_lib = SpeciesLib()
    if args.get('show'):
        spe_lib.show()
    if args.get('add'):
        for tup in args.get('add').split(','):
            key,value = tup.split(':')
            spe_lib.add(key,value)
        spe_lib.save()
    if args.get('remove'):
        for key in args.get('remove').split(','):
            spe_lib.remove(key)
        spe_lib.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--show','-s',action="store_true",help='show the translation dict')
    parser.add_argument('--add','-a',help='add translation,format like key1:value1,key2:value2,...')
    parser.add_argument('--remove','-r',help="remove keys,input format like key1,key2,...")
    args = parser.parse_args()
    translation_operations(vars(args))