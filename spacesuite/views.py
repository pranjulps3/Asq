from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from notifications.signals import notify

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

def categories(request):
	return render(request, 'login/category.html')

# Create your views here.
@login_required(login_url='/login/')
def manufact(request):
	return render(request, 'login/manufact.html')

@login_required(login_url='/login/')
def busi(request):
	return render(request, 'login/busi.html')

@login_required(login_url='/login/')
def civil(request):
	return render(request, 'login/civil.html')

@login_required(login_url='/login/')
def corpo(request):
	return render(request, 'login/corpo.html')

@login_required(login_url='/login/')
def crimi(request):
	return render(request, 'login/crimi.html')

@login_required(login_url='/login/')
def cs(request):
	return render(request, 'login/cs.html')

@login_required(login_url='/login/')
def dental(request):
	return render(request, 'login/dental.html')

@login_required(login_url='/login/')
def elec(request):
	return render(request, 'login/elec.html')

@login_required(login_url='/login/')
def envi(request):
	return render(request, 'login/envi.html')

@login_required(login_url='/login/')
def finance(request):
	return render(request, 'login/finance.html')

@login_required(login_url='/login/')
def homeo(request):
	return render(request, 'login/homeo.html')

@login_required(login_url='/login/')
def hotel(request):
	return render(request, 'login/hotel.html')

@login_required(login_url='/login/')
def mecha(request):
	return render(request, 'login/mecha.html')

@login_required(login_url='/login/')
def pharma(request):
	return render(request, 'login/pharma.html')

@login_required(login_url='/login/')
def service(request):
	return render(request, 'login/service.html')

@login_required(login_url='/login/')
def surgery(request):
	return render(request, 'login/surgery.html')
