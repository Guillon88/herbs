 # -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os

sys.path.append('/home/scidam/webapps/bgicms242/bgi')
os.environ['DJANGO_SETTINGS_MODULE']='bgi.settings'
import gc
from .countries import *
from ..models import (Family, Genus, Species, Country, HerbItem,
                      Additionals, HerbAcronym, Subdivision)
from ..utils import  create_safely
import pandas as pd
import datetime, calendar
import re
from geoposition import Geoposition
from django.contrib.auth import get_user_model

CDIR = os.path.dirname(os.path.abspath(__file__))



data = pd.read_excel(os.path.join(CDIR, 'todb.xlsx'))
data = data.astype(pd.np.object)

new =data.astype(str)['colnum'].map(str.strip).map(str.lower)
inds = new.map(lambda x: True if 'd#' in x or 'duplicate ex' in x else False)
data = data[~inds]
print(data.info())



syns = pd.read_excel(os.path.join(CDIR, 'syns.xlsx'))
syns = syns.astype(pd.np.object)

syns = syns.applymap(str.strip)


vbgitaxa = pd.read_excel(os.path.join(CDIR, 'vbgitaxa.xlsx'))
vbgitaxa = vbgitaxa.astype(pd.np.object)
vbgitaxa = vbgitaxa.applymap(str.strip)




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
        return (split_species(nfiltered.iloc[0]['approved']), 0)
    elif len(nfiltered) > 1:
        return (split_species(nfiltered.iloc[0]['approved']), len(nfiltered))

    vbgix = _vbgi['current'].map(lambda x: x.startswith(sp))
    vfiltered = vbgi[vbgix]
    if len(vfiltered) == 1:
        return (split_species(vfiltered.iloc[0]['current']), 0)
    elif len(vfiltered) > 1:
        return (split_species(vfiltered.iloc[0]['current']), len(vfiltered))
    return (split_species(sp), 0)

def extract_species(x):
    ns = x.replace('together with', '').strip()
    alist = map(str.strip, ns.split('@') if '@' in ns else ns.split(';'))
    return list(filter(lambda x: len(x)>0, alist))


def parse_month(ss):
    try:
        res = int(re.findall('\.(\d\d)\.', ss)[0])
    except:
        res = ''
    return res


def parse_year(ss):
    try:
        res = int(re.findall('(\d\d\d\d)', ss)[0])
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
              'lat': '',
              'lon': '',
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
    final = []
    region = ''
    if row['label']:
        rr = row['label'].split('.')
        res = []
        for item in rr:
            res.append(item.split(','))
        prepared = []
        for item in res:
            if isinstance(item, list):
                for el in item:
                    if el.lower() == _country:
                        item.remove(el)
                _it = []
                for x in item:
                    if x.strip():
                        _it.append(x.strip())
                prepared.append(_it)
            else:
                if item.strip().lower() == _country:
                    res.remove(item)
                else:
                    prepared.append(item.strip())

        for item in prepared:
             if not region:
                 if isinstance(item, list):
                     for s in item:
                         if len(s.strip()) >3:
                             region = s.strip()
                             item.remove(s)
                             break
                 elif len(item) > 3:
                     region = item.strip()
                     prepared.remove(item)
             _aux = ''
             if isinstance(item, list) and len(item)>0:
                 _aux = ', '.join(map(str.strip, item))
                 final.append(_aux)
             elif isinstance(item, str):
                 _aux = item
                 if region != _aux.strip():
                     final.append(_aux.strip())
    final = '. '.join(final)
    result.update({'region': region})
    tonote += final

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
           sd = datetime.date(year=y, month=1, day=1)
           ed = datetime.date(year=y, month=12, day=31)
       if m:
           if isinstance(sd, datetime.date):
               sd = sd.replace(month=m)
           if isinstance(ed, datetime.date):
               ed = ed.replace(month=m, day=calendar.monthrange(year=y, month=m)[1])
    if ed or sd:
       result.update({'identified_s': sd})
       result.update({'identified_e': ed})

    # filling additionals
    adds = []
    if row['comment'].strip():
        for item in extract_species(row['comment']):
            adds.append(suggest_species(item.lower().strip()))
        result.update({'additionals': adds})

    result.update({'note': tonote})

    return result




# Preliminary information
user = get_user_model().objects.get(username='bryophyte')
mainuser = get_user_model().objects.get(username='scidam')
herbgroup = Subdivision.objects.get(name__icontains='риптогам')
herbacronym = HerbAcronym.objects.get(name='VBGI')


# -------------------- Main function: Data loading -------------------
for ind, row in data.iterrows():
    print('Evaluating ind:', ind)
    row_data = evaluate_row(row)
    tonote = row_data['note']

    # -------- species loading --------
    genus = row_data['species'][0][0].lower().strip()
    species = row_data['species'][0][1].lower().strip()
    authorship = row_data['species'][0][2].strip()

    if row_data['species'][1] > 0:
        tonote += '[Sp. ambig. %s]' % row_data['species'][1]

    genobj = create_safely(Genus, ('name',), (genus, ), postamble='')
    spobj = create_safely(Species, ('name', 'genus', 'authorship'), (species, genobj, authorship), postamble='')

    herbitem = HerbItem(species=spobj,
                        region=row_data['region'],
                        fieldid=row_data['fieldid'],
                        itemcode=row_data['itemcode'],
                        altitude=str(row_data['altitude']),
                        collectedby=row_data['collectedby'],
                        identifiedby=row_data['identifiedby'],
                        detailed=row_data['detailed'],
                        acronym=herbacronym,
                        user=user,
                        subdivision=herbgroup
                        )

    if row_data['lat'] and row_data['lon']:
        herbitem.coordinates=Geoposition(row_data['lat'], row_data['lon'])
    if row_data['collected_s']:
        herbitem.collected_s=row_data['collected_s']
    if row_data['collected_e']:
        herbitem.collected_e=row_data['collected_e']
    if row_data['identified_s']:
        herbitem.identified_s=row_data['identified_s']
    if row_data['identified_e']:
        herbitem.identified_e=row_data['identified_e']

    # ----- additionals ----- and country, herbacronym, herbgroup ...

    # --------- get and set  country ---------------
    if row_data['country']:
        try:
            cc = Country.objects.get(name_en__icontains=row_data['country'].strip().lower())
            herbitem.country = cc
        except Country.DoesNotExist:
            pass
    # ----------------------------------------------
    # save herbitem
    herbitem.note = row_data['note'] + tonote
    herbitem.save()
    # --------- fill  additionals ----------------

    for adsp, count in row_data['additionals']:
        adgenus = adsp[0]
        adspecies = adsp[1]
        adauthor = adsp[2]
        adgenobj = create_safely(Genus, ('name',), (adgenus, ), postamble='')
        adspobj = create_safely(Species, ('name', 'genus', 'authorship'), (adspecies, adgenobj, adauthor), postamble='')
        cur_add = Additionals(herbitem=herbitem, identifiedby=row_data['identifiedby'], species=adspobj)
        if row_data['identified_s']:
            cur_add.identified_s = row_data['identified_s']
        cur_add.save()
    gc.collect()
