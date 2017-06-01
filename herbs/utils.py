#coding: utf-8

import re

from datetime import date

from django.utils.text import capfirst
from django.utils.dateformat import DateFormat
# --------------- Author string validation and extraction --------
validate_auth_str_pat = re.compile(r'^[\sa-zA-Z\.\-\(\)]+')
parenthesis_pat = re.compile(r'\(([\sa-zA-Z\.\-]+)\)')
after_parenthesis_pat = re.compile(r'\)([\sa-zA-Z\.\-]+)')
delatorre_pat = re.compile(r'\d{1,10}')
# ----------------------------------------------------------------

# ----------------Date manipulations -----------------------------

monthes = {'янв': 1,
           'фев': 2,
           'мар': 3,
           'апр': 4,
           'май': 5,
           'мая': 5,
           'июн': 6,
           'июл': 7,
           'авг': 8,
           'сен': 9,
           'ент': 9,
           'окт': 10,
           'ноя': 11,
           'дек': 12
           }
year_pat = re.compile('\d{4}')
day_pat = re.compile('[\D]+(\d{1,2})[\D]+')

NECESSARY_DATA_COLUMNS = 'family    genus    species    country    region    district    place    coordinates    altitude    ecology    collected    collectedby    identified    identifiedby itemcode  gcode note'.split()

# ----------------------------------------------------------------

def smart_unicode(s):
    # TODO: This should be checked for infinite recursion in Django
    res = ''
    if type(s) is unicode:
        res = s.encode('utf-8').strip()
    else:
        res = str(s).strip()
    if 'nan' == res.lower().strip():
        res = ''
    return res


def get_authors(auth_str):
    '''Evaluates an `author string` and returns list of authors and priorities
    '''

    _auth_str = auth_str.strip()
    err_msg = ''
    auth_array = []

    if not _auth_str:
        err_msg = 'Author not provided'
        return (err_msg, [(0, '')])
    elif not validate_auth_str_pat.match(_auth_str):
        err_msg = 'Invalid author string'
        return (err_msg, [(0, _auth_str)])

    if _auth_str.count('(') != _auth_str.count(')'):
        err_msg = 'Unbalanced parenthesis'
        return (err_msg, [(0, _auth_str)])

    if _auth_str.count('(') > 0:
        flist = parenthesis_pat.findall(_auth_str)
        if len(flist) != 1:
            err_msg = 'Auxiliary author string is empty'
            return (err_msg, [(0, _auth_str)])
        else:
            try:
                after_auth = after_parenthesis_pat.findall(_auth_str).pop().strip()
            except IndexError:
                err_msg = 'Auxiliary authors without primary authors are given'
                return (err_msg, [(0, _auth_str)])
            if after_auth:
                auth_array.append(after_auth)
            auth_array.append(flist[0])
    else:
        auth_array.append(_auth_str)

    return (err_msg, list(enumerate(reversed(auth_array))))


def evaluate_family(taxon):
    '''Could be changed in future; we don't follow dry principle here!'''
    res = taxon.split()
    authors = get_authors(' '.join(res[1:]))
    family = res[0]
    return (family, authors)


def evaluate_genus(taxon):
    '''Could be changed in future; we don't follow dry principle here!'''
    res = taxon.split()
    authors = get_authors(' '.join(res[1:]))
    genus = res[0]
    return (genus, authors)


def evaluate_species(taxon):
    '''Could be changed in future; we don't follow dry principle here!'''
    res = taxon.split()
    authors = get_authors(' '.join(res[2:]))
    species = res[1]
    return (species, authors)


def evaluate_date(item):
    '''Make str to date convertion.
    '''
    item_ = ' ' + item + ' '
    year = year_pat.findall(item_)
    if len(year) != 1:
        result = ('Год не определен', item_)
        return result
    cmonth = None
    for month in monthes.keys():
        if month in item_:
            cmonth = monthes[month]
    if not cmonth:
        result = ('Месяц не определен', item_)
        return result
    day = day_pat.findall(item_)
    if len(day) != 1:
        result = ('день не определен', item_)
        return result
    day = int(day.pop())
    year = int(year.pop())
    if not (0 < day < 32):
        result = ('День должен быть от 1 до 31', item_)
        return result
    if year > 2050 or year < 1500:
        result = ('Странное значение года', item_)
        return result
    cdate = date(year=year, day=day, month=cmonth)
    return ('', cdate)


def create_safely(model, fields=(), values=(), postamble='iexact'):
    post = '__%s' % postamble if postamble else ''
    kwargs = {'%s' % key + post: val for key, val in zip(fields, values)}
    query = model.objects.filter(**kwargs)
    if query.exists():
        return query[0]
    else:
        newobj = model(**{key: val for key, val in zip(fields, values)})
        newobj.save()
        return newobj


#  ----------- Functions below used in herbarium sheet label creation -----
def  _smartify_family(family):
    if not family:
        return ''
    return family.upper()

def _smartify_dates(item, prefix='collected'):
    date_s = getattr(item, prefix + '_s', None)
    date_e = getattr(item, prefix + '_e', None)
    if not (date_s or date_e):
        return ''
    if date_s:
        if date_e:
            fdate_s = DateFormat(date_s)
            fdate_e = DateFormat(date_e)
            if (date_e.month == date_s.month) and\
                    (date_s.day == 1) and (date_e.day in\
                                                     [30,31]):
                return fdate_s.format('M Y')
            else:
                if date_s < date_e:
                    return fdate_s.format('d M Y') +\
                       u'\N{EM DASH}' + fdate_e.format('d M Y')
                else:
                    return fdate_s.format('d M Y')
        else:
            fdate_s = DateFormat(date_s)
            return fdate_s.format('d M Y')
    elif date_e:
        fdate_e = DateFormat(date_e)
        return fdate_e.format('d M Y')


def _smartify_altitude(alt):
    if not alt: return ''
    alt = alt.strip()
    alt.replace(u' м.', ' m.')
    alt.replace(u' м ', ' m.')
    alt = alt[:30]  # Altitude couldn't be very long?!
    return alt

