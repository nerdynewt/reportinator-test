import pandas
import io
import os
import configparse
import sys


# Change working directory
script = str(os.path.dirname(os.path.realpath(sys.argv[0])))
cache_dir=configparse.cfg["cache_dir"]
# os.chdir(script)

section=sys.argv[1]
name=section.split('\n', 1)[0][2:]

def convertToLaTeX(df, alignment="c"):
    numColumns = df.shape[1]
    numRows = df.shape[0]
    output = io.StringIO()
    colFormat = ("%s|" % (("|"+ alignment) * numColumns))
    # Write header
    output.write("\\begin{tabular}{%s}\n" % colFormat)
    columnLabels = ["\\textbf{%s}" % label for label in df.columns]
    output.write("\\hline%s\\\\\\hline\n" % " & ".join(columnLabels))
    # Write data lines
    for i in range(numRows):
        output.write("%s\\\\\hline\n"
                     % (" & ".join([str(val) for val in df.iloc[i]])))
    # Write footer
    output.write("\\end{tabular}")
    return output.getvalue()

# CSV FILES
if not os.listdir(cache_dir+"/csvs/"):
    pass
else:
    for item in os.listdir(cache_dir+"/csvs/"):
        path = cache_dir+"/csvs/" + item
        df = pandas.read_csv(path)
        df = df.round(decimals=2)
        print(convertToLaTeX(df,alignment='c'))

# EXCEL
if os.path.exists(cache_dir+"/data.xlsx"):
    path = cache_dir+"/data.xslx"
    xls = pandas.ExcelFile(path)
    sheets = xls.sheet_names

    for sheet in sheets:
        df = pandas.read_excel(xls, sheet_name=sheet, index_col=None)
        df = df.round(decimals=2)
        print(convertToLaTeX(df,alignment='c'))
