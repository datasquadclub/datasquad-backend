import csv
from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone

from .models import Visit

admin.site.site_header = "Data Squad — Administration"
admin.site.site_title = "Data Squad Admin"
admin.site.index_title = "Tableau de bord"


@admin.action(description="Exporter la sélection en CSV")
def export_visits_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="visites_data_squad.csv"'
    writer = csv.writer(response)
    writer.writerow(["Date", "Page", "Pays", "Langue", "Appareil", "Navigateur", "OS", "IP", "Référent", "Nouveau visiteur"])
    for v in queryset.order_by("-created_at"):
        writer.writerow([v.created_at, v.path, v.country, v.lang, v.device_type, v.browser, v.os, v.ip_address, v.referrer, v.is_new_visitor])
    return response


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("created_at", "path", "country", "lang", "device_type", "browser", "os", "ip_address", "is_new_visitor")
    list_filter = ("country", "lang", "device_type", "browser", "os", "is_new_visitor", "created_at")
    search_fields = ("path", "ip_address", "referrer", "visitor_id")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in Visit._meta.fields]
    actions = [export_visits_csv]

    def has_add_permission(self, request):
        # Les visites sont créées uniquement par le site web, jamais à la main.
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("dashboard/", self.admin_site.admin_view(self.dashboard_view), name="tracking_dashboard"),
        ]
        return custom + urls

    def dashboard_view(self, request):
        now = timezone.now()
        since_30d = now - timedelta(days=30)
        since_14d = now - timedelta(days=14)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        total_visits = Visit.objects.count()
        visits_today = Visit.objects.filter(created_at__gte=today_start).count()
        visits_30d = Visit.objects.filter(created_at__gte=since_30d).count()
        unique_visitors_30d = Visit.objects.filter(created_at__gte=since_30d).values("visitor_id").distinct().count()

        top_pages = (
            Visit.objects.filter(created_at__gte=since_30d)
            .values("path")
            .annotate(n=Count("id"))
            .order_by("-n")[:10]
        )
        max_page = max([p["n"] for p in top_pages], default=1)

        per_day = (
            Visit.objects.filter(created_at__gte=since_14d)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(n=Count("id"))
            .order_by("day")
        )
        max_day = max([d["n"] for d in per_day], default=1)

        devices = (
            Visit.objects.filter(created_at__gte=since_30d)
            .values("device_type")
            .annotate(n=Count("id"))
            .order_by("-n")
        )

        countries = (
            Visit.objects.filter(created_at__gte=since_30d)
            .exclude(country="")
            .values("country")
            .annotate(n=Count("id"))
            .order_by("-n")[:10]
        )
        max_country = max([c["n"] for c in countries], default=1)

        context = dict(
            self.admin_site.each_context(request),
            title="Tableau de bord des visites — Data Squad",
            total_visits=total_visits,
            visits_today=visits_today,
            visits_30d=visits_30d,
            unique_visitors_30d=unique_visitors_30d,
            top_pages=[{"path": p["path"], "n": p["n"], "pct": round(p["n"] * 100 / max_page)} for p in top_pages],
            per_day=[{"day": d["day"], "n": d["n"], "pct": round(d["n"] * 100 / max_day)} for d in per_day],
            devices=devices,
            countries=[{"country": c["country"], "n": c["n"], "pct": round(c["n"] * 100 / max_country)} for c in countries],
        )
        return TemplateResponse(request, "admin/tracking/dashboard.html", context)
