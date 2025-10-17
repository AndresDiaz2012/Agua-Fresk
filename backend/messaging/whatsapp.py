import requests
from django.conf import settings


class WhatsAppClient:
    def __init__(self):
        self.base_url = settings.WHATSAPP_API_BASE
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.token = settings.WHATSAPP_TOKEN
        if not self.phone_number_id or not self.token:
            # In development, we allow missing configuration but raise on send
            pass

    def _headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def send_template(self, to_e164: str, template_name: str, variables: dict):
        if not self.phone_number_id or not self.token:
            raise RuntimeError('WhatsApp API not configured')

        url = f"{self.base_url}/{self.phone_number_id}/messages"
        # Basic example using a text template with variables interpolated client-side
        text = (
            f"Hola {variables.get('name','')},\n"
            f"te recordamos tu servicio de agua en {variables.get('address','')}.\n"
            f"Responde este mensaje para coordinar el despacho."
        )
        payload = {
            "messaging_product": "whatsapp",
            "to": to_e164.replace('+', ''),
            "type": "text",
            "text": {"body": text},
        }
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=20)
        resp.raise_for_status()
        return resp.json()
