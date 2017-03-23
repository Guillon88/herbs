import pandas as pd
import datetime, calendar
import re



data = pd.read_excel('todb.xlsx')
data = data.astype(pd.np.object)

new =data.astype(str)['colnum'].map(str.strip).map(str.lower)
inds = new.map(lambda x: True if 'd#' in x or 'duplicate ex' in x else False)
data = data[~inds]
print(data.info())



syns = pd.read_excel('syns.xlsx')
syns = syns.astype(pd.np.object)

syns = syns.applymap(str.strip)


vbgitaxa = pd.read_excel('vbgitaxa.xlsx')
vbgitaxa = vbgitaxa.astype(pd.np.object)
vbgitaxa = vbgitaxa.applymap(str.strip)


# ====== Load all csv files ==========


#allFiles = glob.glob("./*.csv")
#frame = pd.DataFrame()
#list_ = []
#for file_ in allFiles:
#    df = pd.read_csv(file_)
#    list_.append(df)
#frame = pd.concat(list_)
#frame = frame.astype(str)
#frame = frame.applymap(str.lower)

#----- End of the theplantlist db ------



def split_species(sp):
    _sp = sp.split()
    if len(_sp) == 1:
        raise IndexError
    if len(_sp) == 2:
        return _sp[0], _sp[1], ''
    elif len(_sp) >= 3:
        return _sp[0], _sp[1], ' '.join(_sp[2:])

def suggest_species(sp, syns=syns, vbgi=vbgitaxa):
    _syns = syns.copy()
    _syns = syns.applymap(str.lower)
    _vbgi = vbgi.copy()
    _vbgi = vbgi.applymap(str.lower)

    # ------------ Preliminary evaluations ------------
    _sp = sp.split()
    if len(_sp) == 1:
        return ((_sp[0], 'sp.', ''), 0)

    if _sp[1] == 'aff.' or _sp[1] == 'aff':
        return ((sp[0], 'sp.', ''), 0)

    if _sp[1] == 'cf.' or _sp[1] == 'cf':
        return ((_sp[0], _sp[2], ' '.join(_sp[3:])), 0) if (len(_sp) >= 4) else ((_sp[0], _sp[2], ''), 0)

    if _sp[1] == 'sp' or _sp[1] == 'sp.':
        return ((_sp[0], 'sp.', ''), 0)
    # --------------------------------------------------

    ix = _syns['current'].map(lambda x: x.startswith(sp))
    filtered = syns[ix]
    if len(filtered) == 1:
        if 'the same' in filtered.iloc[0]['approved']:
            return (split_species(filtered.iloc[0]['current']),0)
        else:
            return (split_species(filtered.iloc[0]['approved']),0)
    elif len(filtered) > 1:
         if 'the same' in filtered.iloc[0]['approved']:
            return (split_species(filtered.iloc[0]['current']), len(filtered))
         else:
            return (split_species(filtered.iloc[0]['approved']), len(filtered))

    nix = _syns['approved'].map(lambda x: x.startswith(sp))
    nfiltered = syns[nix]
    if len(nfiltered) == 1:
        return split_species(nfiltered.iloc[0]['approved'])
    elif len(nfiltered) > 1:
        return split_species(nfiltered.iloc[0]['approved'], len(nfiltered))

    vbgix = _vbgi['current'].map(lambda x: x.startswith(sp))
    vfiltered = vbgi[vbgix]
    if len(vfiltered) == 1:
        return split_species(vfiltered.iloc[0]['current'])
    elif len(vfiltered) > 1:
        return (split_species(vfiltered.iloc[0]['current']), len(vfiltered))
    return split_species(sp)

def extract_species(x):
    ns = x.replace('together with', '').strip()
    alist = map(str.strip, ns.split('@') if '@' in ns else ns.split(';'))
    return list(filter(lambda x: len(x)>0, alist))


def parse_month(ss):
    try:
        res = re.findall('\.(\d\d)\.')[0]
    except:
        res = ''
    return res


def parse_year(ss):
    try:
        res = re.findall('\.(\d\d\d\d)\.')[0]
    except:
        res = ''
    return res

def evaluate_row(row):
    row = {name: str(row[name]) if not pd.isnull(row[name]) else '' for name in row.keys().tolist()}
    result = {'species': None,
              'additionals': [],
              'detailed': '',
              'region': '',
              'fieldid': '',
              'country': '',
              'collected_s': None,
              'collected_e': None,
              'collectedby': '',
              'identified_s': None,
              'identified_e': None,
              'identifiedby': '',
              'altitude': None,
              'itemcode': None,
              'lat':None,
              'lon':None,
              'note': ''
              }
    tonote = ''
    # Get main species
    result.update({'species': suggest_species(row['species'].strip().lower())})

    # Get lat & lon
    result.update({'lat': row['lat'], 'lon': row['lon']})


    # Get itemcode
    try:
        curnum = re.findall('(\d+)', row['curnum'])[0]
    except:
        curnum = ''

    try:
        result.update({'altitude': re.findall('(\d+)', row['alt'])[0]})
    except:
        pass

    result.update({'itemcode': curnum if len(curnum)<15 else ''})
    if len(curnum) >= 15: tonote+='[%s]' % curnum

    # get fieldid
    if len(row['colnum']) < 20:
        result.update({'fieldid': row['colnum'].strip()})
    else:
        tonote += '[%s]' % row['colnum'].strip()

    #get ecology
    if len(row['ecology']) < 300:
        result.update({'detailed': row['ecology'].strip()})
    else:
        tonote += '[%s]' % row['ecology'].strip()

    identifiedby = row['determiner'].strip()
    collectedby = row['collector'].strip()
    country = row['country'].strip()
    result.update({'country': country,
                   'identifiedby': identifiedby,
                   'collectedby':collectedby
                   })

    #Get region
    _country = country.lower()
    rr = row['label'].lower().replace(_country + ' ','').replace(_country + '.','').replace(_country + ',','')
    region = rr.split('.')[0].capitalize().strip() if len(rr.split('.')[0]) < 150 else  ''
    if not region:
        region = rr.split(',')[0].capitalize().strip() if len(rr.split(',')[0])<150 else ''
    result.update({'region': region})

    splitted = ','.join(map(str.capitalize, rr.split(',')))
    splitted = '.'.join(map(str.capitalize, splitted.split('.')))
    tonote += splitted

    if row['collected']:
        try:
            idents = datetime.datetime.strptime(row['collected'].strip(),'%d.%m.%Y')
        except:
            tonote += '[collected=%s]' % row['collected']
            idents = None
        if idents:
            result.update({'collected_s': idents})

    ed = sd = ''
    if row['determined']:
       m = parse_month(row['determined'])
       y = parse_year(row['determined'])
       if y:
           sd = datetime.date(year=y, m=1, d=1)
           ed = datetime.date(year=y, m=12, d=calendar.monthrange(year=y, month=12)[1])
       if m:
           sd.month = m
           ed.month = m
           ed.day = calendar.monthrange(year=y, month=m)[1]
    if ed or sd:
       result.update({'collected_s': sd})
       result.update({'collected_e': ed})

    # filling additionals
    adds = []
    if row['comment'].strip():
        for item in extract_species(row['comment']):
            adds.append(suggest_species(item.lower().strip()))
        result.update({'additionals': adds})

    result.update({'note': tonote})

    return result


for ind, row in data.iterrows():
    print('\n'+'='*100)
    print(ind, evaluate_row(row))
    print('='*100+'\n')
