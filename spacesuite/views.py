from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def main(request):
	if request.user.username:
		user = request.user
	elif user.username:
		user=user
		request.user = user
	return render(request, 'login/index.html', {'user': user, 'auth': request.user.is_authenticated()})


def index(request):
	#notify.send(request.user, recipient=request.user, verb=u'logged in', action_object=request.user, target=request.user)
	return render(request, 'login/index.html')
