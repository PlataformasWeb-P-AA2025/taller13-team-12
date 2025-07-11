from django.contrib import admin
from app.models import Edificio, Departamento
# Register your models here.
class EdificioAdmin(admin.ModelAdmin):
 
    list_display = ('nombre', 'ciudad', 'tipo')


    search_fields = ('nombre', 'ciudad','tipo')

admin.site.register(Edificio, EdificioAdmin)


class DepartamentoAdmin(admin.ModelAdmin):
 
    list_display = ('nombres', 'apellidos', 'costo', 'edificio')
  
    raw_id_fields = ('edificio',)

admin.site.register(Departamento, DepartamentoAdmin)