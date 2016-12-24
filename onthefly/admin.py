from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings


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
            settings.backend.add_field(name)
        elif action_type == 'delete_field':
            settings.backend.delete_field(name)
        elif action_type == 'set_value':
            settings.backend.set_value(name, request.POST.get('value'))
        request.method = 'GET'
        return self.get(request, *args, **kwargs)


admin.site.register_view('onthefly-settings/', 'Onthefly Settings',
                         view=AppSettingsView.as_view())
