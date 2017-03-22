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



def split_species(sp):
    _sp = sp.split()
    if len(_sp) == 1:
        raise IndexError
    if len(_sp) == 2:
        return _sp[0], _sp[1], ''
    elif len(_sp) >= 3:
        return _sp[0], _sp[1], ' '.join(_sp[3:])

def suggest_species(sp, syns=syns, vbgi=vbgitaxa, main=frame):
    _syns = syns.copy()
    _syns = syns.applymap(str.lower)
    _vbgi = vbgi.copy()
    _vbgi = vbgi.applymap(str.lower)

    # ------------ Preliminary evaluations ------------
    _sp = sp.split()
    if len(_sp) == 1:
        return (sp[0], 'sp.', '')

    if _sp[1] == 'aff.' or _sp[1] == 'aff':
        return (sp[0], 'sp.', '')

    if _sp[1] == 'cf.' or _sp[1] == 'cf':
        return (_sp[0], _sp[2], ' '.join(_sp[3:]) if (len(_sp) >= 4) else (_sp[0], _sp[2], ''))

    if _sp[1] == 'sp' or _sp[1] == 'sp.':
        return (_sp[0], 'sp.', '')
    # --------------------------------------------------

    authorship = ' '.join(_sp[2:]) if len(_sp) >= 3 else ''
    if len(_sp) >= 2:
        if any((main['Genus'] == _sp[0]) & (main['Species'] == _sp[1])) & (main['Authorship'] == authorship):
            return  (_sp[0], _sp[1], authorship)

    ix = _syns['current'].map(lambda x: x.startswith(sp))
    filtered = syns[ix]
    if len(filtered) == 1:
        if 'the same' in filtered.iloc[0]['approved']:
            return split_species(filtered.iloc[0]['current'])
        else:
            return split_species(filtered.iloc[0]['approved'])
    elif len(filtered) > 1:
        print('%s: %s items found' % (sp, len(filtered)))
    nix = _syns['approved'].map(lambda x: x.startswith(sp))
    nfiltered = syns[nix]
    if len(nfiltered) == 1:
        return split_species(nfiltered.iloc[0]['approved'])
    elif len(nfiltered) > 1:
        print('%s: %s items found' % (sp, len(nfiltered)))

    vbgix = _vbgi['current'].map(lambda x: x.startswith(sp))
    vfiltered = vbgi[vbgix]
    if len(vfiltered) == 1:
        return split_species(vfiltered.iloc[0]['current'])
    elif len(vfiltered) > 1:
        print('%s: %s items found' % (sp, len(nfiltered)))
    return split_species(sp)

def extract_species(x):
    ns = x.replace('together with', '').strip()
    alist = map(str.strip, ns.split('@'))
    return list(filter(lambda x: len(x)>0, alist))


for ind, row in data.iterrows():
    if not pd.isnull(row['comment']):
       comm = extract_species(row['comment'])
       if comm:
           for item in comm:
               print(suggest_species(item))
   if not pd.isnull(row['species']):
       res = suggest_species(row['species'].strip().lower())
       print(res)
