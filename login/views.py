from .models import Person, Post, Comment, Like, Item, Topic
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View
from .forms import *
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import (CreateView, DeleteView, FormView, UpdateView)
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.middleware.csrf import get_token
from django.db.models import Q
from dal import autocomplete

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.views.generic import View

from braces.views import (AjaxResponseMixin, JSONResponseMixin,  LoginRequiredMixin, SuperuserRequiredMixin,)

def temp_view(request):
	context = {
		'title':'Form',
		'user':request.user,
	}
	return render(request, 'login/user_form.html', context)

def get_if_user(request):
	if request.method == 'POST':
		search_q = request.POST.get('search_q', None)
		if(search_q == ''):
			data = {'data' : True}
			return JsonResponse(data)
		k=0
		try:
			user = User.objects.get(username = search_q)
		except Exception as e:
			k = k+1

		try:
			user = User.objects.get(email = search_q)
		except Exception as e:
			k = k+1

		if k == 2:
			data = {'data':True,}
		else:
			data = {'data': False}
		return JsonResponse(data)


def general_info(request):
	if request.method == 'POST':
		print(request.POST.get('remove'))
		print(request.FILES.get('profile-pic'))
	context = {'title': 'Edit Profile'}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return redirect('/')


def video_chat_view(request):
	u = request.POST.get('user_id')
	user = User.objects.get(id = u)
	print(user.username)
	context = {
		'title':'Varta- The Video Chat',
	}
	if user == request.user:
		html = render_to_string('login/varta_chat.html', {})
	else:
		html = "<h2>You are unauthorised!! Please, Sign up!!</h2>"
	context['html'] = html
	print(html)
	return HttpResponse(json.dumps(context), content_type = 'application/json')

# Create your views here.
@login_required(login_url='/login/')
@require_POST
def post_upvote(request):
	if request.method == 'POST':
		user = request.user
		post_id = request.POST.get("post_id",None)
		post = get_object_or_404(Post,id=post_id)
		if user.person not in post.upvotes.all():
			post.upvotes.add(user.person)
			msg = "Upvoted"
			upvotes = post.upvotes.all().count()
		else:
			post.upvotes.remove(user.person)
			msg = "Unvoted"
			upvotes = post.upvotes.all().count()
		ctx = {
			'message':msg,
			'upvotes':upvotes,
		}
		return HttpResponse(json.dumps(ctx), content_type = 'application/json')
	else:
		raise Http404("page not found :/")


@login_required(login_url='/login/')
def item_create(request):
	if request.method == 'POST':
		if not request.user.is_authenticated():
			return redirect("/login")
		form = ItemForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			item = form.save(commit = False)
			item.reported_by = request.user
			item.save()
			messages.success(request, ('Your report was successfully filed!'))
			return redirect('/')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		form = ItemForm()
	context = {'form':form , 'title': 'Report Lost/Found'}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/login.html', context)

@login_required(login_url='/login/')
def lost_view(request, id=None):
	item = Item.objects.get(id=id)
	lost=False
	if item.lost == 'L':
		lost=True
	context = {'item':item , 'title': 'Lost/Found', 'lost':lost}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/lost.html', context)

@login_required(login_url='/login/')
@require_POST
def answer_upvote(request):
	if request.method == 'POST':
		user = request.user
		answer_id = request.POST.get("answer_id",None)
		answer = get_object_or_404(Answer,id=answer_id)
		if user.person not in answer.upvotes.all():
			answer.upvotes.add(user.person)
			msg = "Upvoted"
			upvotes = answer.upvotes.all().count()
		else:
			answer.upvotes.remove(user.person)
			msg = "Unvoted"
			upvotes = answer.upvotes.all().count()
		ctx = {
			'message':msg,
			'upvotes':upvotes,
		}
		return HttpResponse(json.dumps(ctx), content_type = 'application/json')
	else:
		raise Http404("page not found :/")


@login_required(login_url='/login/')
@require_POST
def follow_request(request):
	if request.method == 'POST':
		user = request.user
		user_id = request.POST.get("user_id",None)
		follow = get_object_or_404(User,id=user_id)
		if not follow.person in user.person.follows.all():
			request.user.person.follows.add(follow.person)
			msg = "followed"
		else:
			request.user.person.follows.remove(follow.person)
			msg = "Unfollowed"
		ctx = {
			'message':msg,
		}
		return HttpResponse(json.dumps(ctx), content_type = 'application/json')
	else:
		raise Http404("page not found :/")

@login_required(login_url='/login/')
def profile_view(request, id=None):
	if not request.user.is_authenticated():
		return redirect("/login")
	profile = get_object_or_404(User, id=id)
	userq = Question.objects.filter(author = profile)
	usera = Answer.objects.filter(author = profile)
	userp = Post.objects.filter(author = profile)
	context = {
	'user':request.user,
	'profile': profile,
	'userp':userp,
	'userq':userq,
	'usera':usera,
	}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/profile_view.html', context)


@login_required(login_url='/login/')
def profile_search(request):
	if request.method == 'POST':
		search_q = request.POST.get('search_q', None)
		if(search_q == ''):
			data = {'data':False,'html': ''}
			return JsonResponse(data)
		profiles = User.objects.filter(~Q(username=request.user.username)) # select * from User where username <> request.user.username;
		profiles = profiles.filter(Q(username__contains = search_q) | Q(email__contains = search_q) | Q(first_name__contains = search_q))
		# profiles = list(profiles)
		# for i in User.objects.all():
		# 	for j in search_q.split():
		# 		if i.first_name in j:
		# 			profiles = profiles + list(i)
		# 		if i.last_name in j:
		# 			profiles = profiles + list(i)
		# 		if j in i.first_name:
		# 			profiles = profiles + list(i)
		# 		if j in i.last_name:
		# 			profiles = profiles + list(i)
		profiles = set(profiles)
		count = len(profiles)
		html = render_to_string("login/profile_search.html", {'profiles': profiles, 'count': count })
		data = {
			'data':True,
			'html':html,
		}
		return JsonResponse(data)

@login_required(login_url='/login/')
def post_create(request):
	if not request.user.is_authenticated():
		return redirect("/login")
	nex = request.GET.get('next')
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.author = request.user
		instance.save()
		for idm in request.POST.getlist('topic_follows'):
			instance.topic_follows.add(Topic.objects.get(id= idm))
		instance.save()
		if nex:
			return redirect(nex)
		return redirect('/post/')
	context = {'form':form , 'title': 'New Post'}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/login.html', context)


def post_view(request, id=None):
	post = get_object_or_404(Post, id=id)
	context={
		'title':'Post',
		'user':request.user,
		'post':post,
	}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/post_view.html', context)

@login_required(login_url='/login/')
def post_details(request):
	queryset = Post.objects.all().order_by('-timestamp')
	#queryset = request.user.post_set.all()
	context = {
	'post':queryset,
	'user':request.user,
	'title':'Post Feed',
	}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/post_details.html', context)


@login_required(login_url='/login/')
def post_update(request,id=None):
	instance = get_object_or_404(Post, id=id)
	if request.user == instance.author:
		form = PostForm(request.POST or None, instance= instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			for i in instance.topic_follows.all():
				instance.topic_follows.remove(i)
			for i in request.POST.getlist('topic_follows'):
				instance.topic_follows.add(Topic.objects.get(id= i))
			instance.save()
			return HttpResponseRedirect('/post/view/'+id+"/")
		context = {
		'title':'Post',
		'instance':instance,
		'form': form,
		}
		litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
		fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
		context['litem']=litem 
		context['fitem']=fitem
		return render(request, 'login/login.html', context)
		# return render(request, 'login/login.html', context)
	else:
		raise Http404("Something went wrong!!")


@login_required(login_url='/login/')
def post_delete(request, id=None):
	if request.method == 'POST':
		user = request.user
		post_id = request.POST.get("post_id",None)
		post = get_object_or_404(Post,id=post_id)
		if user.id == post.author.id:
			post.delete()
			msg = "Deleted"
		else:
			msg = "Unauthenticated"
		ctx = {
			'message':msg,
		}
		return HttpResponse(json.dumps(ctx), content_type = 'application/json')
	else:
		raise Http404("page not found :/")

@login_required(login_url='/login/')
def question_create(request):
	if not request.user.is_authenticated():
		return redirect("/login")
	nex = request.GET.get('next')
	form = QuestionForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.author = request.user
		# print(instance.question)
		instance.save()
		for idm in request.POST.getlist('topic_follows'):
			instance.topic_follows.add(Topic.objects.get(id= idm))
		instance.save()
		if nex:
			return redirect(nex)
		return redirect('/question/view/'+str(instance.id))
	context = {'form':form , 'title': 'Ask'}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/login.html', context)

@login_required(login_url='/login/')
def question_view(request, id=None):
	question = get_object_or_404(Question, id=id)
	context={
		'title':'Question',
		'user':request.user,
		'quest':question,
	}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/question_view.html', context)

@login_required(login_url='/login/')
def question_update(request,id=None):
	instance = get_object_or_404(Question, id=id)
	if request.user == instance.author:
		form = QuestionForm(request.POST or None, instance= instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			for i in instance.topic_follows.all():
				instance.topic_follows.remove(i)
			for i in request.POST.getlist('topic_follows'):
				instance.topic_follows.add(Topic.objects.get(id= i))
			instance.save()
			return HttpResponseRedirect('/question/view/'+id+"/")
		context = {
		'title':'Edit Question',
		'instance':instance,
		'form': form,
		}
		litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
		fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
		context['litem']=litem 
		context['fitem']=fitem
		return render(request, 'login/login.html', context)
	else:
		raise Http404("page not found :/")

@login_required(login_url='/login/')
def question_delete(request, id=None):
	if request.method == 'POST':
		user = request.user
		question_id = request.POST.get("question_id",None)
		question = get_object_or_404(Question,id=question_id)
		if user.id == question.author.id:
			question.delete()
			msg = "Deleted"
		else:
			msg = "Unauthenticated"
		ctx = {
			'message':msg,
		}
		return HttpResponse(json.dumps(ctx), content_type = 'application/json')
	else:
		raise Http404("page not found :/")


@login_required(login_url='/login/')
def answer_create(request, id=None):
	if not request.user.is_authenticated():
		return redirect("/login")
	nex = request.GET.get('next')
	form = AnswerForm(request.POST or None)
	question = Question.objects.get(id=id)
	if question.author == request.user:
		raise Http404("You are not allowed to do this!")
	if form.is_valid():
		quest = Question.objects.get(id=id)
		if quest.answers.filter(author=request.user) or request.user.username == quest.author.username:
			raise Http404("Invalid Request :/")
		instance = form.save(commit=False)
		instance.author = request.user
		instance.question = quest
		# print(instance.question)
		instance.save()
		if nex:
			return redirect(nex)
		return redirect('/answer/view/'+str(instance.id))
	context = {'form':form , 'title': 'Answer', 'quest': Question.objects.get(id=id)}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/answer.html', context)

@login_required(login_url='/login/')
def answer_view(request, id=None):
	answer = get_object_or_404(Answer, id=id)
	context={
		'title':'Answer to '+answer.question.question,
		'user':request.user,
		'answer':answer,
	}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/answer_view.html', context)

@login_required(login_url='/login/')
def answer_update(request,id=None):
	instance = get_object_or_404(Answer, id=id)
	if request.user == instance.author:
		form = AnswerForm(request.POST or None, instance= instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return HttpResponseRedirect('/answer/view/'+id+"/")
		context = {
		'quest':instance.question,
		'title':'Edit Answer',
		'instance':instance,
		'form': form,
		}
		litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
		fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
		context['litem']=litem 
		context['fitem']=fitem
		return render(request, 'login/answer.html', context)
	else:
		raise Http404("page not found :/")

@login_required(login_url='/login/')
def answer_delete(request, id=None):
	if request.method == 'POST':
		user = request.user
		answer_id = request.POST.get("answer_id",None)
		answer = get_object_or_404(Answer,id=answer_id)
		if user.id == answer.author.id:
			answer.delete()
			msg = "Deleted"
		else:
			msg = "Unauthenticated"
		ctx = {
			'message':msg,
		}
		return HttpResponse(json.dumps(ctx), content_type = 'application/json')
	else:
		raise Http404("page not found :/")


def login_view(request):
	if request.user.is_authenticated():
		return redirect('/')
	return redirect('/accounts/login/')

# def login_view(request):
# 	if request.user.is_authenticated():
# 		return redirect("/")
# 	nex = request.GET.get('next')
# 	form = UserForm(request.POST or None)
# 	if form.is_valid():
# 		username = form.cleaned_data.get("username")
# 		password = form.cleaned_data.get("password")
# 		user= authenticate(username=username, password=password)
# 		login(request, user)
# 		print(request.user.is_authenticated())
# 		if nex:
# 			return redirect(nex)
# 		return redirect("/")

# 	return render(request, 'login/login.html', {'form':form, 'title': 'Log In'})

class person_info(UpdateView):
	model = Person
	fields = ['gender', 'display_pic', 'about_me', 'cv']


# def register_view(request):
# 	if request.user.is_authenticated(): 
# 		return redirect("/")
# 	form = UserRegisterForm(request.POST or None)
# 	nex = request.GET.get('next')
# 	if form.is_valid():
# 		user = form.save(commit=False)
# 		password = form.cleaned_data.get('password')
# 		user.set_password(password)
# 		user.save()
# 		new_user= authenticate(username=user.username, password=password)
# 		login(request, new_user)
# 		if nex:
# 			return redirect(nex)
# 		return redirect("/")
# 	context = {'form':form, 'title': 'Sign Up'}
# 	return render(request, 'login/login.html', context)


@login_required(login_url='/login/')
def person_view(request):
	if request.method == 'POST':
		form = PersonForm(request.POST, request.FILES, instance=request.user.person)
		if form.is_valid():
			form.save()
			user=User.objects.get(id=request.user.id)
			if request.POST.get('remove'):
				user.person.display_pic.delete(save=False)
			if request.FILES.get('profile-pic'):
				user.person.display_pic=request.FILES.get('profile-pic')
			user.first_name = request.POST.get('first_name')
			user.last_name = request.POST.get('last_name')
			user.save()
			messages.success(request, ('Your profile was successfully updated!'))
			return redirect('/')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		form = PersonForm(instance=request.user.person)
	context = {'form':form , 'title': 'Edit Profile'}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp') # select * from Item where lost="L" order by timestamp ASC;
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp') # select * from Item where lost="F" order by timestamp ASC;
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/user_form.html', context)



def logout_view(request):
	logout(request)
	return redirect("/login/")

@login_required(login_url='/login/')
def index(request):
	user = request.user
	person = user.person
	follows = person.follows.all()
	fuser = list()
	fuser.append(user)
	for i in follows:
		fuser.append(i.username)
	if not request.user.first_name:
		return redirect('/fillup')
	feed_a = Answer.objects.filter(author__in = fuser)[:5]
	feed_p = Post.objects.filter(author__in = fuser)[:5]
	feed_q = Question.objects.all().order_by('-timestamp')[:5]
	feed = list(feed_q) + list(feed_a) + list(feed_p)
	feed.sort(key=lambda x: x.timestamp, reverse=True)
	context = {
			'feed':feed,
			'user':user,
			'title': 'Latest Feed'
	}
	litem = Item.objects.filter(lost= 'L').order_by('-timestamp')
	fitem = Item.objects.filter(lost= 'F').order_by('-timestamp')
	context['litem']=litem 
	context['fitem']=fitem
	return render(request, 'login/feed.html', context)

@login_required(login_url='/login/')
def categories(request):
	if request.user.username:
		user = request.user
	elif user.username:
		user=user
	return render(request, 'login/category.html', {'user': user, 'auth': request.user.is_authenticated()})

@login_required(login_url='/login/')
def auth(request):
	try:
		user = Person.objects.get(email=request.POST['email'], password=request.POST['password'])
	except(KeyError, Person.DoesNotExist):
		return render(request, 'login/login.html', {
			'error_message':'Invalid username or password'
			})
	user.active=True
	return render(request, 'login/head.html', {'ppl': user})


class TopicAutocomplete(autocomplete.Select2QuerySetView):
	def create_topic(self):
		topic = Topic.objects.create(name = self.q)
		topic.save()
		print("2")
		return topic.pk

	def get_queryset(self):
		 # Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return Topic.objects.none()
		qs = Topic.objects.all()
		print("1")
		if self.q:
			qs = qs.filter(name__istartswith=self.q)
		return qs

class AjaxableResponseMixin(object):

    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'success': 0,
                'error': form.errors})
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            csrf_token_value = get_token(self.request)
            html = render_to_string(
                "comments/comment.html",
                {'object': self.object,
                 'user': self.request.user,
                 'form': CommentForm(),
                 'liked': False,
                 'csrf_token': csrf_token_value,
                 'allow_likes': getattr(
                    settings,
                    'COMMENTS_ALLOW_LIKES',
                    True)
                 })
            try:
                data = {
                    'success': 1,
                    'html': html,
                    'id': self.object.id,
                    'oid':self.object.object_id,
                }
            except:
                data = {
                    'success': 1,
                }
            return JsonResponse(data)
        else:
            return response


class CommentCreateView(AjaxableResponseMixin, CreateView):

    """
    Class that creates an instance of model:comment.Comment

    """
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment_form.html'
    success_url = reverse_lazy('comment-create')

    def form_valid(self, form):
        comment = form.save(commit=False)
        try:
            content_type = ContentType.objects.get(
                app_label=self.request.POST['app_name'],
                model=self.request.POST['model'].lower())
            model_object = content_type.get_object_for_this_type(
                id=self.request.POST['model_id'])
            comment.content_object = model_object
        except:
            pass
        comment.save()
        return super(CommentCreateView, self).form_valid(form)


class CommentDeleteView(DeleteView):

    """
    Class that deletes an instance of model:comment.Comment

    """
    model = Comment
    success_url = reverse_lazy('comment-create')

    def get(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        try:
            id = request.GET['id']
            self.object = Comment.objects.get(id=id)
            if (self.object.user.id == request.user.id or self.object.content_object.author.id == request.user.id):
                self.object.delete()
                data = {"success": "1",
                        "count": Comment.objects.count(),
                        'oid': self.object.object_id,}
            else:
                data = {"success": "0"}
        except:
            data = {"success": "0"}
        if request.is_ajax():
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(self.success_url)


class LikeComment(FormView):

    """
    Class that creates an instance of model:comment.Like
    """

    def get(self, request, *args, **kwargs):
        comment_id = request.GET['comment_id']
        likes_count = 0
        data = {}

        # Check if user is authenticated.
        if not request.user.is_authenticated():
            # Return if user is not authenticated.
            data['success'] = 0
            data['error'] = "You have to sign in first"
            return JsonResponse(data)

        user = request.user
        try:
            # Check if the comment with the requested id exists.
            comment = Comment.objects.get(id=comment_id)
            likes_count = comment.likes_count
            try:
                # Check if the user already liked the comment,
                # Do nothing in this case.
                Like.objects.get(comment=comment, user=user)
                data['success'] = 0
                data['error'] = "You have already liked this comment"
            except:
                # Create a like on the comment in case the user hasn't
                # liked it already.
                Like.objects.create(comment=comment, user=user).save()
                likes_count = Like.objects.filter(comment=comment).count()
                comment.likes_count = likes_count
                comment.save()
                data['likes_count'] = likes_count
                data['success'] = 1
        except:
            # Return an error where the comment might have been removed.
            data['success'] = 0
            data['error'] = "This comment might have been removed"
        return JsonResponse(data)


class UnlikeComment(FormView):

    """
    Class that deletes an instance of model:comment.Like
    """

    def get(self, request, *args, **kwargs):
        comment_id = request.GET['comment_id']
        likes_count = 0
        data = {}

        # Check if user is authenticated.
        if not request.user.is_authenticated():
            # Return if user is not authenticated.
            data['success'] = 0
            data['error'] = "You have to sign in first"
            return JsonResponse(data)

        user = request.user
        try:
            # Check if the comment with the requested id exists.
            comment = Comment.objects.get(id=comment_id)
            likes_count = comment.likes_count
            try:
                # Check if the user already liked the comment,
                # Unlike the comment in this case.
                Like.objects.get(comment=comment, user=user).delete()
                likes_count =Like.objects.filter(comment=comment).count()
                comment.likes_count =  likes_count
                comment.save()
                data['success'] = 1
                data['likes_count'] = likes_count
            except:
                # If the user hasn't liked it, return an error.
                data['success'] = 0
                data['error'] = "You have to like the comment first"
        except:
            # Return an error where the comment might have been removed.
            data['error'] = "This comment might have been removed"
        return JsonResponse(data)


class CommentUpdateView(AjaxableResponseMixin, UpdateView):

    """
    Class that updates an instance of model:comment.Comment
    """
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment_edit_form.html'
    success_url = reverse_lazy('comment-create')

    def form_valid(self, form):
        if not self.object.user:
            return HttpResponse('not allowed')
        else:
            if (self.request.user.is_authenticated and
                    self.object.user == self.request.user):
                form.save()
                return super(CommentUpdateView, self).form_valid(form)
            else:
                return HttpResponse('not authenticated')



# class UserFormView(View):
# 	form_class = UserForm
# 	template_name = 'login/register.html'

# 	def get(self, request):
# 		form = self.form_class(None)
# 		return render(request, self.template_name, {'form': form})

# 	def post(self, request):
# 		form = self.form.save(commit=False)

# 		username = form.cleaned_data['username']
# 		password = form.cleaned_data['password']
# 		user.set_password(password)
# 		user.save()   

# 		user = authenticate(username=username, password=password)

# 		if user is not None:

# 			if user.is_active:
# 				login(request, user)
# 				return redirect('home:/')

# 		return render(request, self.template_name, {'form': form})
