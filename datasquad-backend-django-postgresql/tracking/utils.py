import ipaddress

import requests
from user_agents import parse as parse_ua


def get_client_ip(request):
    """Récupère l'IP réelle du visiteur, y compris derrière un reverse-proxy
    (Nginx/Render/Railway...) qui pose l'en-tête X-Forwarded-For."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def parse_client(user_agent_string):
    ua = parse_ua(user_agent_string or "")
    if ua.is_bot:
        device_type = "bot"
    elif ua.is_mobile:
        device_type = "mobile"
    elif ua.is_tablet:
        device_type = "tablet"
    elif ua.is_pc:
        device_type = "desktop"
    else:
        device_type = "other"
    return {
        "browser": (ua.browser.family or "")[:50],
        "os": (ua.os.family or "")[:50],
        "device_type": device_type,
    }


def guess_lang(path):
    path = (path or "").lstrip("/")
    if path.startswith("en/"):
        return "en"
    if path.startswith("ar/"):
        return "ar"
    return "fr"


def _is_public_ip(ip):
    try:
        addr = ipaddress.ip_address(ip)
    except (ValueError, TypeError):
        return False
    return not (addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved)


def lookup_country(ip):
    """Renvoie le nom du pays correspondant à une IP publique, ou "" si
    l'IP est privée/locale ou si le service de géolocalisation ne répond
    pas. Utilise ip-api.com (gratuit, sans clé, ~45 requêtes/minute) --
    largement suffisant pour un petit site associatif. En cas de panne ou
    de dépassement de quota, on continue simplement sans le pays (aucune
    visite n'est perdue, le champ reste juste vide)."""
    if not ip or not _is_public_ip(ip):
        return ""
    try:
        resp = requests.get(
            f"http://ip-api.com/json/{ip}",
            params={"fields": "status,country"},
            timeout=2,
        )
        data = resp.json()
        if data.get("status") == "success":
            return (data.get("country") or "")[:100]
    except Exception:
        pass
    return ""
