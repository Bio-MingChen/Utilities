##########################Warning#######################
#Functions in this scripts just adapt to my work scenario
#I record them to re-use when proper time in the future
#So you can just omit them


#=====================================
# path_is valid is used to check a path is valid and
# have at lest one fastq file in it
#=====================================
def path_is_valid(path,lib,idx):
    """
    check the valid of path
    """
    alt_lib = "-".join([lib,idx])
    path1 = os.path.join(path,lib)
    path2 = os.path.join(path,alt_lib)
    for path in [path1,path2]:
        if os.path.isdir(path):
            if os.listdir(path):
                fq_exist = any([True if re.search(r'fq.gz$',i) else False for i in os.listdir(path)])
                if fq_exist:
                    return True
    return False
