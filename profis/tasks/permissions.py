from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsWorker(permissions.BasePermission):
    """
    Permission class for determining User type.
    """

    message = _("Только исполнители могут опубликовать задачу")

    def has_permission(self, request: Request, view: APIView) -> bool:
        if view.action == "create":
            return request.user.is_worker
