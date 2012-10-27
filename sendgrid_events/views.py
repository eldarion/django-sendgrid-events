from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from sendgrid_events.models import Event


@require_POST
@csrf_exempt
def handle_batch_post(request):
    Event.process_batch(data=request.raw_post_data)
    return HttpResponse()
