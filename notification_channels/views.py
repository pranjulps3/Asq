from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


login_url = getattr(settings, "LOGIN_URL", "/")


@login_required(login_url=login_url)
def notifications(request):
	return render(request, "notification_channels/notify.html", {"notifications": request.user.notifications.all()})