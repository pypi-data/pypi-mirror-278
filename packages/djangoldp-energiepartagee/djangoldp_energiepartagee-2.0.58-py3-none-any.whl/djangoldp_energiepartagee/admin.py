from django.conf import settings
from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin

from djangoldp_energiepartagee.models import *


@admin.register(
    CommunicationProfile,
    SAPermission,
    Testimony,
)
class EmptyAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(
    College,
    Collegeepa,
    Integrationstep,
    Interventionzone,
    Legalstructure,
    Paymentmethod,
    Profile,
    CapitalDistribution,
    EnergyBuyer,
    EnergyType,
    EnergyProduction,
    ContractType,
    Partner,
    Shareholder,
    PartnerLink,
    PartnerLinkType,
)
class EPModelAdmin(DjangoLDPAdmin):
    readonly_fields = ("urlid",)
    exclude = ("is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(PartnerType)
class EPPartnerTypeAdmin(EPModelAdmin):
    filter_horizontal = ("partners",)


@admin.register(Regionalnetwork)
class EPRegionalnetworkAdmin(EPModelAdmin):
    filter_horizontal = ("colleges",)


@admin.register(Region)
class EPRegionAdmin(EPModelAdmin):
    filter_horizontal = ("admins",)


@admin.register(EarnedDistinction)
class EPDistinctionAdmin(EPModelAdmin):
    filter_horizontal = ("citizen_projects",)


@admin.register(SiteEarnedDistinction)
class EPSiteEarnedDistinctionAdmin(EPModelAdmin):
    filter_horizontal = ("production_sites",)


class TestimonyInline(admin.TabularInline):
    model = Testimony
    fk_name = "citizen_project"
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class CommunicationProfileInline(admin.StackedInline):
    model = CommunicationProfile
    fk_name = "citizen_project"
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(CitizenProject)
class CitizenProjectAdmin(DjangoLDPAdmin):
    # list_display = ('urlid', 'name', 'allow_self_registration')
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    inlines = [CommunicationProfileInline, TestimonyInline]
    search_fields = ["urlid", "name", "partnered_by__actor__members__user__urlid"]
    ordering = ["urlid"]


@admin.register(ProductionSite)
class ProductionSiteAdmin(DjangoLDPAdmin):
    # list_display = ('urlid', 'name', 'allow_self_registration')
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    search_fields = ["urlid", "name"]
    ordering = ["urlid"]


@admin.register(Actor)
class ActorAdmin(EPModelAdmin):
    list_display = ("longname", "shortname", "updatedate", "createdate")
    search_fields = ["longname", "shortname"]
    filter_horizontal = ("interventionzone",)


@admin.register(Relatedactor)
class RelatedactorAdmin(EPModelAdmin):
    list_display = ("__str__", "role")
    search_fields = [
        "actor__longname",
        "actor__shortname",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]


if not getattr(settings, "IS_AMORCE", False):

    @admin.register(Contribution)
    class ContributionAdmin(EPModelAdmin):
        list_display = ("actor", "year", "updatedate", "createdate")
        search_fields = ["actor__longname", "actor__shortname"]
        filter_horizontal = ("discount",)

        def get_readonly_fields(self, request, obj=None):
            if obj and obj.contributionstatus in (
                "a_ventiler",
                "valide",
            ):
                return self.readonly_fields + ("amount",)
            return self.readonly_fields

else:

    admin.site.register(Contribution, EmptyAdmin)
