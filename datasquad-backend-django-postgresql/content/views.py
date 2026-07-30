from django.http import JsonResponse

from .models import NewsPost, TeamMember


def _initials(name):
    parts = [p for p in name.split() if p]
    return ("".join(p[0] for p in parts[:2])).upper()


def actus_list(request):
    posts = NewsPost.objects.filter(is_published=True)
    data = [
        {
            "title": p.title,
            "date_label": p.date_label,
            "body": p.body,
            "photo": p.photo.url if p.photo else None,
        }
        for p in posts
    ]
    return JsonResponse({"results": data})


def equipe_list(request):
    members = TeamMember.objects.filter(is_published=True)
    data = [
        {
            "name": m.name,
            "initials": m.initials or _initials(m.name),
            "role": m.role,
            "mission": m.mission,
            "photo": m.photo.url if m.photo else None,
        }
        for m in members
    ]
    return JsonResponse({"results": data})
