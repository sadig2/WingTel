from django.contrib import admin
from django.apps import apps

apps = apps.get_app_configs()

for app in apps:

    # app = apps.get_app_config('usage')

    for model_name, model in app.models.items():
        model_admin = type(model_name + "Admin", (admin.ModelAdmin, ), {})

        model_admin.list_display = model.admin_list_display if hasattr(
            model, 'admin_list_display') else tuple(
                [field.name for field in model._meta.fields])
        try:
            admin.site.unregister(model)
        except:
            pass
            # print(f"{model}not registered")
        admin.site.register(model, model_admin)
