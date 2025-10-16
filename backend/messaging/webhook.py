from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from .models import MessageLog


@csrf_exempt
def whatsapp_webhook(request: HttpRequest):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse(status=403)

    if request.method == 'POST':
        # Minimal handler: update delivery/read statuses
        data = request.json if hasattr(request, 'json') else None
        if not data:
            try:
                import json
                data = json.loads(request.body.decode('utf-8'))
            except Exception:
                data = {}
        try:
            entries = data.get('entry', [])
            for entry in entries:
                for change in entry.get('changes', []):
                    messages = change.get('value', {}).get('statuses', [])
                    for st in messages:
                        msg_id = st.get('id')
                        status = st.get('status')
                        if not msg_id:
                            continue
                        try:
                            log = MessageLog.objects.get(provider_message_id=msg_id)
                            if status in ['sent', 'delivered', 'read', 'failed']:
                                log.status = status
                                log.save(update_fields=['status'])
                        except MessageLog.DoesNotExist:
                            continue
        except Exception:
            pass
        return JsonResponse({"ok": True})

    return HttpResponse(status=405)
