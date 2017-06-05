 # -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os

sys.path.append('/home/scidam/webapps/bgicms242/bgi')
os.environ['DJANGO_SETTINGS_MODULE']='bgi.settings'
import gc
from bgi.herbs.models import Genus, Species
from bgi.herbs.utils import  create_safely
import pandas as pd
import re

CDIR = os.path.dirname(os.path.abspath(__file__))

syns = pd.read_excel(os.path.join(CDIR, 'syns.xlsx'))
syns = syns.astype(pd.np.object)

syns = syns.applymap(lambda a: a.strip())

syns =syns[~syns.approved.str.contains('the same')]


def split_species(sp):
    _sp = sp.split()
    if len(_sp) == 1:
        return (_sp[0].strip().lower(), '', '')
    if len(_sp) == 2:
        return _sp[0].strip().lower(), _sp[1].strip().lower(), ''
    elif len(_sp) >= 3:
        return _sp[0].strip().lower(), _sp[1].strip().lower(), ' '.join(_sp[2:])


total=0
for ind, row in syns.iterrows():
    cur_genus, cur_species, cur_author = split_species(row.current)
    syn_genus, syn_species, syn_author = split_species(row.approved)
    try:
        cgenus = Genus.objects.get(name=cur_genus)
    except (Genus.DoesNotExist, Genus.MultipleObjectsReturned):
        print('Genus', cur_genus, 'not exists')
        continue
    try:
        cspecies = Species.objects.get(name=cur_species, genus=cgenus, authorship=cur_author)
    except Species.DoesNotExist:
        
        if cur_genus and cur_species and cur_author:
            print('Will be created', cur_species, cur_genus, cur_author)
            cspecies = create_safely(Species, fields=('name','genus', 'authorship'), values=(cur_species, cgenus, cur_author), postamble='')
        else:
            continue

    try:
        sgenus = Genus.objects.get(name=syn_genus)
    except (Genus.DoesNotExist, Genus.MultipleObjectsReturned):
        print('Genus syn', syn_genus, 'not found')
        continue
    try:
        sspecies = Species.objects.get(name=syn_species, genus=sgenus, authorship=syn_author)
    except Species.DoesNotExist:
        if syn_genus and syn_species and syn_author:
            print('Will be created (syn)', syn_species, syn_genus, syn_author)
            sspecies = create_safely(Species, fields=('name','genus', 'authorship'), values=(syn_species, sgenus, syn_author), postamble='')
        else:
            continue
    
    if  (syn_species!=cur_species) or (syn_genus!=cur_genus) or (syn_author!=cur_author):
        cspecies.synonym = sspecies
        cspecies.save()
    else:
        cspecies.synonym = None
        cspecies.save()
    total+=1

print('Total modified species', total)