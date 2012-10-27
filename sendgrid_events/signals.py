import django.dispatch


batch_processed = django.dispatch.Signal(providing_args=["events"])
