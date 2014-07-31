.. _usage:

Usage
=====

Using this after it has been setup in your site depends on what you want
to accomplish. Just installing it will enable you to receive events on
every email sent through your Sendgrid account.

That by itself, however, likely produces much value as there is no
context to those emails to derive any meaningful use out of.

One of the cool things you can do now that you have the Events API
configured and django-sendgrid-events hooked up, is send identifying
data in the headers of each email you send so that when you receive
and Event API POST you can tied each email back to some event in your
site.

To accomplish this you should make sure your email settings are
configured to use your Sendgrid account::

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.sendgrid.net")
    EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = True

And then whenever you are sending an email in your site that you
want to be able to track the response to send an extra header like
so::

    email = EmailMultiAlternatives(
        "Your Subject Here",
        "Your plain text message here",
        "sender@email.com",
        ["recipient@email.com"],
        headers={
            "X-SMTPAPI": json.dumps({
                "unique_args": {
                    "some_key": "some_value"
                },
                "category": "some_category"
            })
        }
    )
    email.attach_alternative("Your html rendered email", "text/html")
    email.send()

You don't have to send HTML emails, but you can control the look a
bit better since in order to get open and click event tracking with
plain text emails, Sendgrids converts it to an HTML email, which
can end up not looking how you'd like it to.

Now when your events POST to the endpoint you have setup, they'll
have this extra bit of data which you can use to link to something
in your site. For example, say, you want to link it to the instance
of a specific content model you can pass in as a ``unique_arg``::

    "unique_args": {
        "my_model_pk": object.pk
    }

Then hook up a signal receiver for ``sendgrid_events.signals.batch_processed``::

    from django.dispatch import receiver

    from sendgrid_events.signals import batch_processed
    from mysite.myapp.models import SomeContent


    @receiver(batch_processed)
    def handle_batch_processed(sender, events, **kwargs):
        for event in events:
            try:
                c = SomeContent.objects.get(pk=event.data.get("my_model_pk"))
                c.email_events.create(sendgrid_event=event)
            except SomeContent.DoesNotExist:
                pass

Where you have created a tracking model in your ``mysite.myapps.models`` for
``SomeContent``::

    class SomeContentEvent(models.Model):
        some_content = models.ForeignKey(SomeContent, related_name="email_events")
        sendgrid_event = models.ForeignKey(Event, related_name="+")

        class Meta:
            ordering = ["sendgrid_event__created_at"]

Now, you have access to email events for that object that you can use in
your site::

    {% for event in some_content.email_events.all %}
        <span class="label label-{{ event.kind }}" title="{{ event.created_at }}">
            {{ event.kind }}
        </span>
    {% endfor %}
