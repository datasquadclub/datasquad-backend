import json
import uuid

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Visit
from .utils import get_client_ip, parse_client, guess_lang, lookup_country


@csrf_exempt
@require_POST
def track_pageview(request):
    """Endpoint appelé en JS (beacon) à chaque chargement de page du site
    statique Data Squad. Enregistre une visite et pose/relit un cookie
    visiteur anonyme (aucune donnée personnelle identifiable stockée)."""
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("invalid json")

    path = str(payload.get("path", ""))[:500]
    referrer = str(payload.get("referrer", ""))[:500]
    if not path:
        return HttpResponseBadRequest("missing path")

    cookie_name = settings.VISITOR_COOKIE_NAME
    raw_cookie = request.COOKIES.get(cookie_name)
    is_new_visitor = False
    try:
        visitor_id = uuid.UUID(raw_cookie) if raw_cookie else None
    except ValueError:
        visitor_id = None
    if visitor_id is None:
        visitor_id = uuid.uuid4()
        is_new_visitor = True

    ua_string = request.META.get("HTTP_USER_AGENT", "")
    parsed = parse_client(ua_string)
    ip = get_client_ip(request)

    Visit.objects.create(
        visitor_id=visitor_id,
        ip_address=ip,
        path=path,
        referrer=referrer,
        lang=guess_lang(path),
        user_agent=ua_string[:1000],
        browser=parsed["browser"],
        os=parsed["os"],
        device_type=parsed["device_type"],
        country=lookup_country(ip),
        is_new_visitor=is_new_visitor,
    )

    response = JsonResponse({"status": "ok"})
    response.set_cookie(
        cookie_name,
        str(visitor_id),
        max_age=settings.VISITOR_COOKIE_MAX_AGE,
        samesite="None" if not settings.DEBUG else "Lax",
        secure=not settings.DEBUG,
        httponly=True,
    )
    return response
