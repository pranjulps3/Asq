"""spacesuite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from login.views import *
import notifications.urls


app_name='home'



urlpatterns = [

	#Home
	url(r'^$', index, name='index'),
	#semantic
	url(r'^varta/', video_chat_view, name='varta_chat'),
	#all auth urls
	url(r'^accounts/', include('allauth.urls')),
	# #social auth
	# url(r'^oauth/', include('social_django.urls', namespace='social')),
	#Topic Autocomplete
	url(r'^topic-autocomplete/$', TopicAutocomplete.as_view(create_field = 'name'), name='topic-autocomplete'),
	#login
	url(r'^login/', login_view, name='login'),
	#notification handling side
	url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
	#report lost and found
	url(r'^report/', item_create, name='report'),
	#lost found view
	url(r'^lost/(?P<id>\d+)/$', lost_view, name='lost_view'),
	#follow users
	url(r'^follow/request/', follow_request, name='follow_request'),
	#edit profile
	url(r'^fillup/', person_view, name='fillup'),
	#markdown drag and drop markdown editor
	url(r'^markdownx/', include('markdownx.urls')),
	#friendship and follow(doesn't work)
	url(r'^friendship/', include('friendship.urls'), name='friendship'),
	#post create
	url(r'^post/create/', post_create, name = 'create_post'),
	#upvote a post
	url(r'^post/upvote/', post_upvote, name = 'upvote_post'),
	#upvote a post
	url(r'^answer/upvote/', answer_upvote, name = 'upvote_answer'),
	#update post
	url(r'^post/update/(?P<id>\d+)/$', post_update, name = 'update_post'),
	#view individual post
	url(r'^post/view/(?P<id>\d+)/$', post_view, name='view_post'),
	#delete post
	url(r'^post/delete/', post_delete, name = 'delete_post'),
	#post feed
	url(r'^post/', post_details, name = 'details_post'),
	#question create
	url(r'^question/create/', question_create, name = 'create_question'),
	#update question
	url(r'^question/update/(?P<id>\d+)/$', question_update, name = 'update_question'),
	#view individual question
	url(r'^question/view/(?P<id>\d+)/$', question_view, name='view_question'),
	#delete question
	url(r'^question/delete/', question_delete, name = 'delete_question'),
	#answer create
	url(r'^answer/create/(?P<id>\d+)/$', answer_create, name = 'create_answer'),
	#update answer
	url(r'^answer/update/(?P<id>\d+)/$', answer_update, name = 'update_answer'),
	#view individual answer
	url(r'^answer/view/(?P<id>\d+)/$', answer_view, name='view_answer'),
	#delete answer
	url(r'^answer/delete/', answer_delete, name = 'delete_answer'),
	#create a comment
	url(r'^comment/create/$', CommentCreateView.as_view(), name='comment-create'),
	#update a comment
    url(r'comment/update/(?P<pk>[0-9]+)/$',CommentUpdateView.as_view(), name='comment-update'),
    #delete a comment
    url(r'^comment/delete/(?P<pk>[-\w]+)$', CommentDeleteView.as_view(), name='comment-delete'),
    #like a comment
    url(r'^comments/like/$', LikeComment.as_view(), name='comment-like'),
    #unlike a comment
    url(r'^comments/unlike/$', UnlikeComment.as_view(), name='comment-unlike'),
    #simply logout or GTFO
	url(r'^logout/', logout_view, name='logout'),
	#draceditor urls
	url(r'^draceditor/', include('draceditor.urls')),
	#Searching Users
	url(r'^search/user/profiles/', profile_search, name='profile_search'),
	#view individuals profile
	url(r'^view/profile/(?P<id>\d+)/$', profile_view, name='profile_view'),
	# #sing up or register
	# url(r'^register/', register_view, name='register'),
	#admin/
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
