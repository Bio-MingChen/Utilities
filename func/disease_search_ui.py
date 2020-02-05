#!/usr/bin/env python
# -*- coding=utf-8 -*-

#========================================================================
#This script make a good interact with user to search and determine which
#items should stay at last this is a example of 
# Loading CHPO dataset and get the English and Chinese disease information
# You can change it to adapt to your work scene
#========================================================================

import sys
if sys.version_info[0] == '2':
    reload(sys)
    sys.setdefaultencoding='utf-8'

import re
import json
from textwrap import dedent
from collections import OrderedDict

from fuzzywuzzy import process
import colorama

def make_colors():
    """
    make some colors in command line
    """
    colors = {}
    colorama.init()
    colors['red'] = colorama.Fore.RED
    colors['green'] = colorama.Fore.GREEN
    colors['green_ex'] = colorama.Fore.LIGHTGREEN_EX
    colors['white'] = colorama.Fore.LIGHTWHITE_EX
    colors['magenta_ex'] = colorama.Fore.LIGHTMAGENTA_EX
    colors['magenta'] = colorama.Fore.MAGENTA
    colors['cyan'] = colorama.Fore.CYAN
    colors['cyan_ex'] = colorama.Fore.LIGHTCYAN_EX
    colors['yellow'] = colorama.Fore.YELLOW
    colors['bright'] = colorama.Style.BRIGHT
    colors['back'] = colorama.Style.RESET_ALL
    return colors

class SearchDisease():
    """
    Reading in json file generated by mongoexport
    extract best items by input query_disease and
    interface with user to determine which of them
    should retain to output
    """
    def __init__(self,args):
        self.query_disease = args.get('query')
        self.chpo = args.get('chpo')
        self.cutoff = args.get('cutoff')
        self.limit = args.get('limit')
        print(self.chpo)
        self.query_dict = self.load_chpo_to_query_json(self.chpo)

    def load_chpo_to_query_json(self,chpo_mgjson):
        """
        load chpo dataset from mongo json format
        output {english_name: other info} dict
        """
        query_dict = OrderedDict()
        with open(chpo_mgjson,'r') as indata:
            for line in indata:
                record = json.loads(line)
                en_name = record['name_en']
                _id = record['_id']['$oid']
                query_dict[_id] = record
        return query_dict

    def find_best_results(self,score_cutoff,limit):
        #Get best match ones
        choices_dict = {}
        for _id in self.query_dict:
            choices_dict[_id] = self.query_dict[_id]['name_en']
        # print('score_cutoff is {},limit is {}'.format(score_cutoff,limit))
        search_order = process.extractBests(self.query_disease,choices_dict,score_cutoff=score_cutoff,limit=limit)
        title = dedent("""
        {green}[All candidate diseases list below with score {red}{bright}cutoff {score_cutoff} and limit {limit}{green},
                plase select one or more of them!]{back}
        """.format(score_cutoff=score_cutoff,limit=limit,**colors
            )
        )
        results_str = ""
        for tag,(disease,score,_id) in enumerate(search_order):
            name_cn = self.query_dict[_id]['name_cn']
            description_cn = self.query_dict[_id]['definition_cn']
            description_en = self.query_dict[_id]['definition_en']
            results_str += dedent('''
            {yellow}[{tag}] {red}{bright}{score:>3} : {back}{magenta}{disease}{green}[{name_cn}]{back}
                {yellow}[Description_cn]{back} {description_cn}
                {yellow}[Description_en]{back} {description_en}\
            '''.format(
                tag=tag,
                disease=disease,
                score=score,
                # name_cn='test',
                description_en=description_en.strip(),
                name_cn=name_cn.encode('utf-8'),
                description_cn=description_cn.encode('utf-8').strip(),
                **colors))

        _id_list = [tup[-1] for tup in search_order]
        return title,results_str,_id_list

    def _split_fun(self,i):
        start,end = [ int(j) for j in i.split('-')]
        end += 1
        return {j for j in range(start,end)}

    def user_interaction(self,score_cutoff=None,limit=None):
        '''
        User interaction to determine the results
        '''
        # Set default cutoff and limit
        if not score_cutoff:
            score_cutoff = self.cutoff
        if not limit:
            limit = self.limit
        title,results_str,_id_list = self.find_best_results(score_cutoff=score_cutoff,limit=limit)
        #print title
        if not title:
            print('''{green}[Please make choice:]{back}
            '''.format(**colors))
        else:
            print(title)
        #print results
        if results_str:
            print(results_str)
        else:
            print('{red}{bright}          [No Results!]{back}\n'.format(**colors))
        #run the UI
        print('{red}分数低于90分时，说明匹配度较低，可以考虑换一个疾病搜索{back}'.format(**colors))
        while True:
            print('''{cyan}Commands examples:
            2,4,6 #select 2,4,6 diseases
            1,3-6 #select 1,3,4,5,6 diseases
            all   #select all print diseases
            l=[\d]+ #rechoice the number of items show before
            c=[0,100] #show the item score greater than indicated number which range 0~100 
            q     # quit
            ctrl+spaceback #deleting forward input
            {red}序号从0开始
            {back}'''.format(**colors))

            std = raw_input('{yellow}input tag>{back}'.format(**colors))
            if std == 'q':
                exit(0)
            elif std == 'all':
                std_list = _id_list
            elif re.search('l=([\d]+)',std) or re.search('c=([\d]+)',std):
                if re.search('l=([\d]+)',std):
                    limit = int(re.search('l=([\d]+)',std).group(1))
                else:
                    limit = self.limit
                if re.search('c=([\d]+)',std):
                    cutoff = int(re.search('c=([\d]+)',std).group(1))
                else:
                    cutoff = self.cutoff
                #recursion of user_interaction to change limit and cutoff
                return self.user_interaction(score_cutoff=cutoff,limit=limit)
            else:
                if not re.match(r'^[\d, -]+$',std):
                    print('{red}[Error]invalid input,please input again{back}'.format(**colors))
                    continue
                else:
                    std = re.sub(' ','',std)
                    std_list = set()
                    for i in std.split(','):
                        if '-' in i:
                            aset = self._split_fun(i)
                            std_list = std_list | aset
                        else:
                            std_list.add(int(i))
                    print(std_list)
            selected_ids = [_id_list[idx] for idx in std_list]
            results_dict = OrderedDict()
            for _id in selected_ids:
                results_dict[_id] = self.query_dict[_id]
            break
        print(results_dict)
        return results_dict
    

if __name__ == "__main__":
    #test
    # query_dict = load_chpo_to_query_json('chpo.json')
    # search_ui('heart disease',query_dict)
    # results = process.extractBests('test',{'test':'a','b':'test'})
    # print(results)
    colors = make_colors()
    args = {'query':'heart disease','chpo':'chpo.json','cutoff':80,'limit':10}
    sd = SearchDisease(args)
    sd.user_interaction()
