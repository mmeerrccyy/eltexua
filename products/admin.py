from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField


# Register your models here.

class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(SubCategory.objects.filter(name='Ноутбуки'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PCAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(SubCategory.objects.filter(name='ПК'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TabletAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(SubCategory.objects.filter(name='Планшети'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(SubCategory.objects.filter(name='Смартфони'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TVAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(SubCategory.objects.filter(name='Телевізори'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AudioAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(SubCategory.objects.filter(name='Навушники'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(PersonalComputer, PCAdmin)
admin.site.register(Tablet, TabletAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(TVset, TVAdmin)
admin.site.register(Audio, AudioAdmin)