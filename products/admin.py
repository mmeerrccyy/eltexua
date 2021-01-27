from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField, ModelForm


# Register your models here.

class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance:
            self.fields['sd'].widget.attrs.update(
                {
                    'readonly': True, 'style': 'background: lightgray'
                }
            )
            self.fields['back_cam'].widget.attrs.update(
                {
                    'readonly': True, 'style': 'background: lightgray'
                }
            )
            self.fields['front_cam'].widget.attrs.update(
                {
                    'readonly': True, 'style': 'background: lightgray'
                }
            )

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd'] = None
            return self.cleaned_data
        if not self.cleaned_data['back_cam']:
            self.cleaned_data['back_cam'] = None
            return self.cleaned_data
        if not self.cleaned_data['front_cam']:
            self.cleaned_data['front_cam'] = None
            return self.cleaned_data


class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='Ноутбуки'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PCAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='ПК'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TabletAdmin(admin.ModelAdmin):

    change_form_template = 'products/admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='Планшети'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'products/admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='Смартфони'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TVAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='Телевізори'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AudioAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(name='Навушники'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
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