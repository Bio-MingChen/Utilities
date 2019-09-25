class TitleParser():
    """
    Reading in a file title and than getting indicated column element 
    Case Ignore
    """
    
    def __init__(self,title):
        self.title_list = [i.lower() for i in title.strip().split('\t')]

    def get_field(self,line_list,colname):
        if len(self.title_list) != len(line_list):
            raise Exception("Title length differs with line!")
        try:
            idx = self.title_list.index(str(colname).lower())
        except:
            print('{colname} not in title！'.format(colname=colname))
            return None

        return line_list[idx]
 
 if __name__ == "__main__":
    title = 'ColA\tColB\tColC\n'
    title_parser = TitleParser(title)

    first_line = '1\t2\t3\n'
    col_a = title_parser.get_field(first_line.split('\t'),"cola")
    print(col_a)
    
