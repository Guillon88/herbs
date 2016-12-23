from ajax_select import register, LookupChannel
from .models import Family, Genus, Species, Country, HerbItem
from .conf import settings, HerbsAppConf
import re


NS = getattr(settings,
             '%s_AUTOSUGGEST_NUM_ADMIN' % HerbsAppConf.Meta.prefix.upper(),
             20)
ACHAR = getattr(settings,
             '%s_AUTOSUGGEST_CHAR' % HerbsAppConf.Meta.prefix.upper(),
             3)


@register('family')
class FamilyLookup(LookupChannel):
    model = Family
    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:NS]


@register('genus')
class GenusLookup(LookupChannel):
    model = Genus
    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:NS]


@register('species')
class SpeciesLookup(LookupChannel):
    model = Species
    def get_query(self, q, request):
        mq = q.lstrip()
        res = self.model.objects.none()
        if len(mq) >= ACHAR:
            splitted = mq.split()
            if len(splitted) > 1:
                res = self.model.objects.filter(genus__name__istartswith=splitted[0],
                                             name__icontains=splitted[1])
            else:
                res = self.model.objects.filter(genus__name__istartswith=splitted[0])
        return res[:NS]


@register('country')
class CountryLookup(LookupChannel):
    model = Country
    def get_query(self, q, request):
        if re.match('.*[a-zA-Z]+.*', q):
            res = self.model.objects.filter(name_en__icontains=q)
        else:
            res = self.model.objects.filter(name_ru__icontains=q)
        return res[:NS]


#class DifferentValueMixin(LookupChannel):
    #'''Abstract class'''
    # def get_query(self, q, request):
        #objs = HerbItem.objects.raw('''SELECT * FROM herbs_herbitem WHERE %s LIKE "%%%s%%" GROUP BY %s''',
                                    #[self.fieldname, q, self.fieldname])
        #return map(lambda x: getattr(x, self.fieldname), objs[:NS])


@register('region')
class RegionLookup(LookupChannel):
    def get_query(self, q, request):
        return HerbItem.objects.filter(region__icontains=q).values_list('region', flat=True).distinct()[:NS]

@register('district')
class DistrictLookup(LookupChannel):
    def get_query(self, q, request):
        return HerbItem.objects.filter(district__icontains=q).values_list('district', flat=True).distinct()[:NS]

@register('collectedby')
class CollectorsLookup(LookupChannel):
    def get_query(self, q, request):
        return HerbItem.objects.filter(collectedby__icontains=q).values_list('collectedby', flat=True).distinct()[:NS]

@register('identifiedby')
class IdentifiersLookup(LookupChannel):
    def get_query(self, q, request):
        return HerbItem.objects.filter(identifiedby__icontains=q).values_list('identifiedby', flat=True).distinct()[:NS]

