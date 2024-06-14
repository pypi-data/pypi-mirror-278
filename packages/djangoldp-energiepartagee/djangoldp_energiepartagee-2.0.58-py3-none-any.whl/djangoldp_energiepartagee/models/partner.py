from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_energiepartagee.models.actor import Actor
from djangoldp_energiepartagee.models.citizen_project import CitizenProject


class Partner(Model):
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteur",
        related_name="partner_of",
    )
    citizen_project = models.ForeignKey(
        CitizenProject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Projet Citoyen",
        related_name="partnered_by",
    )

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [InheritPermissions]
        inherit_permissions = ["actor", "citizen_project"]
        rdf_type = "energiepartagee:partner"
        nested_fields = ["types"]
        verbose_name = _("Partenaire")
        verbose_name_plural = _("Partenaires")

    def __str__(self):
        return self.urlid
