import argparse
import os
import sys


parser = argparse.ArgumentParser(description='Image Processing in reportinator')
parser.add_argument('--file', required=True, help="Directory path of the source files, without / at the end")

args = parser.parse_args()
file = args.file
location = "../_assets/"+args.file
act_location = "./"+args.file

def ext(fp):
    ext = os.path.splitext(fp)[-1].lower()
    if ext == ".jpeg":
        return file[:-5]
    else:
        return file[:-4]

file_name = ext(location)

print ('\\begin{figure}[H]'+'\n'+'\\centering'+'\n'+'\\includegraphics[width = \\columnwidth]'+'{'+act_location+'}'+'\n'+'\\caption{'+file_name+'}'+'\n'+'\\label{fig:\"'+file_name+'\"}'+'\n'+'\\end{figure}')


