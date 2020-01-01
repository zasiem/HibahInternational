# include modules
import os
import pandas as pd
import itertools 
from collections import Counter 
import numpy as np
pd.set_option('display.max_rows', None)

# go to working directory
os.chdir('./data')
print(os.getcwd())

# activity list
membuat = ["buat", "create"]
menambahkan = ["ambah", "add"]
mengubah = ["ubah", "edit"]
update = ["update"]
menghubungkan = ["onek", "connect", "ubung", "ambung"]
memperbaiki = ["baik", "revisi", "fix", "betulkan"]
melengkapi = ["lengkapi"]
testing = ["test"]
resolved = ["resolve"]
merge = ['merge']
kata_sambung = ["dan", "#", "+", ",", "dari", "dengan", "pada", "untuk", "ref", "&", "http"]
conditional = ["fungsional", "layout", "fitur", "menampilkan"]
allAct = membuat + menambahkan + mengubah + update + menghubungkan + memperbaiki + melengkapi + testing + resolved + kata_sambung + merge + conditional


#open each csv file
for file in os.listdir():
  if(os.path.splitext(file)[1] == '.csv'):
    filecsv = pd.read_csv(file)
    f_name,f_ext = os.path.splitext(file)

    #duplicate series and make it in lower case
    aktivitas = filecsv['Message']
    aktivitas = aktivitas.str.lower()

    # make new activity column
    for string in membuat:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'membuat'
    for string in menambahkan:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'menambahkan'
    for string in mengubah:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'mengubah'
    for string in update:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'update'
    for string in menghubungkan:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'menghubungkan'
    for string in memperbaiki:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'memperbaiki'
    for string in melengkapi:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'melengkapi'
    for string in testing:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'testing'
    for string in resolved:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'resolved'
    for string in merge:
        filecsv.loc[aktivitas.str.contains(string), 'activity'] = 'merge'


    # split series into list
    aktivitas = aktivitas.str.split()

    # delete activity keyword from series
    for upItem in aktivitas:
        for items in upItem:
            for act in allAct:
                upItem[:] = ['qwerty' if act in items  else items for items in upItem]

    for upItem in aktivitas:
        if 'qwerty' in upItem:
            upItem[:] = list(dict.fromkeys(upItem))
            upItem.remove('qwerty')

    # convert fitur into string and store it in list
    aktivitas2 = []
    for items in aktivitas:
        items = " ".join(items)
        aktivitas2.append(items)
        
    # make it short
    shortAct = []
    for items in aktivitas2:
        if (len(items.split())) < 3:
            shortAct.append(items)
        else:
            items = items.split()
            a = items[0] + ' ' + items[1]
            shortAct.append(a)

    # create new frame
    newFrame = pd.DataFrame(columns = ['Case ID', 'Timestamp', 'Activity', 'Resource'])  
    newFrame['Timestamp'] = filecsv['Date']
    newFrame['Activity'] = filecsv['activity']
    newFrame['Resource'] = filecsv['Author']
    newFrame.Activity = newFrame.Activity.replace(np.nan, 'menambahkan', regex=True)

    # join activity with fitur
    feature = newFrame['Activity']
    feature = feature.str.split()
    i = 0
    for items in feature:
        items.append(shortAct[i])
        items = " ".join(items)
        i+=1

    # convert into list
    aktifitasbaru = []
    for items in feature:
        items = " ".join(items)
        aktifitasbaru.append(items)

    newFrame['Activity'] = aktifitasbaru

    # grouping fitur
    shortAct[:] = list(dict.fromkeys(shortAct))
    if('' in shortAct):
      shortAct.remove('')
    shortAct

    # grouping fitur into caseID
    caseid = [0] * len(aktifitasbaru)

    i = 1
    aktifitasbaru
    for items in shortAct:
        y = 0
        d = False
        for item in aktifitasbaru:
            if items in item:
                caseid[y] = i
                d = True
            y+=1
            
        if d:
            i+=1
        
    # create new column
    newFrame['Case ID'] = pd.Series(caseid)
    # saved file into new folder
    os.chdir('../')
    if os.path.isdir('./converted'):
        os.chdir('./converted')
        newfile = '{}{}'.format(f_name, f_ext)
        newFrame.to_csv(newfile)
        os.chdir('../data')
    else:
        os.mkdir('converted')
        os.chdir('./converted')
        newfile = '{}{}'.format(f_name, f_ext)
        newFrame.to_csv(newfile)
        os.chdir('../data')








