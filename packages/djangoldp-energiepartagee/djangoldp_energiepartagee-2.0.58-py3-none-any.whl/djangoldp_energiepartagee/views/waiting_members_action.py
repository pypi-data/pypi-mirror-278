from datetime import date

import validators
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.views import LDPAPIView, NoCSRFAuthentication
from rest_framework import status
from rest_framework.response import Response

from djangoldp_energiepartagee.models.related_actor import Relatedactor


class WaitingMembersActionView(LDPAPIView):
    authentication_classes = (NoCSRFAuthentication,)

    # def dispatch(self, request, *args, **kwargs):
    #     response = super(WaitingMembersActionView, self).dispatch(request, *args, **kwargs)
    #     response["Access-Control-Allow-Origin"] = request.headers.get('origin')
    #     response["Access-Control-Allow-Methods"] = "POST, GET"
    #     response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
    #     response["Access-Control-Expose-Headers"] = "Location, User"
    #     response["Access-Control-Allow-Credentials"] = 'true'
    #     response["Accept-Post"] = "application/json"
    #     response["Accept"] = "*/*"

    #     if request.user.is_authenticated:
    #         try:
    #             response['User'] = request.user.webid()
    #         except AttributeError:
    #             pass
    #     return response

    def post(self, request, pk):
        # from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        if request.data:
            urlid = settings.BASE_URL + "/relatedactors/" + str(pk)
            if validators.url(urlid):
                model, instance = Model.resolve(urlid)
                if instance:
                    obj = Relatedactor.objects.get(pk=pk)
                    title = "Energie Partagée"
                    if getattr(settings, "IS_AMORCE", False):
                        title = "AMORCE"
                    if request.data == "reminder":
                        specificdata = {
                            "email_text": "emails/txt/waiting_reminder.txt",
                            "email_html": "emails/html/waiting_reminder.html",
                            "email_title": title
                            + " - Vous avez une demande en attente pour l'acteur ",
                            "status": "",
                            "email": instance.actor.managementcontact.email,
                        }
                        obj.reminderdate = date.today()
                        obj.save()
                    else:
                        if request.data == "refuse":
                            specificdata = {
                                "email_text": "emails/txt/join_actor_denied.txt",
                                "email_html": "emails/html/join_actor_denied.html",
                                "email_title": title
                                + " - Votre demande de rejoindre l'acteur ",
                                "status": " a été refusée",
                                "email": instance.user.email,
                            }
                        else:
                            specificdata = {
                                "email_text": "emails/txt/join_actor_validated.txt",
                                "email_html": "emails/html/join_actor_validated.html",
                                "email_title": title
                                + " - Votre demande de rejoindre l'acteur ",
                                "status": " a été acceptée",
                                "email": instance.user.email,
                            }
                        obj.role = request.data
                        obj.save()
                text_message = loader.render_to_string(
                    specificdata["email_text"],
                    {
                        "sender": request.user,
                        "user": instance.user,
                        "role": request.data,
                        "actor": instance.actor,
                        "uri": request.build_absolute_uri("/media/"),
                        "front_url": getattr(
                            settings, "INSTANCE_DEFAULT_CLIENT", "http://localhost"
                        ),
                        "back_url": settings.BASE_URL,
                    },
                )
                html_message = loader.render_to_string(
                    specificdata["email_html"],
                    {
                        "is_amorce": getattr(settings, "IS_AMORCE", False),
                        "sender": request.user,
                        "user": instance.user,
                        "role": request.data,
                        "actor": instance.actor,
                        "uri": request.build_absolute_uri("/media/"),
                        "front_url": getattr(
                            settings, "INSTANCE_DEFAULT_CLIENT", "http://localhost"
                        ),
                        "back_url": settings.BASE_URL,
                    },
                )
                send_mail(
                    _(
                        specificdata["email_title"]
                        + instance.actor.longname
                        + specificdata["status"]
                    ),
                    text_message,
                    settings.EMAIL_HOST_USER or "contact@energie-partagee.fr",
                    [specificdata["email"]],
                    fail_silently=False,
                    html_message=html_message,
                )
            response = Response(
                {"content": "This is a success"}, status=status.HTTP_200_OK
            )

            return response

        return Response(status=204)
