"""In ansys WB create named sections based on region of interest(edge1,edge2,edge3,edge4..etc)
Run the script (disp_line_plot.py)  to extract the deformation results for the above named selections.
These are the input for tool macro. Extract the nodal angular locations wrt cylindrical coordinate system.
Note: export manually from Ansys wb, make sure the number of nodes matches with the result file and has angular data.
angle in degrees. Node number from two files should match else you will see not graph.
"""

import glob
import os
import xlsxwriter
import openpyxl
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from openpyxl import load_workbook


#fpath = ('C:\\Users\\arpuste\\Downloads\\case2\\displ_edge4.txt')
#path = os.getcwd()
path= filedialog.askdirectory(title='Select a Folder which contains data files')
files = glob.glob(os.path.join(path, "*.txt"))
print(files)

dfs = []

for file in files:
    df = pd.read_csv(file, sep='\t')
    df['source'] = os.path.basename(file)
    dfs.append(df)

df_master= pd.concat(dfs, axis=0)
filename = 'dataframe.csv'
#itle=dfs.df_master.values.tolist()
title=str(df_master.columns.values[4])
print(title)

#my_list = ['Node Number','Normal Stress (MPa)','source']
#for item in my_list:
df_node_disp= df_master.filter(['Node Number', title , 'source'])

print(df_node_disp)


path2= filedialog.askdirectory(title='Select a Folder which contains Node detail files')
files2 = glob.glob(os.path.join(path2, "*.txt"))
print(files2)

dfnodes = []

for filee in files2:
    df = pd.read_csv(filee, sep='\t',encoding='ISO-8859-1',skiprows=[1])
    df['Location'] = os.path.basename(filee)
    dfnodes.append(df)
# append all the sheet data to one dataframe:
dfn= pd.concat(dfnodes, axis=0)
filename2 = 'nodes_dataframe.csv'
dfn = dfn[dfn.filter(regex='^(?!Unnamed)').columns]
dfnf= dfn.filter(['Node ID', 'Theta(°)', 'Location'])

sorted_df = dfnf.sort_values(by=['Location','Theta(°)'], ascending=True)
#renane the column heading to be common between the two dataframe where merge can be done
df_rename = sorted_df.rename(columns={'Node ID': 'Node Number'})
print(df_rename.head())
""""##The pandas .merge() method allows us to merge two DataFrames together.##
##VLOOKUP is essentially a left join between two tables, that is,
# the output consists of all the rows in the left table and only the matched rows from the right table.#"""

df33= pd.merge(df_node_disp,df_rename, how='left')
df3 = df33.sort_values(by=['source','Theta(°)'], ascending=True)
#df3 is the final dataframe which has all the information and sorted with Source and theta
# unique names from the dataframe
uniqueNames = df3['source'].unique().tolist()
print(uniqueNames)
#final dataframe is filtered based on source and added to a dictionary below
# which is called later to plot graph
df_names = dict()
for k, v in df3.groupby('source'):
    df_names[k] = v
#define number of rows and columns for subplots

# writing all the dictionary data to one excel group
from matplotlib.ticker import AutoMinorLocator
for df_name, df in df_names.items():

     # df.sort_values(by=['Theta(°)'], ascending=True)
     values = df[['Theta(°)',title]]
     #values = df_names['disp_edge3XAxis.txt'][['Theta(°)', 'Normal Stress (MPa)']]
    #print(values)
     #fig = plt.figure()
     #fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

     ax= values.plot.line(x='Theta(°)',y= title, rot=0)
     #ax.plot(values)
     ax.grid()
     plt.xlabel('Angular location (in Degrees)')
     plt.ylabel(title)
     plt.title(str( df_name))
     plt.legend()
     #ax = values.plot.line(x='Theta(°)', y='Normal Stress (MPa)', rot=0)
     #plt.rcParams["figure.figsize"] = [10, 7]

     plt.savefig(str(df_name)+'.jpg', dpi=300)
     #plt.show()
     plt.close()

with pd.ExcelWriter('results1.xlsx',engine="xlsxwriter") as writer:

#writer.sheets = dict((ws.title, ws) for ws in book1.worksheets)
    for df_name, df in df_names.items():
       # df.sort_values(by=['Theta(°)'], ascending=True)
        df.to_excel(writer, sheet_name=str(df_name))


#for elem in uniqueNames:
#print(df_names)
df_stack = pd.concat(df_names, axis=0)

#df_master.to_csv(path +'_'+filename,index=False)


#print(df_names)
#print(df_names['disp_edge1XAxis.txt'])
df3.to_csv(path +'_'+filename2,index=False)
print("excecution completed!")

"""$df2 = pd.read_csv(fpath, sep='\t' )
df2 = df2[df2.filter(regex='^(?!Unnamed)').columns]
print(df2)
print(df2.shape)
print(df2.columns)
# execute(fpath)
print(fpath)"""