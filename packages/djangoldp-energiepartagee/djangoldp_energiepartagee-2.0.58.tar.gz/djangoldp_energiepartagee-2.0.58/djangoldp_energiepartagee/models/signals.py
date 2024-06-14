from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template import loader
from django.utils.translation import gettext_lazy as _

from djangoldp_energiepartagee.models import *


@receiver(post_save, sender=Actor)
def create_actor_global(sender, instance, created, **kwargs):
    CapitalDistribution.objects.get_or_create(actor=instance)
    if created:
        memberInstance = instance.members.create(
            role=ROLE_CHOICES[0][0], user=instance.managementcontact
        )
        memberInstance.save()


if not getattr(settings, "IS_AMORCE", False):

    @receiver(post_save, sender=Actor)
    def create_actor_contributions(sender, instance, created, **kwargs):
        if created:
            if not instance.contributions or not instance.contributions.exists():
                amount = instance.get_next_contribution_amount()

                contributionInstance = instance.contributions.create(
                    year=Contribution.get_current_contribution_year(),
                    numberpeople=instance.numberpeople,
                    numberemployees=instance.numberemployees,
                    turnover=instance.turnover,
                    amount=amount,
                    paymentto=instance.regionalnetwork,
                    contributionnumber=Contribution._get_next_contribution_number(),
                )
                contributionInstance.save()

                integrationstepInstance = Integrationstep(
                    packagestep=True,
                    adhspacestep=True,
                    adhliststep=True,
                    regionalliststep=True,
                )
                integrationstepInstance.save()
                instance.integrationstep = integrationstepInstance

                instance.save()

    @receiver(pre_save, sender=Actor)
    def compute_contributions(sender, instance, **kwargs):
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            current_year_contribution = Contribution.objects.filter(
                actor=instance, year=Contribution.get_current_contribution_year()
            ).first()
            if current_year_contribution:
                if (
                    current_year_contribution.contributionstatus
                    == CONTRIBUTION_CHOICES[0][0]
                    or current_year_contribution.contributionstatus
                    == CONTRIBUTION_CHOICES[1][0]
                    or current_year_contribution.contributionstatus
                    == CONTRIBUTION_CHOICES[2][0]
                ):
                    current_year_contribution.amount = (
                        instance.get_next_contribution_amount()
                    )
                    current_year_contribution.numberpeople = instance.numberpeople
                    current_year_contribution.numberemployees = instance.numberemployees
                    current_year_contribution.turnover = instance.turnover
                    # Detect change on Villageoise field
                    if old_instance.villageoise != instance.villageoise:
                        # Check if the discount Villageoise is applied and apply it on
                        villageoise = Discount.objects.filter(name="villageoise").all()[
                            0
                        ]
                        if instance.villageoise:
                            current_year_contribution.discount.add(villageoise)
                        else:
                            current_year_contribution.discount.remove(villageoise)
                    current_year_contribution.save()

    @receiver(pre_save, sender=Contribution)
    def update_status_after_payment_change(sender, instance, **kwargs):
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            # New contribution
            pass
        else:
            # Detect change on payment fields
            if (
                old_instance.receivedby == instance.receivedby
                or old_instance.paymentmethod == instance.paymentmethod
                or old_instance.paymentdate == instance.paymentdate
            ):

                # Check if payment fields are filled
                if (
                    instance.receivedby is not None
                    and instance.paymentmethod is not None
                    and instance.paymentdate is not None
                ):

                    # Change status except if is already 'validé'
                    if instance.contributionstatus != CONTRIBUTION_CHOICES[4][0]:
                        instance.contributionstatus = CONTRIBUTION_CHOICES[3][0]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance,
            picture="https://moncompte.energie-partagee.org/img/default_avatar_user.svg",
        )


@receiver(post_save, sender=Relatedactor)
def send_mail_after_new_join_request(instance, created, **kwargs):
    if created:
        if not instance.actor.members.filter(role="admin", user=instance.user):
            for admin in instance.actor.members.filter(role="admin"):
                text_message = loader.render_to_string(
                    "emails/txt/new_join_request.txt",
                    {
                        "user": instance.user,
                        "actor": instance.actor,
                        "front_url": getattr(
                            settings, "INSTANCE_DEFAULT_CLIENT", "http://localhost"
                        ),
                    },
                )
                html_message = loader.render_to_string(
                    "emails/html/new_join_request.html",
                    {
                        "is_amorce": getattr(settings, "IS_AMORCE", False),
                        "user": instance.user,
                        "actor": instance.actor,
                        "front_url": getattr(
                            settings, "INSTANCE_DEFAULT_CLIENT", "http://localhost"
                        ),
                    },
                )
                title = "Energie Partagée"
                if getattr(settings, "IS_AMORCE", False):
                    title = "AMORCE"
                send_mail(
                    title
                    + " - Nouvelle demande pour rejoindre l'acteur "
                    + instance.actor.longname,
                    text_message,
                    settings.DEFAULT_FROM_EMAIL or "contact@energie-partagee.fr",
                    [admin.user.email],
                    fail_silently=False,
                    html_message=html_message,
                )


@receiver(post_save, sender=Actor)
def update_project_visibility_from_actor(instance, created, **kwargs):
    if not created:
        if instance.visible is False:
            CitizenProject.objects.filter(founder=instance).update(visible=False)


@receiver(pre_save, sender=CitizenProject)
def update_project_visibility_from_itself(instance, **kwargs):
    if instance.visible and instance.status != "published":
        instance.visible = False


@receiver(post_save, sender=CitizenProject)
def update_production_site_visibility_from_project(instance, created, **kwargs):
    if not created:
        if instance.visible is False:
            ProductionSite.objects.filter(citizen_project=instance).update(
                visible=False
            )
