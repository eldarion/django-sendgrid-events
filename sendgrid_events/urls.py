from django.conf.urls import patterns, url


urlpatterns = patterns(
    "sendgrid_events.views",
    url(r"^batch/$", "handle_batch_post", name="sendgrid_handle_batch_post")
)
