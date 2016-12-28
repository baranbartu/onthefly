from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import messages
from onthefly.utils import SUPPORTED_TYPES, convert


class AppSettingsView(TemplateView):
    """
    Show current settings
    """
    template_name = 'admin/onthefly_settings.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AppSettingsView, self).get_context_data(
            *args, **kwargs)
        context.update({
            'original_settings': (
                settings.get_original_settings_without_onthefly),
            'onthefly_settings': settings.get_onthefly_settings
        })
        return context

    def post(self, request, *args, **kwargs):
        action_type = request.POST.get('actiontype')
        name = request.POST.get('name')
        if action_type == 'add_field':
            original_value = settings.backend.get_value_from_original_settings(
                name)
            if original_value is None:
                messages.error(
                    request, 'NoneType objects can not be changed at runtime!')
            elif type(original_value) not in SUPPORTED_TYPES:
                messages.error(
                    request,
                    '%s is not supported to add ONTHEFLY settings!' % (
                        type(original_value)), )
            else:
                settings.backend.add_field(name)
                settings.backend.set_value(name, original_value)
        elif action_type == 'delete_field':
            settings.backend.delete_field(name)
            settings.backend.delete_value(name)
        elif action_type == 'set_value':
            original_value = settings.backend.get_value_from_original_settings(
                name)
            if type(original_value) not in SUPPORTED_TYPES:
                messages.error(
                    request,
                    '%s is not supported to add ONTHEFLY settings!' % (
                        type(original_value)), )
            value = request.POST.get('value')
            converted_value = convert(value, type(original_value))
            if converted_value is None:
                messages.error(
                    request,
                    'Original value type is different than current type!')
            else:
                settings.backend.set_value(name, converted_value)
        request.method = 'GET'
        return self.get(request, *args, **kwargs)


admin.site.register_view('onthefly-settings/', 'Onthefly Settings',
                         view=AppSettingsView.as_view())
