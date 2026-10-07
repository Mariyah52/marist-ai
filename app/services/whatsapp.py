import httpx
from app.core.config import settings

def send_text(to: str, text: str) -> bool:
    if not settings.whatsapp_token or not settings.whatsapp_phone_number_id:
        return False
    url = f"https://graph.facebook.com/{settings.whatsapp_graph_version}/{settings.whatsapp_phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {settings.whatsapp_token}", "Content-Type": "application/json"}
    payload = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    r = httpx.post(url, headers=headers, json=payload, timeout=20)
    return r.is_success
