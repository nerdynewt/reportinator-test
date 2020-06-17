import glob
import os
# print(os.listdir())
# f=os.listdir()
# for f in glob.glob("*.aux" or "*.bcf" or "*.log" or "*.run.xml" or "*.fls" or ".fbd.latexmk" or ".blg"):
for f in glob.glob("*.tex" or "*.fls"):
    print(f)
