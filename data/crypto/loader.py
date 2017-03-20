import pandas as pd
import glob




data = pd.read_excel('todb.xlsx')
data = data.astype(pd.np.object)


syns = pd.read_excel('syns.xlsx')
syns = syns.astype(pd.np.object)

syns = syns.applymap(str.strip)


vbgitaxa = pd.read_excel('vbgitaxa.xlsx')
vbgitaxa = vbgitaxa.astype(pd.np.object)
vbgitaxa = vbgitaxa.applymap(str.strip)


# ====== Load all csv files ==========


allFiles = glob.glob("./*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_)
    list_.append(df)
frame = pd.concat(list_)
frame = frame.astype(str)
frame = frame.applymap(str.lower)

#----- End of the theplantlist db ------





def suggest_species(sp, syns=syns, vbgi=vbgitaxa, main=frame):
    _syns = syns.copy()
    _syns = syns.applymap(str.lower)
    _vbgi = vbgi.copy()
    _vbgi = vbgi.applymap(str.lower)

    splitted = sp.split()
    if len(splitted)>1:
        if any((main['Genus'] == splitted[0].strip()) & (main['Species'] == splitted[1].strip())):
            return True
    elif len(splitted)==1:
        return any(main['Genus']==splitted[0].strip())
    
    ix = _syns['current'].map(lambda x: x.startswith(sp))
    filtered = syns[ix]
    if len(filtered) >= 1:
        if 'the same' in filtered.iloc[0]['approved']:
            return filtered.iloc[0]['current']
        else:
            return filtered.iloc[0]['approved']
    else:
        pass
    nix = _syns['approved'].map(lambda x: x.startswith(sp))
    nfiltered = syns[nix]
    if len(nfiltered) >= 1:
        return nfiltered.iloc[0]['approved']
    else:
        pass
    vbgix = _vbgi['current'].map(lambda x: x.startswith(sp))
    vfiltered = vbgi[vbgix]
    if len(vfiltered) >= 1:return vfiltered.iloc[0]['current']

    
    return None



def extract_species(x):
    ns = x.replace('together with', '').strip()
    alist = map(str.strip, ns.split('@'))
    return list(filter(lambda x: len(x)>0, alist))



#print(suggest_species('nardia les'))

notfound = []
for ind, row in data.iterrows():
    if not pd.isnull(row['comment']):
       comm = extract_species(row['comment'])
       if comm:
           for item in comm:
               what = ' '.join(item.strip().lower().split()[:2])
               rc = suggest_species(what)
               if rc is None:
                    print('(Comment)', ind + 2, item)
                    notfound.append(what)
    if not pd.isnull(row['species']):
        res = suggest_species(row['species'].strip().lower())
        if res is None:
            print('(Species)', ind+2, row['species'])
            notfound.append(row['species'].lower().strip())
            
print("\nUnique species, total:", len(list(pd.np.unique(notfound))))
