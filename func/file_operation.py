# -*- coding=utf-8 -*-

#Functions in this script are all about file operations
#like open files by their file type or get columns by file title etc.

import gzip

#=======================================================
#TitleParser is used to get columns by file's title name
#========================================================
class TitleParser():
    """
    Reading in a file title and than getting indicated column element.
    Title names are all CaseIgnore
    """
    
    def __init__(self,title):
        self.title_list = [i.lower() for i in title.strip().split('\t')]

    def get_field(self,line_list,colname,check=True):
        """
        Reading in a list and returning the element with the 
        index which colname in title's list
        """
        if check:
            if len(self.title_list) != len(line_list):
                raise Exception("Title length differs with line!")
        try:
            idx = self.title_list.index(str(colname).lower())
        except:
            print('{colname} not in title！'.format(colname=colname))
            return None

        return line_list[idx]

    def have_title(self,colname):
        """
        Judging whether a colname is in title
        """
        if str(colname).lower() in self.title_list:
            return True
        return False
    
    def get_idx(self,colname):
        """
        return index of columns by their name in title list
        """
        idx = self.title_list.index(str(colname).lower())

        return idx

#=======================================
#gopen function is used to open file by their suffix
# open .gz file with gzip.open else open
#=======================================

def gopen(filename,mode):
    """
    open .gz file with gzip.open
    open plain text file with open
    """
    if filename.endswith('.gz'):
        return gzip.open(filename,mode)

    return open(filename,mode)


    
