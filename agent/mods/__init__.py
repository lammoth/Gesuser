import os
import glob

path = os.path.join(os.path.abspath(os.curdir), __file__)
path = os.path.dirname(path)
file_list = [t for t in glob.glob1(path, "mod_*.py")]
file_list = map(lambda k:k.split(".")[0], file_list)
__all__=list(file_list)
