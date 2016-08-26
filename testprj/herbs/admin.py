from django.contrib import admin

# Register your models here.


from .models import (Family, Genus, GenusAuthorship, FamilyAuthorship,
                     SpeciesAuthorship, PendingHerbs,
                     Author, HerbItem, Species, LoadedFiles,
                     ErrorLog)
from .forms import (FamilyForm, GenusForm, HerbItemForm,
                    GenusAuthorshipForm, FamilyAuthorshipForm,  AuthorForm,
                    SpeciesForm, SpeciesAuthorshipForm
                    )
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminTabularInline




class AuthorAdmin(admin.ModelAdmin):
    form = AuthorForm 


class FamilyAuthorshipInline(AjaxSelectAdminTabularInline):
    form = FamilyAuthorshipForm
    model = FamilyAuthorship
    extra = 0

class GenusAuthorshipInline(AjaxSelectAdminTabularInline):
    form = GenusAuthorshipForm
    model = GenusAuthorship
    extra = 0

class SpeciesAuthorshipInline(AjaxSelectAdminTabularInline):
    form = SpeciesAuthorshipForm
    model = SpeciesAuthorship
    extra = 1


class FamilyAdmin(admin.ModelAdmin):
    form = FamilyForm
    inlines = (
        FamilyAuthorshipInline,
        )


class GenusAdmin(admin.ModelAdmin):
    form = GenusForm
    inlines = (
        GenusAuthorshipInline,
        )

class HerbItemAdmin(AjaxSelectAdmin):
    form = HerbItemForm
    list_display = ('get_full_name', 'gcode','itemcode','family', 'genus', 'species', 'collectedby', 'collected_s')
    list_filter = ('public', 'family', 'genus', 'species')
    inlines = (
        SpeciesAuthorshipInline,
        )
    search_fields = ('itemcode', 'gcode', 'collectedby', 'identifiedby', 'family__name', 'genus__name')
    
class PendingHerbsAdmin(admin.ModelAdmin):
    model = PendingHerbs
    list_display = ('get_full_name', 'checked','itemcode','family', 'genus', 'species','collectedby','collected_s')
    list_filter = ('public', 'family', 'genus', 'species')


class LoadedFilesAdmin(admin.ModelAdmin):
    model = LoadedFiles
    list_display = ('datafile', 'status','createdby', 'created')
    list_filter = ('status', 'createdby')

class SpeciesAdmin(admin.ModelAdmin): 
    form = SpeciesForm

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'created')
    readonly_fields = ('message', 'created')
#     def show_messages(self, obj):
#         return '<a href="%s">%s</a>' % (obj.firm_url, obj.firm_url)
#     show_firm_url.allow_tags = True    


admin.site.register(Family, FamilyAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register(HerbItem, HerbItemAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(PendingHerbs, PendingHerbsAdmin)
admin.site.register(LoadedFiles, LoadedFilesAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)
