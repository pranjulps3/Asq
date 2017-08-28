from django import forms
from django.contrib.auth.models import User
from .models import *
from pagedown.widgets import PagedownWidget
from django.contrib.auth import authenticate, login, logout, get_user_model
from markdownx.fields import MarkdownxFormField
from draceditor.fields import DraceditorFormField
from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete
from django.db import models

class AnswerForm(forms.ModelForm):
    content = DraceditorFormField()
    class Meta:
        model = Answer
        fields = [ 'content']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','lost','image','details']

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self, *args, **kwargs):
    	username = self.cleaned_data.get('username')
    	password = self.cleaned_data.get('password')
    	user= authenticate(username=username, password=password)
    	if not user:
    		raise forms.ValidationError("The user doen't exist")
    	if not user.check_password(password):
    		raise forms.ValidationError("The password doen't match")
    	if not user.check_password(password):
    		raise forms.ValidationError("The password doen't match")
    	return super(UserForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [ 'gender', 'about_me']

class PostForm(forms.ModelForm):
    #publish =  forms.DateField(widget = forms.SelectDateWidget)
    content = DraceditorFormField()
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Heading for the Post...'}))
    topic_follows = models.ManyToManyField('login.topic')
    #content = forms.CharField(widget = PagedownWidget)
    #content = MarkdownxFormField(widget = PagedownWidget)
    class Meta:
        model = Post
        fields = [ 'title', 'topic_follows' , 'content']
        widgets = {'topic_follows': autocomplete.ModelSelect2Multiple(url='topic-autocomplete')}

class QuestionForm(forms.ModelForm):
    question = forms.CharField()
    topic_follows = models.ManyToManyField('login.topic')
    class Meta:
        model = Question
        fields = [ 'question', 'topic_follows', 'details']
        widgets = {'topic_follows': autocomplete.ModelSelect2Multiple(url='topic-autocomplete')}

class UserRegisterForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    # password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model=User
        fields = ['username','email', 'first_name', 'last_name']

    # def clean_password2(self):
    #     password= self.cleaned_data.get('password')
    #     password2= self.cleaned_data.get('password2')
    #     if password != password2:
    #         raise forms.ValidationError("Passwords Don't Match")
    #     return password

    def clean_email(self):
        email= self.cleaned_data.get('email')
        email_qs= User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email already Taken")
        return email

    def clean_username(self):
        username= self.cleaned_data.get('username')
        username_qs= User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("username already Taken")
        return username

    def clean_first_name(self):
        first_name= self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("Name required")
        return first_name

    def signup(self, request, user):
        if request.user.is_authenticated(): 
            return redirect("/")
        form = UserRegisterForm(request.POST or None)
        nex = request.GET.get('next')
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user= authenticate(username=user.username, password=password)
            login(request, new_user)
            if nex:
                return redirect(nex)
            return redirect("/")
        context = {'form':form, 'title': 'Sign Up'}
        return render(request, 'login/login2.html', context)

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='comment', 
        widget=forms.Textarea(
            attrs={'rows':'1','cols':'70','placeholder': 'Write a Comment...', 'class':'comment-form-class'}
        )
    )
    class Meta:
        model = Comment
        exclude = ('likes_count', 'dislikes_count', 'content_type', 'object_id', 'content_object')