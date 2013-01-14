from django.contrib import admin

from .models import Event


admin.site.register(Event, list_display=["kind", "email", "created_at"], list_filter=["created_at", "kind"], search_fields=["email", "data"])
